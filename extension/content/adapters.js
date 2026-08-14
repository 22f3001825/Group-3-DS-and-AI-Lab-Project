/**
 * content/adapters.js — turning a selection into a question stem plus its options.
 *
 * A student highlights the question text; the answer choices are usually *next to* the
 * selection rather than inside it. Recovering them matters because `/socratic/analyze`
 * uses the options to sharpen the concept match, and because the panel can then show what
 * was on offer.
 *
 * Hostname-keyed adapters override the generic path. The generic path is the one that has
 * to work: portal markup changes without notice, and an unknown quiz page must still be
 * usable rather than silently producing a stem with no options.
 */

const OPTION_PATTERN = /^\s*(\(?[a-eA-E][).]|[1-5][).])\s+\S/;

/** Walk up from the selection to the nearest block that looks like a whole question. */
function questionBlock(node) {
  let element = node?.nodeType === Node.TEXT_NODE ? node.parentElement : node;
  for (let depth = 0; element && depth < 8; depth += 1) {
    const text = (element.innerText || "").trim();
    // A question block is one that contains both a stem and at least two option-shaped
    // lines. Stopping at the first ancestor with *any* list would grab a nav menu.
    if (text.length > 40) {
      const optionCount = text
        .split("\n")
        .filter((line) => OPTION_PATTERN.test(line)).length;
      if (optionCount >= 2) return element;
    }
    element = element.parentElement;
  }
  return null;
}

function splitStemAndOptions(text) {
  const lines = (text || "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
  const stem = [];
  const options = [];
  for (const line of lines) {
    if (OPTION_PATTERN.test(line) && line.length < 300) options.push(line);
    else if (!options.length) stem.push(line);
  }
  return { stem: stem.join(" "), options };
}

const ADAPTERS = {
  /**
   * Seek renders each option as its own labelled row, so the option text does not carry
   * an "(a)" prefix and the generic line test cannot see it.
   */
  "seek.onlinedegree.iitm.ac.in": (selection, range) => {
    const block = range?.commonAncestorContainer?.parentElement?.closest(
      "[data-testid*='question'], .question, article"
    );
    if (!block) return null;
    const options = Array.from(
      block.querySelectorAll("label, [role='radio'], li")
    )
      .map((el) => (el.innerText || "").trim())
      .filter((text) => text && text.length < 300);
    if (!options.length) return null;
    return { stem: selection, options: options.slice(0, 8) };
  },
};

export function extractQuestion() {
  const selection = window.getSelection();
  const selected = (selection?.toString() || "").trim();
  if (!selected) return null;

  const range = selection.rangeCount ? selection.getRangeAt(0) : null;

  const adapter = ADAPTERS[window.location.hostname];
  if (adapter) {
    try {
      const result = adapter(selected, range);
      if (result?.stem) return { ...result, via: window.location.hostname };
    } catch {
      // An adapter that throws on changed markup must not take the feature with it.
    }
  }

  // If the highlight already contains the options, use it verbatim — the student told us
  // what the question is, and second-guessing that is how you end up sending a nav bar.
  const inline = splitStemAndOptions(selected);
  if (inline.options.length >= 2) return { ...inline, via: "selection" };

  const block = questionBlock(range?.commonAncestorContainer);
  if (block) {
    const fromBlock = splitStemAndOptions(block.innerText);
    if (fromBlock.options.length >= 2) {
      return { stem: selected || fromBlock.stem, options: fromBlock.options, via: "block" };
    }
  }

  return { stem: selected, options: [], via: "bare" };
}
