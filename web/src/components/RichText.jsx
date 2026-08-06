import React, { useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { latexToMarkdown } from './latex';
import './RichText.css';

/** Markdown + LaTeX, themed and overflow-safe. One renderer for every piece of course
 *  content on the site — question units, chat answers, quiz questions and explanations —
 *  because they all come from the same corpus and so carry the same notation.
 *
 *  `inline` drops the block spacing and the paragraph wrapper, for a title or an option
 *  that has to stay on one line. It is the same component either way: a title carries the
 *  same `\(...\)` a body does.
 */
export default function RichText({ children, className = '', inline = false }) {
  const source = useMemo(() => latexToMarkdown(children), [children]);
  if (!source) return null;
  return (
    <div className={`rich-text ${inline ? 'rich-inline' : ''} ${className}`.trim()}>
      <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
        {source}
      </ReactMarkdown>
    </div>
  );
}
