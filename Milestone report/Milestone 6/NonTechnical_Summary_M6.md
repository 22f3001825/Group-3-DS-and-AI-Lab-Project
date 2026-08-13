
# Milestone 6 — Non-Technical Summary

Summary: A reader-friendly description of the project purpose, how users interact with it, the benefits it delivers, and practical notes on privacy and usage.

## Problem Statement (Plain English)
Students and instructors often spend time searching through long lecture notes and transcripts to find specific answers. This project creates an assistant that reads course materials and returns concise, referenced answers to student questions.

## How a User Experiences the System
1. Visit the web demo or open the local app.
2. Upload a document (lecture notes or transcript) or choose a preset example.
3. Ask a question in plain language (e.g., "What is gradient descent?").
4. The assistant returns a short answer and shows the exact passages used as evidence.

## Key Benefits
- Saves time: instant answers with citations instead of manual search.
- Improves learning: students see both concise explanations and source material for deeper study.
- Supports instructors: reduces repetitive answering and surfaces common confusion areas.

## Limitations (simple terms)
- Not perfect: sometimes the AI may give incomplete answers or include irrelevant text; the system shows sources to help users verify responses.
- File types: best with text/markdown; PDFs should be converted properly.

## Privacy & Practical Tips
- Do not upload sensitive personal information. The pipeline can be configured to remove or redact personal identifiers during preprocessing.

## Full Layperson-Friendly Project Walkthrough (M1 → M6)
This walkthrough explains the project's steps and outcomes in plain language so someone without a technical background can understand what was done, why it matters, and how to use the system.

### M1 — Understanding the need and collecting materials
- What we did: talked to students/instructors and collected course materials (lecture notes, transcripts, FAQs) that students typically search through.
- Why: to know what users want and to gather the text the assistant will read.

### M2 — Cleaning the material and breaking it into pieces
- What we did: removed irrelevant bits (like timestamps or repeated headers), corrected obvious formatting issues, and split long documents into shorter paragraphs or "chunks".
- Why: shorter chunks make it easier for the system to find the exact part of a document that answers a question.

### M3 — Teaching the system to 'understand' text
- What we did: used pre-trained language models that convert each chunk of text into a compact numerical fingerprint (an "embedding") so the system can compare chunks and find ones similar to a user's question.
- Why: instead of scanning whole documents, the system retrieves the most relevant chunks quickly.

### M4 — Building the search-and-answer system
- What we did: put together a pipeline that (a) finds relevant chunks, (b) optionally refines their order, and (c) asks an AI to write a short answer using those chunks.
- Why: this gives users both a concise answer and the original passages that support the answer.

### M5 — Improving answer accuracy and checking quality
- What we did: added a step that reorders the candidate passages for higher accuracy and asked humans to check if answers were faithful to the sources.
- Why: to reduce incorrect or made-up answers and measure how trustworthy the system is.

### M6 — Deploying and making the tool usable for everyone
- What we did: packaged the system into a web demo where users can upload documents, try preset examples, and ask questions. Added monitoring and documentation.
- Why: to make the tool accessible to students and instructors and to gather more usage data.

## How a Non-Technical User Uses the System (Example)
1. Go to the demo website or open the local app.
2. Upload a lecture transcript (or choose an example).
3. Type a question in everyday language: "When is the assignment due?" or "Explain overfitting simply."
4. Get a short answer plus links or snippets showing where the information came from.

## Practical Scenarios and Benefits
- Quick revision: students can ask the assistant targeted questions while studying.
- Instructor support: instructors can identify recurrent student questions and improve materials.
- Accessibility: students with limited time or reading difficulties get concise, referenced explanations.

## Plain-English Limitations and Safety Notes
- The assistant tries to be accurate but can still make mistakes. Always check the source passages shown below the answer.
- Avoid uploading sensitive personal information; if you must, redact it before upload.
- The system is designed to cite where answers come from so users can verify the source.

## FAQ (for non-technical reviewers)
- Q: "Is this like Google?"
	A: Similar in that it finds text, but this tool searches only your uploaded course materials and gives answers grounded in those materials.
- Q: "Can it make things up?"
	A: It can. We added steps to reduce this (showing source passages and reranking), but users should confirm with the cited passages.
- Q: "Who can use it?"
	A: Students, TAs, and instructors who want fast, referenced answers from course content.

## Where to Find the Demo and Documentation
- Demo and usage instructions are in the project's README and the `Milestone report/Milestone 6/` folder which contains the user guide and deployment notes.

## Final Note to Non-Technical Readers
This project packages modern AI tools to make classroom materials easier to search and understand. It keeps the human in the loop by displaying the exact text used to form answers, which helps maintain trust and transparency.


