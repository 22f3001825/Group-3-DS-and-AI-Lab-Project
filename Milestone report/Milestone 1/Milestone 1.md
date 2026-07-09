*DS\&AI Lab Project \[Term May 2026\]*

**Course-Aware Personalized Learning Companion for IIT Madras BS Degree Students**

**Milestone 1:**  
**Problem Definition & Literature Review**


| Name | Student Roll No. | Github User ID |
| :---: | :---: | :---: |
| Mayank Singh | 23f1000598 | *Mayank8IITM* |
| Ali Jawad | 22f3001825 | *22f3001825* |
| Sachi Dhaturaha | 21f1000471 | *21f1000471* |
| Aaryan Pratap Maurya  | 22f1000559 | *AryanPratap455* |
| Jibin V Mathews | 21f1001895 | *21f1001895* |

**1\. Introduction and Context**

Students enrolled in the IIT Madras BS Degree program learn primarily through recorded lectures, written course notes, slide decks, previous year question papers (PYQs), frequently asked questions (FAQs), and discussion forums. Each of these resources typically lives on a different platform, and none of them is aware of the others. A student trying to revise a single concept may need to search a lecture video for the right timestamp, dig through a notes PDF, scroll a forum thread for a similar doubt, and separately look up whether that concept has appeared in past question papers. This scattering of resources is the starting point of the problem this project addresses.

General-purpose AI tools have made parts of this easier. Tools that can answer questions from uploaded documents, and tools that can turn notes into quizzes, already exist and are genuinely useful. What they do not do is stay aware of a specific course over time, remember what a specific student already struggles with, or connect a student's questions back to the exact moment in a lecture where the answer was taught. This document lays out the objectives of the proposed Course-Aware Learning Companion, reviews the existing tools that are closest to this space, and identifies where the real gaps and opportunities lie.

This document is scoped strictly to the problem statement and proposed solution as defined for this project. It does not make claims about tools, features, or outcomes beyond what is either stated in the problem statement or drawn from publicly available information about existing products. Where a claim is based on external information, it is treated as a general industry observation rather than a guarantee about any specific product's current behaviour, since AI products change quickly.

**1.1 Stakeholders**

The primary stakeholders for this project include:
*   **Students (Primary Users):** The learners enrolled in the IIT Madras BS program who will use the companion for personalized revision, doubt resolution, and lecture navigation.
*   **Instructors and Teaching Assistants (TAs):** Course administrators who benefit from the automated organization of common doubts (FAQs/PYQs) and gain insights into prevalent knowledge gaps through aggregated analytics.
*   **Course Content Creators:** Professionals who design the course material and can leverage the identified knowledge gaps to refine and improve future iterations of the course content.

**Objectives of the Project**

The objectives below follow directly from the proposed solution and key features described in the problem statement. They are organised from the most foundational (building the knowledge base) to the most advanced (closing the feedback loop between assessment and revision).

**2.1 Primary Objective**

To design and develop a prototype AI-powered learning companion for the IIT Madras BS Degree program that unifies scattered course resources into a searchable, source-grounded knowledge base and personalizes the learning experience based on each student's demonstrated understanding. For the initial prototype and evaluation, the system will be implemented using a single IIT Madras BS course.

**2.2 Supporting Objectives**

1. Build a unified, course-specific knowledge base by integrating lecture transcripts, course notes, slides, PYQs, FAQs, and discussion forum content for one selected course.  
2. Provide source-grounded question answering using Retrieval-Augmented Generation (RAG), so that every answer can be traced back to the specific course material it came from, rather than being generated from the model's general knowledge alone.  
3. Enable lecture timestamp navigation, so that when a student asks a question, the system can point to the exact point in a recorded lecture where the concept is explained, saving the time otherwise spent scrubbing through a video.  
4. Maintain a learner profile that is built from quiz performance and interaction history, and that persists across sessions instead of resetting every time the student opens the tool.  
5. Detect knowledge gaps from that learner profile and turn them into concrete, actionable revision recommendations.  
6. Generate personalized quizzes that are targeted at a student's identified weak areas rather than being generic or one-size-fits-all.  
7. Track learning progress over time so that both the student and the underlying system can see whether a gap is closing.  
8. Build an AI Question Intelligence Module that continuously organizes PYQs, FAQs, and forum questions by identifying duplicates, grouping related concepts, and maintaining an up-to-date repository of common student doubts improving both retrieval quality and the relevance of personalized recommendations.  
9. Present the above through a Learning Analytics Dashboard, giving the student a single place to see their progress, gaps, and recommended next steps.

**2.3 Scope Boundary for the Initial Prototype**

The problem statement is explicit that the initial prototype will focus on a single IIT Madras BS course. This document treats that as a firm boundary: the objectives above describe what the prototype should demonstrate for one course, not a claim about multi-course or program-wide coverage at this stage. Expansion to additional courses is discussed later as an opportunity, not as a committed objective.

**3\. Review of Existing Solutions, Baselines, and Benchmarks**

Before defining what the Course-Aware Learning Companion should build from scratch, it is worth looking honestly at what already exists. Three categories of tools are closest in spirit to parts of the proposed solution: document-grounded AI research assistants (using NotebookLM as the representative example named in scope), AI-based quiz and adaptive-assessment tools, and general-purpose LLM assistants. Each is reviewed here on its own terms, what it does well, and where its design naturally stops short of what a course-aware companion needs.

**3.1 NotebookLM (Document-Grounded AI Research Assistant)**

NotebookLM, built by Google, is a source-grounded assistant: it answers questions using only the documents a user uploads into a notebook, and it attaches citations that link an answer back to the exact passage it came from. This design choice is deliberate and is what keeps it close to Retrieval-Augmented Generation in spirit, the model is not supposed to answer from general world knowledge, only from what has been placed in front of it.

For students, this has real value. NotebookLM can ingest PDFs, slides, text files, and lecture transcripts (via YouTube video links), and from these it can generate summaries, study guides, mind maps, and  relevant to this project flashcards and quizzes grounded in the uploaded material. It also offers an Audio Overview feature that turns source material into a spoken, podcast-style discussion, which some students use as a way to revise while commuting or doing other tasks.

Where NotebookLM's design naturally stops short of a course-aware companion is in three places. First, a notebook is only as current and complete as what a user manually uploads, it does not know about a course as a structured, evolving entity; someone has to keep feeding it material. Second, its quizzes and flashcards are generated from whatever is in the notebook at that moment, but there is no persistent, cross-session learner model tracking what a specific student has repeatedly gotten wrong over weeks of study. Third, it is not built around lecture-video timestamp navigation for revision, it can summarize a transcript, but it is not designed to say "this exact doubt is answered at minute 14:32 of lecture 6."

**3.2 AI-Based Quiz and Adaptive Assessment Tools**

A separate category of tools focuses specifically on quiz generation and adaptive assessment. These range from consumer study apps that turn uploaded notes into flashcards and quizzes, to more structured adaptive-assessment platforms used in classrooms, which adjust question difficulty based on how a student is performing and flag the concepts a student is struggling with.

The common thread across this category is that assessment is the center of gravity: the tool's main job is to generate a question, grade the response, and adjust future questions accordingly. Some platforms in this space do track performance data over time within their own environment and use it to sequence content. This is conceptually close to the "Learner Profile & Progress Tracking" and "Personalized Quiz Generation" features described in the problem statement.

What this category typically does not do is act as the primary knowledge base for open-ended question answering. A student cannot generally ask these tools a free-form doubt and get a source-grounded explanation with a citation back to a specific lecture; their strength is structured assessment, not conversational, source-grounded Q\&A. They also tend to work from whatever content an instructor or student manually loads in, rather than continuously synthesizing PYQs, FAQs, and live discussion-forum activity into one organized repository.

**3.3 General-Purpose LLM Assistants**

General-purpose LLM assistants conversational AI tools trained on broad, general-purpose data  are widely used by students already, simply because they are flexible and can answer almost any question in natural language, including course-related doubts, without any setup.

Their central limitation for this use case is grounding. Because these assistants draw on broad pre-training data rather than a specific course's actual materials, an answer may be generically correct about a topic while still not matching how a particular instructor taught it, which textbook was used, or what was actually said in that course's lectures. Academic research on LLMs has repeatedly flagged hallucination—plausible-sounding but incorrect output—as a significant risk (Zhang et al., 2023) [1]. Furthermore, studies indicate that this risk is substantially reduced, though not completely eliminated, when a model is anchored to a trusted source using techniques like Retrieval-Augmented Generation (RAG) (Lewis et al., 2020) [2], rather than relying solely on general parametric memory.

General-purpose assistants also do not, by default, retain a persistent, structured model of a specific student's mastery across a course over time; each conversation is typically self-contained unless a separate memory layer is deliberately added. And naturally, they have no built-in awareness of a specific course's lecture timestamps, PYQ history, or forum activity unless a user manually pastes that context into the conversation every time which defeats the purpose of a unified, low-friction companion.

**3.4 Comparative Summary**

The table below lines up the three categories against the dimensions that matter most for this project. It is meant as an honest side-by-side, not a scorecard, each category of tool is good at what it was built for.

| Dimension | NotebookLM | AI Quiz / Adaptive-Assessment Tools | General-Purpose LLM Assistants |
| :---- | :---- | :---- | :---- |
| Grounding | Source-grounded on user-uploaded documents; citations link back to the exact passage | Grounded on uploaded notes for question generation; not typically used for open Q\&A | Grounded mainly in pre-training data; web-search plug-ins add partial grounding |
| Primary use case | Summarizing, querying, and repackaging a fixed set of uploaded documents | Generating quizzes/flashcards and adapting question difficulty to performance | General conversational question-answering and explanation |
| Course-awareness | Limited to whatever the user manually uploads into a notebook; no built-in course structure | Content is scoped to what a teacher/student uploads; no cross-source course model | None by default; answers are not tied to a specific course's syllabus or materials |
| Persistent learner profile | Not a core feature; notebooks store sources and outputs, not a learner mastery model | Some tools track quiz performance within their own platform | Not persistent across sessions unless a third-party memory layer is added |
| Timestamped lecture navigation | Not designed for lecture-video timestamp linking | Not applicable | Not applicable |
| Duplicate / related question handling | Not a designed feature | Some platforms cluster items into topic banks for reuse | Not applicable; each query handled independently |
| Integration of PYQs, FAQs, forum data | Possible only if user manually uploads them as sources | Largely limited to instructor-provided question banks | Not integrated unless manually pasted into a prompt |

*Table 1: Comparison of existing tool categories against the capabilities described in the problem statement*

**3.5 Evaluation Metrics**

To ensure the Course-Aware Learning Companion meets its objectives quantitatively, the system will be evaluated using standard Retrieval-Augmented Generation (RAG) metrics [4]. Frameworks such as Ragas or TruLens will be utilized to measure:

* **RAG Q&A:** Retrieval Precision and Recall at *k*, with a target of **≥ 80%**; Answer Faithfulness (Groundedness) to the provided course material, with a target of **≥ 88%**; and Citation Accuracy, with a target of **≥ 85%**.
* **Lecture Navigation:** Timestamp Accuracy within **±10 seconds** for **≥ 80%** of evaluated queries.
* **Learner Profile:** Knowledge Gap Detection Precision of **≥ 80%**, validated against actual quiz performance.
* **Personalized Quizzes:** Relevance to identified weak areas of **≥ 80%**, with an average **pre/post revision quiz score improvement of at least 15%**.
* **Question Intelligence:** Deduplication Precision of **≥ 85%** and **Cluster F1 Score of ≥ 80%**.
* **Overall Experience:** Task completion time **at least 20% faster** than manual search and a **usability rating of at least 3.8/5**.
  
**3.6 What This Review Suggests About Baselines**

Taken together, these three categories suggest a reasonable set of informal baselines for the proposed system rather than formal published benchmarks, since no single existing tool combines all the target capabilities:

* Source-grounded answering with citations, NotebookLM is the closest reference point for this behaviour, and its citation-linking approach is a reasonable design pattern to learn from.  
* Adaptive, performance-driven quizzing, AI quiz and assessment tools are the closest reference point for how difficulty adjustment and gap-flagging can work in practice.  
* Open, flexible natural-language explanation, general-purpose LLM assistants set the expectation for how naturally a student expects to be able to ask a free-form question.

No claim is made here that any of these tools has been formally benchmarked against the others for this specific use case; the comparison is a qualitative one based on publicly documented product capabilities, used to ground the gap analysis that follows.

**4\. Identified Gaps**

The review above points to a consistent pattern: every existing category solves one piece of the problem well, but none of them combines source-grounded, course-specific answering with a persistent learner model and an automatically maintained question repository. The table below summarizes the specific gaps this project is positioned to address.

| Gap Area | What Existing Tools Offer | What Is Missing |
| :---- | :---- | :---- |
| Course-specific grounding | General document upload and Q\&A | A single, continuously updated knowledge base built specifically around one course's lectures, notes, PYQs, FAQs and forum threads |
| Lecture navigation | Text and slide summarization | Direct linking of an answer to the exact lecture timestamp where the concept is taught |
| Learner modelling | Session-based quiz scores | A persistent learner profile that accumulates evidence over time and feeds back into recommendations |
| Question intelligence | Manual question banks curated by instructors | Automated de-duplication and clustering of PYQs, FAQs and forum questions to keep the repository current |
| Closed feedback loop | Quiz generation or Q\&A in isolation | A loop where quiz outcomes shape revision recommendations, which in turn shape future quizzes and retrieval ranking |

*Table 2: Gaps between existing tool categories and the capabilities required by a course-aware learning companion*

**4.1 Gap 1: No Single Tool Is Course-Aware by Design**

NotebookLM and general-purpose LLMs can both be pointed at course material, but only if a student or instructor does the work of assembling and uploading it, and keeping it updated. Neither treats a course as a standing, evolving entity that lecture transcripts, notes, PYQs, and forum activity all belong to. The proposed system's unified knowledge base for one course is intended to close this specific gap.

**4.2 Gap 2: No Timestamp-Level Link Between a Doubt and a Lecture**

None of the reviewed categories are built to connect a specific question to the exact moment in a recorded lecture where it is addressed. Students are left to either re-watch entire lectures or rely on generic summaries. Lecture Timestamp Navigation, as described in the problem statement, targets this gap directly.

**4.3 Gap 3: Assessment and Knowledge Retrieval Are Not Connected**

Quiz and assessment tools track performance; document-grounded assistants answer questions. In the reviewed tools, these two things largely happen in separate systems that do not feed each other. A student's poor quiz performance on a topic does not automatically improve how the Q\&A system prioritizes or explains that topic the next time they ask about it, and vice versa. The proposed Knowledge Gap Detection & Revision Recommendation feature is meant to close this loop.

**4.4 Gap 4: Question Repositories Are Manually Maintained, Not Living Systems**

PYQs, FAQs, and forum discussions accumulate duplicate questions and near-duplicate variants over time, and existing tools generally rely on manual curation to keep a question bank organized. The AI Question Intelligence Module identifying duplicates, grouping related concepts, and keeping the repository current  addresses a gap that none of the three reviewed categories are designed to solve automatically.

**4.5 Gap 5:  No Persistent, Cross-Session Learner Profile Tied to Course Content**

Where performance tracking exists at all in the reviewed tools, it is generally scoped to that tool's own environment and its own content, not tied to the specific structure of one course's syllabus and materials. A learner profile that persists over the duration of a course, and that is grounded in that course's actual content, is a gap the proposed system is intended to fill.

**5\. Opportunities**

The gaps above are also, read the other way, the opportunities this project can pursue. None of them require inventing entirely new AI techniques, Generative AI, RAG, NLP, and learning analytics are all established, well-documented approaches. The opportunity is in combining them around one course, in a way that none of the reviewed tool categories currently do.

**5.1 Combine Grounded Retrieval with a Living Learner Model**

The clearest opportunity is architectural: pairing a RAG-based, source-grounded Q\&A layer (in the spirit of what NotebookLM demonstrates for citation-backed answers) with a persistent learner profile (in the spirit of what adaptive quiz tools demonstrate for performance tracking)  and letting the two inform each other. A question a student asks repeatedly, or a quiz topic they consistently miss, can directly shape what gets recommended for revision next.

**5.2 Use Lecture Timestamps as a Genuine Differentiator**

Since none of the reviewed tool categories are built around timestamp-level navigation of lecture video, this is an area where even a modest implementation would offer something students cannot currently get from existing tools in one place. Grounding an answer in both a text citation and a lecture timestamp gives a student two complementary ways to verify and revisit a concept.

**5.3 Turn Scattered Doubts Into a Structured, Reusable Asset**

PYQs, FAQs, and forum threads currently exist as separate, loosely organized pools of text. The AI Question Intelligence Module is an opportunity to convert this scattered material into a structured asset: a de-duplicated, concept-tagged repository that improves retrieval quality for every student who asks a related question afterward, and that surfaces genuinely common doubts to instructors as a useful by-product.

**5.4 Start Narrow, Prove the Loop, Then Consider Expansion**

Because the prototype is explicitly scoped to one course, there is an opportunity to prove out the full retrieval-plus-personalization loop end-to-end on a manageable, well-defined dataset before considering whether the same architecture could extend to other IIT Madras BS courses. This document does not commit to that expansion, it is noted here only as a natural next step if the single-course prototype demonstrates the intended feedback loop between grounded answering, quizzing, and revision recommendations.

**5.5 Learning Analytics as a Shared View for Students**

A Learning Analytics Dashboard that brings together retrieval activity, quiz performance, and progress over time gives students a single, persistent view of their own learning,  something that is currently split across whichever platform happens to host the lecture, the notes, the PYQs, or the forum on any given day.

**6\. Conclusion**

Students on the IIT Madras BS program already have access to strong individual resources i.e recorded lectures, notes, PYQs, FAQs, and forums  and to strong individual AI tools that can help with pieces of the studying process, such as document-grounded assistants, quiz generators, and general-purpose LLM chat. What is missing is not any single capability in isolation, but the connective tissue between them: a system that is aware of one specific course as a whole, that remembers a specific student's progress in that course over time, and that turns scattered questions into an organized, ever-improving resource for everyone taking it.

The objectives set out in Section 2, read against the gaps identified in Section 4, describe a prototype that is deliberately narrow in scope, one course  but broad in what it tries to demonstrate: source-grounded answering, timestamped lecture navigation, a persistent learner profile, personalized quizzing, and an automatically maintained question repository, all working together rather than as separate tools. That combination, more than any single feature, is where this project's contribution lies.

**7\. References**

[1] Y. Zhang et al., "Siren's Song in the AI Ocean: A Survey on Hallucination in Large Language Models," *Computational Linguistics*, vol. 51, no. 4, 2025. [Online]. Available: https://arxiv.org/abs/2309.01219

[2] P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," in *Advances in Neural Information Processing Systems*, 2020. [Online]. Available: https://arxiv.org/abs/2005.11401

[3] Google, "NotebookLM," 2024. [Online]. Available: https://notebooklm.google.com

[4] S. Esval et al., "Ragas: Automated Evaluation of Retrieval Augmented Generation," *arXiv preprint arXiv:2309.15217*, 2023. [Online]. Available: https://arxiv.org/abs/2309.15217

