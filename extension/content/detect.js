/**
 * content/detect.js — entry point for the content script.
 *
 * Watches for a selection, floats a small trigger next to it, and drives the panel. It
 * holds no token and makes no network call: everything goes through the service worker
 * (see `background/sw.js` for why).
 */

import { extractQuestion } from "./adapters.js";
import { Panel } from "./panel.js";
import { startCapture } from "./capture.js";

const TRIGGER_ID = "mlt-socratic-trigger";
let panel = null;

function getPanel() {
  if (!panel) panel = new Panel();
  return panel;
}

function removeTrigger() {
  document.getElementById(TRIGGER_ID)?.remove();
}

function showTrigger(rect) {
  removeTrigger();
  const button = document.createElement("button");
  button.id = TRIGGER_ID;
  button.textContent = "Ask MLT";
  Object.assign(button.style, {
    position: "absolute",
    top: `${window.scrollY + rect.bottom + 8}px`,
    left: `${window.scrollX + rect.left}px`,
    zIndex: "2147483646",
    padding: "6px 12px",
    borderRadius: "8px",
    border: "0",
    background: "#1a6ed8",
    color: "#fff",
    font: "600 12px -apple-system, 'Segoe UI', Roboto, sans-serif",
    boxShadow: "0 3px 12px rgba(0,0,0,.22)",
    cursor: "pointer",
  });
  button.addEventListener("mousedown", (event) => {
    // mousedown, not click: clicking would first clear the selection we need to read.
    event.preventDefault();
    event.stopPropagation();
    const question = extractQuestion();
    removeTrigger();
    if (question?.stem) analyze(question.stem, question.options);
  });
  document.body.appendChild(button);
}

async function analyze(selection, options, sourceKind = "selection") {
  const view = getPanel();
  view.loading();
  const response = await chrome.runtime.sendMessage({
    type: "analyze",
    payload: {
      selection,
      options: options || [],
      page_url: window.location.href,
      source_kind: sourceKind,
    },
  });

  if (response?.ok) {
    view.render(response.data);
    return;
  }
  showFailure(view, response, "Something went wrong analysing that selection.", () =>
    analyze(selection, options, sourceKind));
}

/**
 * One place that turns a failed `apiFetch` reply into something a student can act on.
 *
 * Every caller needs the same three-way split — sign in, the backend is down, or the
 * request itself was refused — and the status code is the only thing that distinguishes
 * them. The final branch prints the server's `detail` **and** the status precisely so an
 * unexpected code names itself instead of hiding behind a friendly sentence.
 */
function showFailure(view, response, fallback, retry) {
  if (response?.status === 401) {
    view.message("Sign in with your IITM Google account to use the companion.", {
      label: "Sign in",
      onClick: async () => {
        const signedIn = await chrome.runtime.sendMessage({ type: "signIn" });
        if (signedIn?.ok) retry();
        else view.message(signedIn?.error || "Sign-in failed.");
      },
    });
    return;
  }
  if (response?.status === 0) {
    // Backend unreachable is explicitly NOT a sign-out — a restarted server must not
    // evict the session, exactly as the SPA's client treats status 0.
    view.message("Can't reach the study assistant. Is the backend running?");
    return;
  }
  const detail = response?.data?.detail;
  const code = response?.status ? ` (HTTP ${response.status})` : "";
  view.message(`${detail || response?.error || fallback}${code}`);
}

document.addEventListener("selectionchange", () => {
  const selection = window.getSelection();
  const text = (selection?.toString() || "").trim();
  if (text.length < 25) {
    removeTrigger();
    return;
  }
  const range = selection.getRangeAt(0);
  const rect = range.getBoundingClientRect();
  if (rect.width || rect.height) showTrigger(rect);
});

document.addEventListener("mousedown", (event) => {
  if (event.target?.id !== TRIGGER_ID) removeTrigger();
});

chrome.runtime.onMessage.addListener((message) => {
  if (message?.type === "openPanel" && message.selection) {
    analyze(message.selection, []);
  }
  if (message?.type === "startCapture") {
    startCapture((result) => {
      if (result.failure) {
        showFailure(
          getPanel(),
          result.failure,
          result.failure.status === 503
            ? "No text reader is available right now."
            : "Could not read that crop.",
          () => startCapture(() => {}),
        );
        return;
      }
      if (result.error) {
        getPanel().message(result.error);
        return;
      }
      analyze(result.text, result.options, "capture");
    });
  }
});
