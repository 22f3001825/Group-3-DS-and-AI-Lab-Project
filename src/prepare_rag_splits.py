import json
import re
from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

# ── Topic Taxonomy ────────────────────────────────────────────────────────────
_TAXONOMY_PATH = Path(__file__).parent / "topic_taxonomy.json"
_WEEK_TOPICS: dict[int, list[str]] = {}
_TOPIC_NAME_BY_ID: dict[int, str] = {}

if _TAXONOMY_PATH.exists():
    _taxonomy_data = json.loads(_TAXONOMY_PATH.read_text(encoding="utf-8"))
    for _entry in _taxonomy_data:
        _week = _entry["week"]
        _WEEK_TOPICS.setdefault(_week, []).append(_entry["name"])
        _TOPIC_NAME_BY_ID[_entry["id"]] = _entry["name"]


def get_topic_tags(week: int) -> list[str]:
    """Return topic names for a given week from the canonical taxonomy."""
    return _WEEK_TOPICS.get(week, [])


def resolve_topic_ids(topic_ids) -> list[str]:
    """Map taxonomy topic IDs to topic *names*.

    Names, not IDs, because that is the format already baked into every chunk in the
    live collection — `chat.py` reads tags back through `find_topic`, and mixing the
    two representations in one payload field would make that lookup source-dependent.
    Resolving here rather than storing names on disk also means a taxonomy rename
    propagates on the next rebuild.
    """
    names: list[str] = []
    for tid in topic_ids or []:
        try:
            name = _TOPIC_NAME_BY_ID.get(int(tid))
        except (TypeError, ValueError):
            name = None
        if name and name not in names:
            names.append(name)
    return names


def extract_week(filepath: Path) -> int:
    """Extract week number from filepath/filename."""
    match = re.search(r'(?i)week[\s_-]*0*(\d+)', str(filepath))
    if match:
        return int(match.group(1))
    return 0

def extract_source_type(filepath: Path, base_dir: Path) -> str:
    """Extract source type (folder name inside base_dir)."""
    try:
        rel_path = filepath.relative_to(base_dir)
        return rel_path.parts[0]
    except ValueError:
        return "unknown"


# ── Frontmatter ───────────────────────────────────────────────────────────────
# Admin-authored files carry a small YAML block so that metadata asserted through the
# API survives an offline rebuild. Without it `prepare_rag_splits` would regenerate
# week-derived topic_tags and silently discard every asserted tag. Deliberately parsed
# by hand rather than with PyYAML: the schema is four scalar keys and one list, and
# adding a dependency for that would be the more surprising choice.

_FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?", re.DOTALL)


def _parse_scalar(raw: str):
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        items = [p.strip().strip("'\"") for p in raw[1:-1].split(",")]
        return [p for p in items if p]
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "'\"":
        return raw[1:-1]
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    return raw


def split_frontmatter(content: str) -> tuple[dict, str]:
    """Return (metadata, body). No frontmatter yields ({}, content) unchanged.

    None of the corpus's existing markdown carries a block, so this is a no-op for
    every file written before this feature.
    """
    match = _FRONTMATTER_RE.match(content or "")
    if not match:
        return {}, content
    meta: dict = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = _parse_scalar(value)
    return meta, content[match.end():]


def render_frontmatter(meta: dict) -> str:
    """Serialize the metadata block written above admin-authored markdown."""
    lines = ["---"]
    for key in ("week", "source_type", "content_kind", "topic_ids", "lecture_ref", "origin"):
        if key not in meta or meta[key] in (None, "", []):
            continue
        value = meta[key]
        if isinstance(value, list):
            rendered = "[" + ", ".join(str(v) for v in value) + "]"
        elif isinstance(value, int):
            rendered = str(value)
        else:
            rendered = json.dumps(str(value))
        lines.append(f"{key}: {rendered}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


# ── Chunking ──────────────────────────────────────────────────────────────────
# The single definition of what a chunk is. Called by main() below, by the preview in
# the admin ingest service, and by that service's commit — so the chunks an admin is
# shown are provably the chunks that get written. Copying this configuration anywhere
# else reintroduces the drift it exists to prevent.

_HEADERS_TO_SPLIT_ON = [
    ("#", "h1"),
    ("##", "h2"),
    ("### Timestamp:", "timestamp"),
]

_MARKDOWN_SPLITTER = MarkdownHeaderTextSplitter(
    headers_to_split_on=_HEADERS_TO_SPLIT_ON,
    strip_headers=True,
)

_TEXT_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=384,
    chunk_overlap=50,
    length_function=len,
    separators=["\n\n", "\n", " ", ""],
)


def split_document(content: str, *, week: int, source_type: str, doc_id: str,
                   topic_ids=None, origin: str | None = None):
    """Split one document into metadata-carrying chunks.

    Frontmatter (if present) supplies defaults for week / source_type / topic_ids and
    is stripped before splitting — left in, it would be embedded as if it were course
    material. Explicit arguments win over frontmatter; `topic_ids` resolve to topic
    names and fall back to the week's tags when absent, which is the behaviour every
    pre-existing file gets.
    """
    front, body = split_frontmatter(content)

    if week is None:
        week = front.get("week", 0)
    if not source_type:
        source_type = front.get("source_type", "unknown")
    if topic_ids is None:
        topic_ids = front.get("topic_ids")
    if origin is None:
        origin = front.get("origin")

    try:
        week = int(week)
    except (TypeError, ValueError):
        week = 0

    topic_tags = resolve_topic_ids(topic_ids) or get_topic_tags(week)

    md_splits = _MARKDOWN_SPLITTER.split_text(body)
    chunks = _TEXT_SPLITTER.split_documents(md_splits)

    for i, chunk in enumerate(chunks):
        chunk.metadata['week'] = week
        chunk.metadata['source_type'] = source_type
        chunk.metadata['doc_id'] = f"{doc_id}_chunk_{i}"
        chunk.metadata['topic_tags'] = topic_tags
        if origin:
            # Lets every admin contribution be found (and undone) with one filter.
            chunk.metadata['origin'] = origin
    return chunks


def main():
    root_dir = Path(__file__).parent.parent
    cleaned_dir = root_dir / 'data' / 'cleaned'
    splits_dir = root_dir / 'data' / 'splits'

    splits_dir.mkdir(parents=True, exist_ok=True)

    splits = {
        'train': [],
        'val': [],
        'test': []
    }

    total_docs_processed = 0
    total_chunks = 0

    for md_file in cleaned_dir.rglob('*.md'):
        if md_file.is_dir():
            continue

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            continue

        # Parse metadata
        week = extract_week(md_file)
        source = extract_source_type(md_file, cleaned_dir)
        doc_id = md_file.stem.replace(' ', '_')

        chunks = split_document(content, week=week, source_type=source, doc_id=doc_id)

        total_docs_processed += 1

        for chunk in chunks:
            week = chunk.metadata['week']

            # Format output dictionary
            chunk_dict = {
                'text': chunk.page_content,
                'metadata': chunk.metadata
            }

            # Leakage-Free Splitting Strategy
            if 1 <= week <= 8:
                splits['train'].append(chunk_dict)
            elif 9 <= week <= 10:
                splits['val'].append(chunk_dict)
            elif 11 <= week <= 12:
                splits['test'].append(chunk_dict)
            else:
                # Fallback to train if week is missing
                splits['train'].append(chunk_dict)
                
            total_chunks += 1

    # Save to disk as JSON Lines
    for split_name, chunk_list in splits.items():
        out_file = splits_dir / f"{split_name}_chunks.jsonl"
        with open(out_file, 'w', encoding='utf-8') as f:
            for c in chunk_list:
                f.write(json.dumps(c, ensure_ascii=False) + '\n')
                
    # Generate Split Report
    report = f"""# Chunking & Splitting Report

## Document Stats
- **Documents Processed:** {total_docs_processed}
- **Total Chunks Generated:** {total_chunks}

## Splits (Leakage-Free)
- **Train Set (Weeks 1-8):** {len(splits['train'])} chunks
- **Validation Set (Weeks 9-10):** {len(splits['val'])} chunks
- **Test Set (Weeks 11-12):** {len(splits['test'])} chunks

## Output
Saved as JSON-Lines format in `data/splits/`.
"""
    reports_dir = root_dir / 'reports'
    reports_dir.mkdir(parents=True, exist_ok=True)
    with open(reports_dir / 'chunking_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
        
    print(f"Chunking complete. Total chunks: {total_chunks}")
    print(f"Train: {len(splits['train'])}, Val: {len(splits['val'])}, Test: {len(splits['test'])}")

if __name__ == "__main__":
    main()
