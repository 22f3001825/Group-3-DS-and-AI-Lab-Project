"""
scraper_github.py
Scrapes Karthik Sir Notes directly from the GitHub repository raw files.
"""

import os
import re
import time
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import markdownify

ROOT_DIR = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT_DIR / "data" / "raw" / "notes"

def fetch_notes_from_github():
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    print("Scraping Karthik Sir Notes from GitHub...")

    for week in range(1, 13):
        week_label = f"week{week:02d}"
        out_file = NOTES_DIR / f"{week_label}_notes.md"
        
        # We know Week 6 and 7 in original didn't have content or had errors, let's try all
        url = f"https://raw.githubusercontent.com/karthik-iitm/MLT/main/Week-{week}/index.html"
        print(f"Fetching Week {week} from {url}...")
        
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 404:
                print(f"  Page not found (404).")
                continue
            resp.raise_for_status()
            
            # The page is complete HTML with math formulas
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # Extract main content - typically inside a specific div or just the body
            # GitHub Pages usually has an article or main
            main_content = soup.find("article") or soup.find("main")
            if not main_content:
                # Some presentations or custom layouts might just use body
                main_content = soup.find("body") or soup
                
            # Remove navigation and scripts
            for tag in main_content(["script", "style", "nav", "header", "footer"]):
                tag.decompose()
                
            # Convert HTML to Markdown using markdownify
            # markdownify handles headings, lists, tables, etc.
            md_content = markdownify.markdownify(
                str(main_content), 
                heading_style="ATX", 
                bullets="-",
                strip=['script', 'style']
            )
            
            # Clean up excessive blank lines
            md_content = re.sub(r'\n{3,}', '\n\n', md_content)
            
            out_file.write_text(md_content.strip(), encoding="utf-8")
            print(f"  Saved {len(md_content)} characters to {out_file.name}")
            
        except Exception as e:
            print(f"  Error fetching week {week}: {e}")
            
        time.sleep(0.5)

if __name__ == "__main__":
    fetch_notes_from_github()
