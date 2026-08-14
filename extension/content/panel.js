/**
 * content/panel.js — the overlay.
 *
 * **There is no answer-rendering component in this file, and that is the point.** It
 * renders a concept, lecture segments, a guiding question, hints and attempt feedback.
 * If the server ever sent a field containing a solution, there is no code path that would
 * put it on screen. That is the client-side half of L1/L3 — the policy does not depend on
 * the panel behaving, but the panel is built so that misbehaving is not expressible.
 *
 * Rendered into a **shadow root** so the portal's CSS cannot reach in and the panel's
 * cannot leak out. Every insertion goes through `textContent`, never `innerHTML`, so page
 * content and model output cannot inject markup into the extension's own DOM.
 */

const PANEL_ID = "mlt-socratic-root";

function send(type, payload = {}) {
  return chrome.runtime.sendMessage({ type, payload });
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined && text !== null) node.textContent = String(text);
  return node;
}

export class Panel {
  constructor() {
    this.host = null;
    this.root = null;
    this.session = null;
    this.build();
  }

  build() {
    if (document.getElementById(PANEL_ID)) {
      this.host = document.getElementById(PANEL_ID);
      this.root = this.host.shadowRoot;
      return;
    }
    this.host = el("div");
    this.host.id = PANEL_ID;
    this.root = this.host.attachShadow({ mode: "open" });

    const style = el("style");
    style.textContent = PANEL_CSS;
    this.root.appendChild(style);

    this.panel = el("div", "panel");
    this.root.appendChild(this.panel);
    document.documentElement.appendChild(this.host);
  }

  clear() {
    this.panel.replaceChildren();
  }

  header() {
    const bar = el("div", "bar");
    bar.appendChild(el("span", "title", "MLT Companion"));
    const close = el("button", "close", "×");
    close.addEventListener("click", () => this.hide());
    bar.appendChild(close);
    return bar;
  }

  show() {
    this.host.style.display = "block";
  }

  hide() {
    this.host.style.display = "none";
  }

  message(text, action) {
    this.clear();
    this.panel.appendChild(this.header());
    this.panel.appendChild(el("p", "msg", text));
    if (action) {
      const button = el("button", "primary", action.label);
      button.addEventListener("click", action.onClick);
      this.panel.appendChild(button);
    }
    this.show();
  }

  loading(text = "Reading the lectures…") {
    this.message(text);
  }

  /** The main view. `data` is the /socratic/analyze response. */
  render(data) {
    this.session = data.session_id;
    this.clear();
    this.panel.appendChild(this.header());

    if (data.concept) {
      const concept = el("div", "concept");
      concept.appendChild(el("div", "concept-name", data.concept.name));
      if (data.concept.week) {
        concept.appendChild(el("div", "meta", `Week ${data.concept.week}`));
      }
      if (data.why_this_concept) {
        concept.appendChild(el("p", "why", data.why_this_concept));
      }
      this.panel.appendChild(concept);
    }

    // The no-coverage state is a first-class outcome, not an error. Week 6 (Ridge, LASSO,
    // Regularization) has no transcripts at all, so every selection there lands here —
    // saying so plainly beats an empty list that reads as a broken panel.
    //
    // `retrieval_unavailable` is the other empty-segment case and must not borrow that
    // wording: it means the lecture index could not be searched, which is a deployment
    // fault, not a statement about what the course covers.
    if (data.coverage === "retrieval_unavailable") {
      this.panel.appendChild(
        el("p", "nocoverage", "Lecture search is unavailable right now, so no segments could be looked up. The concept and the question below still apply.")
      );
    } else if (data.coverage === "no_transcript") {
      this.panel.appendChild(
        el("p", "nocoverage", "No lecture recording covers this topic, so there is no segment to point you at. The concept and the question below still apply.")
      );
    } else if (data.segments?.length) {
      this.panel.appendChild(el("div", "label", "Watch"));
      for (const segment of data.segments) {
        this.panel.appendChild(this.segmentCard(segment));
      }
    }

    if (data.guiding_question) {
      const box = el("div", "guiding");
      box.appendChild(el("div", "label", "Think about this"));
      box.appendChild(el("p", "question", data.guiding_question));
      this.panel.appendChild(box);
    }

    // `watch_out_for` and `related_questions` are still produced and still guarded server
    // side — they feed the policy harness and the L4 denylist respectively — but neither
    // is rendered. The card is a concept, a segment and one question to think about; the
    // common-mistake line and the neighbour list were reading as more to get through.
    this.panel.appendChild(this.actions(data));

    if (data.policy?.source === "deterministic") {
      this.panel.appendChild(
        el("p", "degraded", "Generated guidance was unavailable, so this card was built from the course outline.")
      );
    }
    this.show();
  }

  segmentCard(segment) {
    const card = el("div", "segment");
    const range =
      segment.start && segment.end
        ? `${segment.start}–${segment.end}`
        : segment.start
        ? `from ${segment.start}`
        : "";
    card.appendChild(el("div", "segment-title", segment.title));
    card.appendChild(
      el("div", "meta", [`Week ${segment.week}`, range].filter(Boolean).join(" · "))
    );
    if (segment.description) {
      card.appendChild(el("p", "segment-desc", segment.description));
    }
    if (segment.deep_link) {
      const link = el("a", "watch-link", "Watch this part →");
      link.href = segment.deep_link;
      link.target = "_blank";
      link.rel = "noreferrer noopener";
      card.appendChild(link);
    }
    return card;
  }

  actions(data) {
    const row = el("div", "actions");

    const hint = el("button", "secondary", "Another hint");
    hint.addEventListener("click", async () => {
      hint.disabled = true;
      const response = await send("hint", { sessionId: this.session });
      hint.disabled = false;
      if (response.ok) {
        this.panel.insertBefore(
          el("p", "hint", `Hint ${response.data.hint_level}: ${response.data.hint}`),
          row
        );
        if (response.data.hint_level >= (data.max_hint_level || 3)) hint.remove();
      } else if (response.status === 409) {
        const detail = response.data?.detail || {};
        this.panel.insertBefore(el("p", "hint", detail.message || "No further hints."), row);
      }
    });
    row.appendChild(hint);

    const attempt = el("button", "primary", "Check my reasoning");
    attempt.addEventListener("click", () => this.attemptForm(row));
    row.appendChild(attempt);
    return row;
  }

  attemptForm(anchor) {
    if (this.panel.querySelector(".attempt-form")) return;
    const form = el("div", "attempt-form");
    const box = el("textarea");
    box.placeholder = "Write out your reasoning — not just the answer.";
    form.appendChild(box);

    const submit = el("button", "primary", "Review it");
    submit.addEventListener("click", async () => {
      const text = box.value.trim();
      if (!text) return;
      submit.disabled = true;
      submit.textContent = "Reviewing…";
      const response = await send("attempt", {
        sessionId: this.session,
        studentAnswer: text,
      });
      submit.disabled = false;
      submit.textContent = "Review it";
      if (response.ok) this.renderFeedback(form, response.data);
      else if (response.status === 503) {
        form.appendChild(el("p", "degraded", "No reviewer is reachable right now — your attempt was not lost. Try again shortly."));
      } else {
        form.appendChild(el("p", "degraded", "Could not review that attempt."));
      }
    });
    form.appendChild(submit);
    this.panel.insertBefore(form, anchor.nextSibling);
  }

  renderFeedback(form, data) {
    const existing = form.querySelector(".feedback");
    if (existing) existing.remove();
    const box = el("div", "feedback");
    // `needs_reasoning` deliberately has no badge. The other three describe the reasoning
    // that was reviewed; this one means none was, so a badge here would be read as a
    // verdict on the answer the student just typed — which is the one thing the server
    // took care not to give them.
    const labels = {
      on_track: "On track",
      partially_correct: "Partly there",
      off_track: "Off track",
    };
    if (labels[data.verdict]) {
      box.appendChild(el("div", "verdict", labels[data.verdict]));
    }
    if (data.first_error) box.appendChild(el("p", null, `First slip: ${data.first_error}`));
    if (data.why) box.appendChild(el("p", null, data.why));
    if (data.concept_to_revisit) {
      box.appendChild(el("p", "meta", `Revisit: ${data.concept_to_revisit}`));
    }
    if (data.next_guiding_question) {
      box.appendChild(el("p", "question", data.next_guiding_question));
    }
    form.appendChild(box);
  }
}

const PANEL_CSS = `
:host { all: initial; }
.panel {
  position: fixed; top: 16px; right: 16px; width: 380px; max-height: 85vh; overflow-y: auto;
  z-index: 2147483647; background: #fff; color: #1a1a1a; border: 1px solid #d8d8d8;
  border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,.18); padding: 14px 16px 18px;
  font: 14px/1.5 -apple-system, "Segoe UI", Roboto, sans-serif;
}
.bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.title { font-weight: 600; font-size: 12px; letter-spacing: .06em; text-transform: uppercase; opacity: .6; }
.close { background: none; border: 0; font-size: 20px; cursor: pointer; color: inherit; opacity: .6; }
.label { font-size: 11px; letter-spacing: .06em; text-transform: uppercase; opacity: .55; margin: 12px 0 4px; }
.concept-name { font-size: 17px; font-weight: 650; }
.meta { font-size: 12px; opacity: .65; }
.why { font-size: 13px; opacity: .85; margin: 6px 0 0; }
.nocoverage { font-size: 13px; opacity: .8; background: rgba(180,140,20,.10); padding: 9px 11px; border-radius: 8px; margin: 10px 0 0; }
.segment { border: 1px solid #e6e6e6; border-radius: 9px; padding: 10px 12px; margin-bottom: 8px; background: #fafafa; }
.segment-title { font-weight: 600; font-size: 14px; }
.segment-desc { font-size: 13px; margin: 6px 0 0; opacity: .9; }
.watch-link { display: inline-block; margin-top: 7px; font-size: 13px; color: #1a6ed8; text-decoration: none; font-weight: 550; }
/* Light surface, so the text colour is stated rather than inherited. \`color: inherit\`
   here is what put near-white text on this near-white box for anyone whose browser is in
   dark mode: the panel's own colour flipped, the box's background did not. Same story for
   the textarea below. Both stay light in both themes — the readable pairing is the point,
   not matching the surrounding chrome. */
.guiding { border-left: 3px solid #1a6ed8; padding: 8px 12px; margin: 14px 0 0; background: #f6f9ff; color: #14181f; border-radius: 0 8px 8px 0; }
.question { font-size: 14px; font-weight: 550; margin: 2px 0 0; }
.hint { font-size: 13px; background: rgba(26,110,216,.09); padding: 9px 11px; border-radius: 8px; margin: 10px 0 0; }
.actions { display: flex; gap: 8px; margin-top: 14px; }
button.primary, button.secondary {
  flex: 1; padding: 8px 10px; border-radius: 8px; font-size: 13px; font-weight: 550; cursor: pointer;
  font-family: inherit;
}
button.primary { background: #1a6ed8; color: #fff; border: 1px solid #1a6ed8; }
button.secondary { background: transparent; color: inherit; border: 1px solid currentColor; opacity: .75; }
button:disabled { opacity: .5; cursor: default; }
.attempt-form { margin-top: 12px; display: flex; flex-direction: column; gap: 8px; }
.attempt-form textarea {
  width: 100%; min-height: 88px; padding: 8px; border-radius: 8px; border: 1px solid #bbb;
  font: inherit; color: #111; background: #fff; resize: vertical; box-sizing: border-box;
}
.attempt-form textarea::placeholder { color: #6b7280; opacity: 1; }
.feedback { border-top: 1px solid #e0e0e0; padding-top: 10px; font-size: 13px; }
.verdict { font-weight: 650; margin-bottom: 4px; }
.degraded { font-size: 12px; opacity: .65; margin-top: 10px; font-style: italic; }
.msg { font-size: 13px; }

/* Last in the sheet on purpose. These rules and the component rules above have the same
   specificity, so source order decides — a dark block placed before them (as it was) is
   overridden by every background it is trying to replace. */
@media (prefers-color-scheme: dark) {
  .panel { background: #1d1f22; color: #e9e9ea; border-color: #34363a; }
  .segment { background: #26282c; border-color: #3a3d42; }
  .feedback { border-top-color: #3a3d42; }
}
`;
