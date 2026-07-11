import os
from pathlib import Path
import re

def clean_markdown_content(text: str) -> tuple[str, dict]:
    stats = {
        'hyphens_merged': 0,
        'timestamps_removed': 0,
        'duplicate_headers_removed': 0,
        'unicode_fixes': 0
    }
    
    # 1. OCR Post-processing
    # Fix OCR hyphenation splitting words across lines (e.g., classi- \n fication)
    # Only applies to alphabetical characters to prevent breaking math equations like "x - \n y"
    text = re.sub(r'([a-zA-Z])-\s*\n\s*([a-zA-Z])', r'\1\2', text)
    
    # Remove PyMuPDF picture text HTML comments
    text = re.sub(r'<!--\s*Start of picture text\s*-->', '', text)
    text = re.sub(r'<!--\s*End of picture text\s*-->', '', text)
    
    # Convert <br> tags to actual newlines for math matrices
    text = re.sub(r'<br\s*/?>', '\n', text)
    
    # Normalize excessive newlines (collapse 3+ into 2)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Fix specific OCR unicode artifacts
    if 'we?Tll' in text:
        stats['unicode_fixes'] += text.count('we?Tll')
        text = text.replace('we?Tll', "we'll")
        
    # 2. Transcript Cleaning (Timestamps)
    # Convert "(Refer Slide Time: 01:01)" to "\n### Timestamp: 01:01\n"
    timestamp_pattern = re.compile(r'\(Refer Slide Time: (\d{2}:\d{2})\)')
    stats['timestamps_removed'] = len(timestamp_pattern.findall(text))
    text = timestamp_pattern.sub(r'\n\n### Timestamp: \1\n\n', text)
    
    # Convert timestamps like [00:03:12] to headers
    bracket_timestamp_pattern = re.compile(r'\[(\d{2}:\d{2}:\d{2})\]')
    stats['timestamps_removed'] += len(bracket_timestamp_pattern.findall(text))
    text = bracket_timestamp_pattern.sub(r'\n\n### Timestamp: \1\n\n', text)

    # 3. Boilerplate removal
    # Remove page numbers like "Page 1 of 12"
    text = re.sub(r'(?i)Page \d+ of \d+', '', text)
    # Remove standalone "Page X" on a line
    text = re.sub(r'(?m)^Page \d+$', '', text)
    
    # Remove duplicate section titles (e.g., ## Practice\n## Practice)
    dup_header_pattern = re.compile(r'^(#+ .*\n)(?:\1)+', flags=re.MULTILINE)
    stats['duplicate_headers_removed'] = len(dup_header_pattern.findall(text))
    text = dup_header_pattern.sub(r'\1', text)
    
    # 4. Whitespace Normalization
    # Remove trailing spaces
    text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)
    # Collapse multiple blank lines into a single blank line
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip(), stats

def main():
    root_dir = Path(__file__).parent.parent
    processed_dir = root_dir / 'data' / 'processed'
    cleaned_dir = root_dir / 'data' / 'cleaned'
    reports_dir = root_dir / 'reports'
    
    cleaned_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    report_data = {
        'total_processed': 0,
        'empty_dropped': 0,
        'files_skipped': 0,
        'total_hyphens_merged': 0,
        'total_timestamps_removed': 0,
        'total_duplicate_headers': 0,
        'total_unicode_fixes': 0
    }
    
    for md_file in processed_dir.rglob('*.md'):
        if md_file.is_dir():
            continue
            
        report_data['total_processed'] += 1
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            cleaned_content, stats = clean_markdown_content(content)
            
            if not cleaned_content:
                report_data['empty_dropped'] += 1
                continue
                
            # Aggregate stats
            report_data['total_hyphens_merged'] += stats['hyphens_merged']
            report_data['total_timestamps_removed'] += stats['timestamps_removed']
            report_data['total_duplicate_headers'] += stats['duplicate_headers_removed']
            report_data['total_unicode_fixes'] += stats['unicode_fixes']
            
            # Preserve hierarchy
            rel_path = md_file.relative_to(processed_dir)
            out_path = cleaned_dir / rel_path
            out_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
                
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
            report_data['files_skipped'] += 1

    # Generate Report
    report_md = f"""# Document Cleaning Report

## Overview
- **Total Documents Processed:** {report_data['total_processed']}
- **Empty Documents Dropped:** {report_data['empty_dropped']}
- **Files Skipped (Errors):** {report_data['files_skipped']}
- **Total Successfully Cleaned:** {report_data['total_processed'] - report_data['empty_dropped'] - report_data['files_skipped']}

## Cleaning Metrics
- **OCR Hyphenations Merged:** {report_data['total_hyphens_merged']}
- **Timestamps Removed:** {report_data['total_timestamps_removed']}
- **Duplicate Headers Removed:** {report_data['total_duplicate_headers']}
- **Unicode Corruptions Fixed:** {report_data['total_unicode_fixes']}

*This report was automatically generated by `src/clean_dataset.py`.*
"""
    
    with open(reports_dir / 'document_cleaning_report.md', 'w', encoding='utf-8') as f:
        f.write(report_md)
        
    print(f"Dataset successfully cleaned. Saved to {cleaned_dir}")
    print(f"Report saved to {reports_dir / 'document_cleaning_report.md'}")

if __name__ == "__main__":
    main()
