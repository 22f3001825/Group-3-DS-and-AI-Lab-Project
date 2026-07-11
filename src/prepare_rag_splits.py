import json
import re
from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

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

def main():
    root_dir = Path(__file__).parent.parent
    cleaned_dir = root_dir / 'data' / 'cleaned'
    splits_dir = root_dir / 'data' / 'splits'
    
    splits_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Setup LangChain Splitters
    # Split on headers and our custom Timestamp headers
    headers_to_split_on = [
        ("#", "h1"),
        ("##", "h2"),
        ("### Timestamp:", "timestamp")
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=True
    )
    
    # Text splitter for chunks that are too long
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=384,
        chunk_overlap=50,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
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
        
        # Split markdown structurally
        md_splits = markdown_splitter.split_text(content)
        
        # Split further by length
        chunks = text_splitter.split_documents(md_splits)
        
        total_docs_processed += 1
        
        for i, chunk in enumerate(chunks):
            # Inject global metadata
            chunk.metadata['week'] = week
            chunk.metadata['source_type'] = source
            chunk.metadata['doc_id'] = f"{doc_id}_chunk_{i}"
            
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
