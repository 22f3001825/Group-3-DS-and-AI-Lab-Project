/**
 * background/sw.js — the extension's only network surface.
 *
 * **Every fetch happens here, never in a content script.** With `host_permissions` for
 * the API origin, MV3 background fetches are not subject to the *page's* CORS policy, so
 * the backend needs no change to serve a content script. That is load-bearing now that the
 * content script matches `<all_urls>`: doing the same fetch from the page context would be
 * a cross-origin request from whatever site the student happens to be on, and the API
 * would have to allow every one of them.
 *
 * It also means the session token never enters the page's JavaScript context, where any
 * script on the portal could read it.
 */

const DEFAULT_API = "http://localhost:8000";
const TOKEN_KEY = "mlt_token";
const API_KEY = "mlt_api_url";

async function apiUrl() {
  const stored = await chrome.storage.local.get(API_KEY);
  return (stored[API_KEY] || DEFAULT_API).replace(/\/+$/, "");
}

async function getToken() {
  const stored = await chrome.storage.local.get(TOKEN_KEY);
  return stored[TOKEN_KEY] || null;
}

async function setToken(token) {
  if (token) await chrome.storage.local.set({ [TOKEN_KEY]: token });
  else await chrome.storage.local.remove(TOKEN_KEY);
}

/**
 * Google sign-in via `launchWebAuthFlow`, which is the only OAuth entry point available
 * to an extension — there is no `<GoogleLogin>` button and no page to host one.
 *
 * `response_type=id_token` matters: the backend's `POST /auth/google` verifies a Google
 * **ID token**, exactly as the SPA sends. An access-token flow would produce no ID token
 * and there would be nothing to verify. The nonce is echoed back inside the signed token,
 * so a replayed response from another flow does not validate.
 */
async function signIn(interactive = true) {
  const { mlt_client_id: clientId } = await chrome.storage.local.get("mlt_client_id");
  if (!clientId) throw new Error("Set your Google Client ID on the extension options page.");

  const redirectUri = chrome.identity.getRedirectURL();
  const nonce = crypto.randomUUID();
  const authUrl =
    "https://accounts.google.com/o/oauth2/v2/auth" +
    `?client_id=${encodeURIComponent(clientId)}` +
    `&response_type=id_token` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}` +
    `&scope=${encodeURIComponent("openid email profile")}` +
    `&nonce=${encodeURIComponent(nonce)}` +
    `&prompt=${interactive ? "select_account" : "none"}`;

  const redirect = await chrome.identity.launchWebAuthFlow({ url: authUrl, interactive });
  // The id_token arrives in the URL fragment, not the query string.
  const fragment = new URLSearchParams((redirect || "").split("#")[1] || "");
  const credential = fragment.get("id_token");
  if (!credential) throw new Error("Google returned no ID token.");

  const base = await apiUrl();
  const response = await fetch(`${base}/auth/google`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ credential }),
  });
  if (!response.ok) throw new Error(`Sign-in rejected (${response.status}).`);

  const data = await response.json();
  await setToken(data.access_token);
  return data;
}

/**
 * One authenticated call. A 401 clears the stored token and reports `unauthorized` so the
 * panel can offer a sign-in button — mirroring the SPA's `mlt:unauthorized` handling.
 *
 * A 403 deliberately does NOT clear the token: the caller is signed in and simply may not
 * do that thing, and signing them out would be both wrong and confusing.
 */
async function apiFetch(path, { method = "GET", body = null, isForm = false } = {}) {
  const token = await getToken();
  if (!token) return { ok: false, status: 401, error: "unauthorized" };

  const base = await apiUrl();
  const headers = { Authorization: `Bearer ${token}` };
  if (!isForm) headers["Content-Type"] = "application/json";

  let response;
  try {
    response = await fetch(`${base}${path}`, {
      method,
      headers,
      body: isForm ? body : body ? JSON.stringify(body) : null,
    });
  } catch (err) {
    // Backend unreachable is not a sign-out: a restarted uvicorn must not log the user
    // out of the extension.
    return { ok: false, status: 0, error: String(err) };
  }

  if (response.status === 401) {
    await setToken(null);
    return { ok: false, status: 401, error: "unauthorized" };
  }

  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }
  return { ok: response.ok, status: response.status, data };
}

const HANDLERS = {
  async signIn() {
    return { ok: true, data: await signIn(true) };
  },
  async signOut() {
    await setToken(null);
    return { ok: true };
  },
  async status() {
    const token = await getToken();
    if (!token) return { ok: false, status: 401 };
    return apiFetch("/auth/me");
  },
  analyze: (payload) => apiFetch("/socratic/analyze", { method: "POST", body: payload }),
  hint: ({ sessionId }) => apiFetch(`/socratic/${sessionId}/hint`, { method: "POST" }),
  attempt: ({ sessionId, studentAnswer }) =>
    apiFetch(`/socratic/${sessionId}/attempt`, {
      method: "POST",
      body: { student_answer: studentAnswer },
    }),

  /**
   * Screenshot the visible tab so the panel can crop it. This is the whole reason the PDF
   * case works: a content script cannot read Chrome's built-in PDF viewer, but the viewer
   * is rendered pixels and `captureVisibleTab` sees pixels.
   */
  async capture() {
    const dataUrl = await chrome.tabs.captureVisibleTab({ format: "png" });
    return { ok: true, data: { dataUrl } };
  },

  async transcribe({ dataUrl }) {
    const blob = await (await fetch(dataUrl)).blob();
    const form = new FormData();
    form.append("file", blob, "crop.png");
    return apiFetch("/socratic/transcribe", { method: "POST", body: form, isForm: true });
  },
};

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  const handler = HANDLERS[message?.type];
  if (!handler) {
    sendResponse({ ok: false, error: `unknown message: ${message?.type}` });
    return false;
  }
  handler(message.payload || {})
    .then(sendResponse)
    .catch((err) => sendResponse({ ok: false, error: String(err?.message || err) }));
  return true; // keep the channel open for the async reply
});

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "mlt-socratic",
    title: "Ask the MLT companion about this",
    contexts: ["selection"],
  });
});

/**
 * Message a tab, injecting the content script first if nothing is listening.
 *
 * "Receiving end does not exist" is the normal state more often than it looks: reloading
 * the extension kills the content script in every open tab, and it does not come back
 * until that tab is reloaded. Re-injecting costs one `executeScript` and removes the
 * "reload the page first" step from every debugging round.
 *
 * `scripting` and `activeTab` are already in the manifest, so this needs no new permission.
 * It cannot rescue Chrome's built-in PDF viewer — no content script runs there at all —
 * which is why the failure is reported rather than swallowed.
 */
async function send(tabId, message) {
  try {
    return await chrome.tabs.sendMessage(tabId, message);
  } catch {
    try {
      await chrome.scripting.executeScript({ target: { tabId }, files: ["content/bundle.js"] });
      return await chrome.tabs.sendMessage(tabId, message);
    } catch (err) {
      console.warn("[MLT] no content script in this tab:", String(err?.message || err));
      return null;
    }
  }
}

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "mlt-socratic" && tab?.id) {
    send(tab.id, { type: "openPanel", selection: info.selectionText });
  }
});

chrome.action.onClicked.addListener((tab) => {
  if (tab?.id) send(tab.id, { type: "startCapture" });
});
