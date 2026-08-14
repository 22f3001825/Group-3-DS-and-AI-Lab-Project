const api = document.getElementById("api");
const client = document.getElementById("client");
const status = document.getElementById("status");

function line(text) {
  const p = document.createElement("p");
  p.textContent = text;
  return p;
}

async function refresh() {
  const stored = await chrome.storage.local.get(["mlt_api_url", "mlt_client_id"]);
  api.value = stored.mlt_api_url || "http://localhost:8000";
  client.value = stored.mlt_client_id || "";

  status.replaceChildren();
  status.appendChild(line(`Redirect URI to authorise: ${chrome.identity.getRedirectURL()}`));

  const me = await chrome.runtime.sendMessage({ type: "status" });
  if (me?.ok) {
    status.appendChild(line(`Signed in as ${me.data.email}${me.data.is_admin ? " (admin)" : ""}.`));
  } else {
    status.appendChild(line("Not signed in."));
  }
}

document.getElementById("save").addEventListener("click", async () => {
  await chrome.storage.local.set({
    mlt_api_url: api.value.trim().replace(/\/+$/, ""),
    mlt_client_id: client.value.trim(),
  });
  refresh();
});

document.getElementById("signin").addEventListener("click", async () => {
  const result = await chrome.runtime.sendMessage({ type: "signIn" });
  if (!result?.ok) {
    status.replaceChildren(line(result?.error || "Sign-in failed."));
    return;
  }
  refresh();
});

document.getElementById("signout").addEventListener("click", async () => {
  await chrome.runtime.sendMessage({ type: "signOut" });
  refresh();
});

refresh();
