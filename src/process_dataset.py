"""
process_dataset.py
Standardizes the MLT dataset into Markdown (.md) format.
Handles PDFs using PyMuPDF4LLM with OCR fallback via Tesseract.
Preserves directory structure and outputs statistics.
"""

import os
import re
import time
import shutil
import statistics
from pathlib import Path

try:
    import fitz  # PyMuPDF
    import pymupdf4llm
except ImportError:
    fitz = None
    pymupdf4llm = None

try:
    import easyocr
    # Initialize reader once
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    EASYOCR_AVAILABLE = True
except Exception as e:
    EASYOCR_AVAILABLE = False
    print(f"Warning: EasyOCR is not available. OCR fallback will be disabled. ({e})")

# ── Paths ─────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
IMG_DIR = PROCESSED_DIR / "images"

# ── Cleaning Rules ────────────────────────────────────────────────────
def clean_markdown(text: str, is_transcript: bool = False) -> str:
    """Applies common cleaning rules to extracted Markdown."""
    # Remove standalone page numbers
    text = re.sub(r'(?m)^[\s]*\d+[\s]*$', '', text)
    
    # Remove excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    if is_transcript:
        # Extract timestamps and move them to metadata block or just remove them from flow
        # E.g., [00:03:12] or (00:03:12)
        timestamps = re.findall(r'\[\d{1,2}:\d{2}(?::\d{2})?\]|\(\d{1,2}:\d{2}(?::\d{2})?\)', text)
        
        # Remove from main text flow for clean reading
        text = re.sub(r'\[\d{1,2}:\d{2}(?::\d{2})?\]|\(\d{1,2}:\d{2}(?::\d{2})?\)', '', text)
        
        # We can append unique timestamps at the top or bottom as metadata
        unique_timestamps = sorted(list(set(timestamps)))
        if unique_timestamps:
            metadata = f"> **Video Timestamps:** {', '.join(unique_timestamps)}\n\n"
            text = metadata + text
            
    return text.strip()

# ── OCR Fallback Function ─────────────────────────────────────────────
def extract_text_ocr(pdf_path: Path) -> str:
    """Extracts text from PDF using EasyOCR (fallback)."""
    if not fitz or not EASYOCR_AVAILABLE:
        return "*OCR unavailable or skipped.*"
        
    text_content = []
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150) # High enough for OCR
        
        # Save pixmap to a temporary file for easyocr
        temp_img_path = f"temp_ocr_{page_num}.png"
        pix.save(temp_img_path)
        
        # OCR
        result = reader.readtext(temp_img_path, detail=0)
        page_text = "\n".join(result)
        text_content.append(f"## Page {page_num + 1}\n\n{page_text}")
        
        # Cleanup
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)
            
    return "\n\n".join(text_content)

# ── Processing Engine ─────────────────────────────────────────────────
def process_dataset():
    print(f"Starting dataset standardization...\nTarget Dir: {PROCESSED_DIR}")
    
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    
    stats = {
        "total_files": 0,
        "processed_files": 0,
        "total_words": 0,
        "file_sizes": [],
        "by_source": {},
        "pages_processed": 0,
        "pages_ocr": 0,
    }

    start_time = time.time()
    
    # Walk through raw directory
    for root, dirs, files in os.walk(RAW_DIR):
        current_dir = Path(root)
        source_folder = current_dir.relative_to(RAW_DIR).parts[0] if current_dir.relative_to(RAW_DIR).parts else "root"
        
        # TARGET ONLY PYQ and pq for this run
        if source_folder.lower() not in ["pyq", "pq"]:
            continue
        
        for file_name in files:
            file_path = current_dir / file_name
            ext = file_path.suffix.lower()
            
            if ext not in {".md", ".pdf", ".txt", ".json"}:
                continue
                
            stats["total_files"] += 1
            source_folder = current_dir.relative_to(RAW_DIR).parts[0] if current_dir.relative_to(RAW_DIR).parts else "root"
            stats["by_source"][source_folder] = stats["by_source"].get(source_folder, 0) + 1
            
            # Output path
            rel_path = current_dir.relative_to(RAW_DIR)
            target_dir = PROCESSED_DIR / rel_path
            target_dir.mkdir(parents=True, exist_ok=True)
            
            out_file_name = file_path.stem + ".md"
            target_file = target_dir / out_file_name
            
            is_transcript = "transcript" in source_folder.lower()
            md_text = ""
            
            print(f"Processing: {file_path.relative_to(RAW_DIR)}")
            
            try:
                if ext in {".md", ".txt"}:
                    md_text = file_path.read_text(encoding="utf-8", errors="ignore")
                    
                elif ext == ".pdf":
                    if pymupdf4llm:
                        doc = fitz.open(file_path)
                        num_pages = len(doc)
                        stats["pages_processed"] += num_pages
                        
                        # Use PyMuPDF4LLM for rich markdown extraction
                        md_text = pymupdf4llm.to_markdown(
                            doc=file_path,
                            page_chunks=False,
                            write_images=True,
                            image_path=str(IMG_DIR),
                            image_format="png"
                        )
                        
                        # --- OCR Interception for Extracted Images ---
                        if EASYOCR_AVAILABLE:
                            # Find all markdown images: ![alt](path)
                            image_tags = re.findall(r'!\[.*?\]\((.*?)\)', md_text)
                            for img_path in image_tags:
                                # img_path is like data/processed/images/file.png
                                full_img_path = Path(img_path)
                                if not full_img_path.is_absolute():
                                    full_img_path = ROOT_DIR / img_path
                                
                                if full_img_path.exists():
                                    try:
                                        print(f"    OCR'ing embedded image: {full_img_path.name}")
                                        result = reader.readtext(str(full_img_path), detail=0)
                                        ocr_text = "\n".join(result).strip()
                                        
                                        if ocr_text:
                                            replacement = f"\n\n> **[Extracted Question]**\n> {ocr_text.replace(chr(10), chr(10)+'> ')}\n\n"
                                        else:
                                            replacement = ""
                                        
                                        # Escape the img_path for regex matching
                                        img_path_escaped = re.escape(img_path)
                                        md_text = re.sub(rf'!\[.*?\]\({img_path_escaped}\)', replacement, md_text)
                                        
                                        # Cleanup image file
                                        full_img_path.unlink()
                                    except Exception as e:
                                        print(f"    OCR failed on {full_img_path.name}: {e}")
                        
                        # Fallback heuristic for whole scanned pages
                        if len(md_text.strip()) < (num_pages * 50) and EASYOCR_AVAILABLE:
                            print(f"  -> Minimal text detected. Using OCR Fallback...")
                            md_text = extract_text_ocr(file_path)
                            stats["pages_ocr"] += num_pages
                    else:
                        print("  -> PyMuPDF4LLM not available.")
                        continue
                        
                elif ext == ".json":
                    # We might skip JSONs or process them if needed, skipping for markdown standardization
                    continue
                
                # Apply Cleaning
                if md_text:
                    cleaned_text = clean_markdown(md_text, is_transcript=is_transcript)
                    target_file.write_text(cleaned_text, encoding="utf-8")
                    
                    stats["processed_files"] += 1
                    stats["total_words"] += len(cleaned_text.split())
                    stats["file_sizes"].append(target_file.stat().st_size)
                    
            except Exception as e:
                print(f"  -> Error processing {file_name}: {e}")

    # Generate Report
    print("\n" + "="*50)
    print("       DATASET STANDARDIZATION REPORT")
    print("="*50)
    print(f"Time Taken        : {time.time() - start_time:.2f} seconds")
    print(f"Files Processed   : {stats['processed_files']} / {stats['total_files']}")
    print(f"Total Words       : {stats['total_words']:,}")
    print(f"Total Pages Parsed: {stats['pages_processed']}")
    print(f"Pages OCR'd       : {stats['pages_ocr']}")
    
    if stats["file_sizes"]:
        print(f"Min File Size     : {min(stats['file_sizes']) / 1024:.2f} KB")
        print(f"Max File Size     : {max(stats['file_sizes']) / 1024:.2f} KB")
        print(f"Avg File Size     : {statistics.mean(stats['file_sizes']) / 1024:.2f} KB")
    
    print("-" * 50)
    print("Files by Source:")
    for source, count in stats["by_source"].items():
        print(f"  - {source:<20}: {count}")
    print("="*50)
    print(f"\nMarkdown files successfully generated in: {PROCESSED_DIR}")

if __name__ == "__main__":
    process_dataset()
