"""
services/notes_generator.py
────────────────────────────────────────────────────────────
Generates structured, explanation-style notes from a transcript using an LLM.
Each section's `bullets` field now holds safe-HTML explanation blocks
(heading + prose + optional derivation), not flat one-line facts.

Supports two detail levels:
  - "simple"   : Short conceptual explanations (3-5 blocks)
  - "detailed" : Deep, step-by-step tutor-style explanations with
                 derivations where relevant (5-8 blocks)
"""

import os
import re
import json
import ollama
import concurrent.futures
from typing import List, Dict
from config import Config
from services.transcript import format_timestamp

# Seconds of transcript content grouped into one notes section
SECTION_WINDOW = 300  # 5 minutes per section

# Max time to wait for a single Ollama call before giving up on that section
_OLLAMA_TIMEOUT_SECONDS = 90


def _markdown_to_safe_html(text: str) -> str:
    """
    Convert a small, controlled subset of Markdown coming back from the LLM
    into safe HTML for direct rendering with Jinja's `| safe` filter.

    Supported:
      **bold**          -> <strong>bold</strong>
      ### Heading text   -> <strong class="note-heading">Heading text</strong>
      newlines           -> <br> (paragraph breaks preserved)

    Everything else is HTML-escaped first so the LLM can never inject
    arbitrary markup, only the two patterns above are re-enabled afterward.
    """
    if not isinstance(text, str):
        text = str(text)

    # 1. Escape any raw HTML the model might have produced.
    escaped = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    # 2. Re-enable heading-style lines: either "### Something" or the
    #    "**Heading: Something**" pattern the LLM is actually asked to produce.
    def _heading_repl(m):
        return f'<strong class="note-heading">{m.group(1).strip()}</strong>'

    escaped = re.sub(r"^#{1,4}\s*(.+)$", _heading_repl, escaped, flags=re.MULTILINE)
    escaped = re.sub(r"\*\*Heading:\s*(.+?)\*\*", _heading_repl, escaped, flags=re.IGNORECASE)

    # 3. Re-enable **bold** spans.
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)

    # 4. Preserve line breaks as paragraph structure.
    escaped = escaped.replace("\r\n", "\n").strip()
    escaped = "<br>".join(line for line in escaped.split("\n") if line.strip())

    return escaped


_PREAMBLE_RE = re.compile(
    r"^(here (is|are) the .*?:|sure[!,]?\s*here.*?:|okay[!,]?\s*here.*?:|"
    r"below (is|are) .*?:)\s*",
    re.IGNORECASE,
)

_HEADING_SPLIT_RE = re.compile(r"(?=\*\*Heading:)", re.IGNORECASE)


def _strip_preamble(s: str) -> str:
    """Remove a leading 'Here is the JSON array...' style sentence some local models add."""
    return _PREAMBLE_RE.sub("", s.strip(), count=1).strip()


def _split_on_headings(content: str) -> List[str]:
    """
    Fallback for models that produce our requested '**Heading: ...**' structure
    but don't actually wrap it in valid JSON (missing quotes/commas). Splits
    directly on each heading marker and strips stray JSON leftovers
    ([, ], quotes, commas) from the edges of each block.
    """
    parts = _HEADING_SPLIT_RE.split(content)
    blocks = []
    for p in parts:
        p = p.strip()
        if not re.match(r"^\*\*heading", p, re.IGNORECASE):
            continue  # drop preamble/junk before the first heading marker
        p = re.sub(r'^[\[\s"]+', "", p)
        p = re.sub(r'[\]\s",]+$', "", p)
        if p:
            blocks.append(p)
    return blocks


_FILLER_LINE_RE = re.compile(
    r"^(let me know.*|i hope this helps.*|hope (this|that) helps.*|"
    r"feel free to ask.*|if you have any questions.*|is there anything else.*|"
    r"please let me know.*)$",
    re.IGNORECASE,
)


def _strip_trailing_filler(block: str) -> str:
    """
    Remove conversational sign-off lines the LLM sometimes tacks onto a block
    (e.g. "Let me know if you'd like me to explain anything further!"),
    which read fine in a chat but don't belong in generated notes.
    """
    lines = block.split("\n")
    while lines and _FILLER_LINE_RE.match(lines[-1].strip()):
        lines.pop()
    return "\n".join(lines).strip()


def _extract_note_blocks(raw_content: str) -> List[str]:
    """
    Turn the raw LLM response into a list of explanation-block strings,
    tolerating the quirks small local models commonly produce:
      - a leading preamble sentence ("Here is the JSON array...")
      - literal newlines inside JSON string values (not escaped as \\n)
      - markdown code fences around the JSON
      - a response truncated mid-array (hit the token limit)
      - skipping JSON structure entirely and just emitting raw
        '**Heading: ...**' blocks with no quotes/commas/brackets

    Falls back to treating the raw text as plain prose blocks if none of
    the above apply, so the user always sees something readable instead of
    a parser error.
    """
    content = raw_content.strip()
    content = content.replace("```json", "").replace("```", "").strip()
    content = _strip_preamble(content)

    start = content.find("[")
    end = content.rfind("]") + 1
    json_candidate = content[start:end] if (start != -1 and end > start) else content

    # Attempt 1: strict=False tolerates raw control characters (literal
    # newlines) inside string values, which local models frequently emit
    # even when asked to use \n.
    try:
        blocks = json.loads(json_candidate, strict=False)
        if isinstance(blocks, list) and blocks:
            return [str(b) for b in blocks]
    except Exception:
        pass

    # Attempt 2: response was likely truncated before the closing "]".
    # Repair by dropping back to the last complete string element and
    # closing the array there.
    if start != -1:
        truncated = content[start:]
        last_quote_pair = truncated.rfind('",')
        if last_quote_pair != -1:
            repaired = truncated[: last_quote_pair + 1] + "]"
            try:
                blocks = json.loads(repaired, strict=False)
                if isinstance(blocks, list) and blocks:
                    return [str(b) for b in blocks]
            except Exception:
                pass

    # Attempt 3: the model produced our requested "**Heading: ...**"
    # structure but not valid JSON at all (no quotes/commas around
    # elements). Split directly on the heading markers we asked for.
    heading_blocks = _split_on_headings(content)
    if heading_blocks:
        return heading_blocks

    # Attempt 4: give up on structure entirely and treat blank-line-separated
    # chunks of the raw response as blocks, so the note isn't just an error.
    plain = content.strip().strip("[]").strip()
    chunks = [c.strip().strip('",').strip() for c in re.split(r"\n\s*\n", plain) if c.strip()]
    if chunks:
        return chunks

    return ["Notes could not be generated for this section — the AI response was empty or malformed."]


def _generate_notes_with_llm(text: str, detail_level: str = "simple") -> List[str]:
    """
    Call the configured LLM to turn a transcript segment into explanation-style
    notes (headings + prose + derivations), NOT flat one-line bullet facts.

    Returns a list of HTML-safe strings, each one a self-contained explanation
    block (roughly one concept per block).

    detail_level: "simple" for concise conceptual explanations,
                  "detailed" for deep, step-by-step tutor-style walkthroughs.
    """
    if detail_level == "detailed":
        detail_instruction = (
            "Write like a patient tutor walking a student through the material step by step. "
            "For each of the 5 to 8 key ideas in this segment, produce ONE block that:\n"
            "  - Starts with a short bolded heading naming the concept, e.g. **Heading: <name>**\n"
            "  - Then explains the concept in 2-5 full sentences of flowing prose (not fragments).\n"
            "  - Bold the important key terms inline using **term**.\n"
            "  - If a formula, equation, or mathematical relationship is mentioned, include a "
            "'**Derivation:**' sub-part that walks through the variables and the reasoning "
            "step by step, in plain sentences (you may use simple inline notation like w^2 or x_i).\n"
            "  - End with why the idea matters or what it connects to next, when relevant.\n"
            "Each block should read like a short tutor explanation, not a list of facts."
        )
    else:
        detail_instruction = (
            "Write like a tutor giving a quick, clear explanation of each key idea. "
            "For each of the 3 to 5 key ideas in this segment, produce ONE block that:\n"
            "  - Starts with a short bolded heading naming the concept, e.g. **Heading: <name>**\n"
            "  - Then explains it in 1-3 full sentences of plain prose (not a one-line fact).\n"
            "  - Bold the important key terms inline using **term**.\n"
            "  - Only include a brief '**Derivation:**' sub-part if the segment explicitly gives "
            "a formula or equation; otherwise skip it entirely.\n"
            "Keep each block concise but written as real explanation, not a bullet fragment."
        )

    prompt = f"""You are an expert tutor for IIT Madras Data Science students, explaining a lecture segment to a student who wants to actually understand it, not just memorize facts.
{detail_instruction}

Return ONLY a valid JSON array of strings, where each string is one explanation block as described above (use \\n for paragraph breaks within a block if needed). No extra text, no preamble, no markdown code fences, and no conversational remarks, sign-offs, or offers to help further (e.g. do NOT add things like "Let me know if you have questions").

Transcript Segment: {text}
"""

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                ollama.chat,
                model=Config.OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}],
                options={
                    # The explanation-style format is much longer than short bullets,
                    # so give the model enough headroom to finish the full JSON array
                    # instead of getting cut off mid-response.
                    "num_predict": 2048,
                    "temperature": 0.4,
                },
            )
            response = future.result(timeout=_OLLAMA_TIMEOUT_SECONDS)
        content = response["message"]["content"].strip()
        blocks = _extract_note_blocks(content)
        blocks = [_strip_trailing_filler(b) for b in blocks]
        blocks = [b for b in blocks if b.strip()]
        if not blocks:
            blocks = ["Notes could not be generated for this section — the AI response was empty."]
        # Convert each block's Markdown-ish content to safe HTML for direct rendering.
        return [_markdown_to_safe_html(b) for b in blocks]
    except concurrent.futures.TimeoutError:
        return [
            f"⚠️ The AI backend timed out while generating {detail_level} notes for this "
            f"section (limit: {_OLLAMA_TIMEOUT_SECONDS}s). Try regenerating, or check that "
            f"Ollama is running and responsive."
        ]
    except Exception as e:
        return [f"Error generating {detail_level} notes: {str(e)}"]


def generate_notes(transcript: dict, video_id: str, detail_level: str = "simple") -> dict:
    """
    Build structured notes from a transcript dict.

    Returns:
    {
        "video_id": str,
        "title": str,
        "detail_level": str,
        "total_duration": str,   # e.g. "42:15"
        "sections": [
            {
                "section_num": int,
                "title": str,
                "timestamp": str,
                "start_time": float,
                "end_time": float,
                "bullets": List[str],
                "full_text": str,
            },
            ...
        ]
    }
    """
    segments = transcript.get("segments", [])
    if not segments:
        return {
            "video_id": video_id,
            "title": "Lecture Notes",
            "detail_level": detail_level,
            "total_duration": "00:00",
            "sections": [],
        }

    total_duration = segments[-1]["start"] + segments[-1].get("duration", 0)
    total_duration_str = format_timestamp(total_duration)

    sections = []
    window_start = 0.0
    window_num = 1

    while window_start < total_duration:
        window_end = window_start + SECTION_WINDOW
        window_segs = [s for s in segments if window_start <= s["start"] < window_end]

        if window_segs:
            full_text = " ".join(s["text"] for s in window_segs)

            # LLM-generated notes at the requested detail level
            bullets = _generate_notes_with_llm(full_text, detail_level=detail_level)

            # Use first ~8 words of the section as its title
            first_line = " ".join(full_text.split()[:8]).strip(".,;:")
            sections.append(
                {
                    "section_num": window_num,
                    "title": first_line or f"Section {window_num}",
                    "timestamp": format_timestamp(window_start),
                    "start_time": window_start,
                    "end_time": min(window_end, total_duration),
                    "bullets": bullets,
                    "full_text": full_text,
                }
            )
            window_num += 1
        window_start = window_end

    return {
        "video_id": video_id,
        "title": f"Lecture Notes — {video_id}",
        "detail_level": detail_level,
        "total_duration": total_duration_str,
        "sections": sections,
    }