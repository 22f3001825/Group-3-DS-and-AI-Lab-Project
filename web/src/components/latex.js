/** Course content is written in LaTeX, but not in the dialect remark-math reads.
 *
 *  Measured over the live bank: 103 units carry `\[ ... \]` display math and 100 carry
 *  `\(...\)` inline math, all from `faq`; remark-math understands `$$...$$` and `$...$`
 *  and neither of the others. So the text arrives valid and renders as source until it
 *  is translated — which is why this is a UI fix and not a re-ingest.
 *
 *  Order matters, three times over:
 *
 *  1. Pre-existing dollar signs are escaped FIRST, before any of ours exist. Five units
 *     (one `pq`, four OCR'd `PYQ`) contain a bare `$`, and an odd number of them would
 *     otherwise open a math span that swallows the rest of the paragraph. Escaping first
 *     means every `$` remaining afterwards is one this function put there.
 *  2. Display before inline: `\[` and `\(` are distinct tokens, but a `\[` left for the
 *     inline pass would still match its own closing `\]` and come out as inline math.
 *  3. The `$$` fences go on their own lines. remark-math only treats `$$` as BLOCK math
 *     when it opens a line — written as `$$x$$` on one line it parses as inline, and the
 *     formula renders mid-sentence at body size instead of centred on its own row.
 *
 *  Lives in its own module rather than beside the component so the component file exports
 *  only a component (react-refresh wants that) and so this stays testable on its own.
 */
export function latexToMarkdown(text) {
  if (!text) return '';
  return String(text)
    .replace(/\$/g, '\\$')
    .replace(/\\\[([\s\S]*?)\\\]/g, (_, body) => `\n\n$$\n${body.trim()}\n$$\n\n`)
    .replace(/\\\(([\s\S]*?)\\\)/g, (_, body) => `$${body.trim()}$`);
}
