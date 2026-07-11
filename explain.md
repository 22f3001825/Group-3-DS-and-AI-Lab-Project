# How We Built the Dataset Pipeline (A Guide for the Team)

Hey team! If you are wondering how we went from a messy pile of PDFs and forum posts to a perfectly clean, machine-learning-ready dataset for Milestone 2, this document tells the complete story. 

I've written this in simple language so everyone is on the same page about what technologies we used, what mistakes we made, how we fixed them, and how the final data is structured.

---

## 1. Gathering the Raw Data (Scraping)
Before we could do anything, we needed the official CS2007 course materials. We wrote automated scrapers to pull this together:
- **Discourse FAQs**: We scraped the weekly Q&A threads directly from the forum as HTML.
- **Kartik Sir's Notes**: We scraped the instructor's GitHub pages directly into Markdown.
- **PDFs**: We manually downloaded the lecture transcripts, Practice Questions (PQs), and Previous Year Questions (PYQs).

*All of this raw, untouched data lives in the `data/raw/` folder.*

## 2. Standardizing Everything to Markdown
To make our AI smart, we needed all of this data in a single, unified format. We chose **Markdown** (`.md`) because it preserves structure (like headers and bullet points) which Large Language Models (LLMs) easily understand.

We used a library called **`pymupdf4llm`** to convert all the PDFs (transcripts and PQs) into Markdown text. For standard text, it worked beautifully. But we immediately hit a massive roadblock with the PYQs...

## 3. The OCR Nightmare: Tesseract vs. EasyOCR
The Previous Year Questions (PYQs) contained heavily formatted mathematical equations and fill-in-the-blank questions. When the PDF converter tried to read them, it just output blank spaces or junk HTML comments like `<!-- Start of picture text -->`. It completely destroyed the questions!

**Attempt 1: Tesseract OCR**
We first tried using `pytesseract` to read the images of the math equations. It performed horribly. The math symbols confused it, the resolution was bad, and it just couldn't recover the text cleanly.

**Attempt 2: EasyOCR (The Winner)**
We ripped out Tesseract and completely rewrote the extraction pipeline (`src/process_dataset.py`) to use **EasyOCR**. EasyOCR uses deep learning and performed *flawlessly*. It looked at the images of the math equations and successfully converted them back into text. (We had a brief crash on Windows due to a `cp1252` encoding bug, but we fixed it by forcing everything into `utf-8`).

*The successfully extracted Markdown files were saved to `data/processed/`.*

## 4. Cleaning the Data (And Fixing a Major Mistake!)
Next, we needed to clean the text (`src/clean_dataset.py`). 

When a PDF reaches the right edge of a page, it often splits words with a hyphen (e.g., `classi- \n fication`). We wrote a Regular Expression (Regex) to merge these back into `classification`. However, we were very careful to only apply this to alphabetical letters (`[a-zA-Z]`), so we didn't accidentally delete the minus sign in a math equation like `x - y`!

**The Big Mistake:**
In the lecture transcripts, the instructor often says *"Refer Slide Time: 01:01"*. In our first cleaning pass, we aggressively deleted these timestamps because they looked like clutter. 
But we suddenly realized: *Wait! If we delete the timestamps, our final RAG app won't be able to give students clickable video links!* 

**The Fix:**
We rewrote the cleaning script. Instead of deleting the timestamps, we safely converted them into Markdown headers: `### Timestamp: 01:01`. You'll see why in the next step.

*The perfectly cleaned files were saved to `data/cleaned/`.*

## 5. Chunking and Metadata (LangChain)
LLMs cannot read 100 pages of text at once; they have a "context limit." We had to chop our cleaned Markdown files into small pieces called "chunks." We wrote `src/prepare_rag_splits.py` using a framework called **LangChain** to do this.

1. **Header Extraction:** We used LangChain's `MarkdownHeaderTextSplitter`. This tool saw our `### Timestamp: 01:01` headers, ripped them out of the text, and injected them neatly into a JSON `metadata` dictionary. Now, every chunk of text secretly carries its video timestamp!
2. **Text Splitting:** We used `RecursiveCharacterTextSplitter` to cut the remaining text into chunks of exactly **384 tokens** (with a 15% overlap so we didn't accidentally chop a sentence in half). We chose 384 tokens because our upcoming embedding model (`BGE-small`) has a strict 512-token limit.

## 6. Splitting for Machine Learning (No Cheating!)
In Machine Learning, you have to split your data into Training and Testing sets. 
If we just shuffled our chunks randomly, a chunk about "Week 3 PCA" might end up in the Training set, and another chunk about "Week 3 PCA" might end up in the Test set. This is called **Data Leakage** (essentially, letting the model cheat on the test).

To prove to the TA that our evaluation is mathematically rigorous, we split the chunks strictly chronologically:
- **Train Set (Weeks 1-8)**: 4,304 chunks
- **Validation Set (Weeks 9-10)**: 216 chunks
- **Test Set (Weeks 11-12)**: 192 chunks

*These final JSON-L files are saved in `data/splits/` and are 100% ready for Milestone 3.*

---

## 🛠️ Summary of Technologies Used
- **Python (uv)**: Core programming language and fast environment manager.
- **BeautifulSoup**: Used for scraping raw HTML from Discourse and GitHub.
- **PyMuPDF4LLM**: State-of-the-art PDF to Markdown converter.
- **EasyOCR**: Deep-learning based Optical Character Recognition (beat Tesseract).
- **Regular Expressions (Regex)**: Used for surgical text cleaning (hyphens, whitespace).
- **LangChain**: Orchestrated the chunking and metadata extraction.
- **JSON-Lines (.jsonl)**: The format we used to store the final chunks, as it is highly efficient for vector databases to read.
