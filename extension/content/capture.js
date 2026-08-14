/**
 * content/capture.js — drag a box, screenshot it, send the pixels for OCR.
 *
 * This is the only path that works on a question-paper PDF. Chrome's built-in viewer is a
 * separate, privileged document: a content script cannot read its text, query its DOM, or
 * select inside it. What it *can* do is ask the service worker for
 * `chrome.tabs.captureVisibleTab`, which renders whatever is on screen — viewer included.
 *
 * The crop happens here rather than server-side so only the question travels, not the
 * whole tab (which may be showing an entire exam, and is a much larger upload).
 */

const OVERLAY_ID = "mlt-capture-overlay";

export function startCapture(onText) {
  if (document.getElementById(OVERLAY_ID)) return;

  const overlay = document.createElement("div");
  overlay.id = OVERLAY_ID;
  Object.assign(overlay.style, {
    position: "fixed",
    inset: "0",
    zIndex: "2147483646",
    cursor: "crosshair",
    background: "rgba(20,22,26,.28)",
  });

  const box = document.createElement("div");
  Object.assign(box.style, {
    position: "fixed",
    border: "2px solid #1a6ed8",
    background: "rgba(26,110,216,.14)",
    display: "none",
    pointerEvents: "none",
  });

  const hint = document.createElement("div");
  hint.textContent = "Drag a box around the question · Esc to cancel";
  Object.assign(hint.style, {
    position: "fixed",
    top: "18px",
    left: "50%",
    transform: "translateX(-50%)",
    background: "#1d1f22",
    color: "#fff",
    padding: "7px 14px",
    borderRadius: "8px",
    font: "13px -apple-system, 'Segoe UI', Roboto, sans-serif",
    pointerEvents: "none",
  });

  overlay.append(box, hint);
  document.documentElement.appendChild(overlay);

  let startX = 0;
  let startY = 0;
  let dragging = false;

  const teardown = () => {
    overlay.remove();
    document.removeEventListener("keydown", onKey);
  };

  function onKey(event) {
    if (event.key === "Escape") teardown();
  }
  document.addEventListener("keydown", onKey);

  overlay.addEventListener("mousedown", (event) => {
    dragging = true;
    startX = event.clientX;
    startY = event.clientY;
    Object.assign(box.style, { display: "block", left: `${startX}px`, top: `${startY}px`,
      width: "0px", height: "0px" });
  });

  overlay.addEventListener("mousemove", (event) => {
    if (!dragging) return;
    const left = Math.min(startX, event.clientX);
    const top = Math.min(startY, event.clientY);
    Object.assign(box.style, {
      left: `${left}px`,
      top: `${top}px`,
      width: `${Math.abs(event.clientX - startX)}px`,
      height: `${Math.abs(event.clientY - startY)}px`,
    });
  });

  overlay.addEventListener("mouseup", async (event) => {
    if (!dragging) return;
    dragging = false;
    const rect = {
      left: Math.min(startX, event.clientX),
      top: Math.min(startY, event.clientY),
      width: Math.abs(event.clientX - startX),
      height: Math.abs(event.clientY - startY),
    };
    // The overlay must be gone before the screenshot, or the capture includes the dimming
    // layer and the selection box — which the OCR model then tries to read.
    teardown();
    if (rect.width < 24 || rect.height < 24) return;

    await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));

    const shot = await chrome.runtime.sendMessage({ type: "capture" });
    if (!shot?.ok) {
      onText({ error: `Could not capture the page. ${shot?.error || ""}`.trim() });
      return;
    }
    const cropped = await cropDataUrl(shot.data.dataUrl, rect, window.devicePixelRatio || 1);
    const response = await chrome.runtime.sendMessage({
      type: "transcribe",
      payload: { dataUrl: cropped },
    });
    // Hand the raw failure up rather than a single sentence. 401, 0 and 413 are three
    // different problems with three different fixes, and collapsing them into "could not
    // read that crop" makes a signed-out user hunt for an OCR bug that isn't there.
    if (!response?.ok) {
      onText({ failure: response || { status: undefined, error: "no reply from the worker" } });
      return;
    }
    onText({ text: response.data.text, options: response.data.options || [] });
  });
}

/**
 * `captureVisibleTab` returns the image at the device pixel ratio, while the drag
 * coordinates are CSS pixels. Skipping this scale is the classic bug: on any HiDPI screen
 * the crop lands at half the intended position and the OCR reads the wrong part of the page.
 */
async function cropDataUrl(dataUrl, rect, ratio) {
  const bitmap = await createImageBitmap(await (await fetch(dataUrl)).blob());
  const canvas = document.createElement("canvas");
  canvas.width = Math.round(rect.width * ratio);
  canvas.height = Math.round(rect.height * ratio);
  const context = canvas.getContext("2d");
  context.drawImage(
    bitmap,
    Math.round(rect.left * ratio),
    Math.round(rect.top * ratio),
    canvas.width,
    canvas.height,
    0,
    0,
    canvas.width,
    canvas.height
  );
  return canvas.toDataURL("image/png");
}
