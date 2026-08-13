
# Milestone 6 — User Guide

## Introduction

This comprehensive guide provides instructions for students, instructors, and administrators to effectively use the MLT Course Assistant. The guide covers getting started, navigating features, interpreting results, troubleshooting common issues, and advanced usage patterns.

## 1. Getting Started

### 1.1 Accessing the System

**For Online Deployment:**
1. Open your web browser (Chrome, Firefox, Safari, or Edge)
2. Navigate to the deployment URL provided in your course syllabus or email
3. Log in with your IIT Madras credentials
4. You are ready to start asking questions

**For Local Installation (Developers and Instructors):**

```bash
# Step 1: Clone repository
git clone <repository-url>
cd Group-3-DS-and-AI-Lab-Project

# Step 2: Set up Python environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Start backend (Terminal 1)
cd src
uvicorn api.main:app --reload --port 8000

# Step 5: Start frontend (Terminal 2)
cd web
npm install
npm run dev

# Step 6: Open application
# Visit http://localhost:5173 in your browser
```

The system will display a login prompt. Use your course credentials to access your personalized learning environment.

### 1.2 Understanding the Interface

The application consists of four main sections:

1. **Chat Tab:** Ask questions and get instant answers with source citations
2. **Quiz Tab:** Take personalized quizzes generated based on your learning progress
3. **Progress Tab:** View your learning journey, topic mastery levels, and recommendations
4. **Upload Tab:** Add new course materials to the knowledge base

## 2. Asking Questions (Chat Feature)

### 2.1 Basic Query Workflow

**Step 1: Navigate to Chat**
Click the "Chat" tab in the navigation menu.

**Step 2: Formulate Your Question**
Type your question in the text input field at the bottom of the screen. Questions can be:
- Conceptual: "Explain what overfitting means"
- Formula-based: "What is the equation for Information Gain?"
- Comparative: "What's the difference between bagging and boosting?"
- Application-oriented: "How would you handle class imbalance in a decision tree?"
- Process-oriented: "Walk me through the gradient descent update process"

**Step 3: Submit Your Question**
Press the "Ask" button or press Enter. The system will:
1. Search through all indexed course material (typically <2 seconds)
2. Retrieve the most relevant passages
3. Generate a concise answer using those passages
4. Display the answer with source citations

**Step 4: Review the Answer**
The response appears in three components:
- **Direct Answer:** A 2-4 sentence response addressing your question
- **Detailed Explanation:** Additional context when needed
- **Source Passages:** The exact text from course materials used to generate the answer

### 2.2 Examples of Effective Questions

**Example 1: Conceptual Question**
- **Your Question:** "What is the bias-variance tradeoff?"
- **System Response:** "The bias-variance tradeoff describes the balance between two types of model errors. Bias measures how well the model approximates the true function (simple models have high bias). Variance measures sensitivity to training data variations (complex models have high variance). An optimal model minimizes total error by balancing these competing concerns."
- **Sources:** Week 4 Lecture Transcript, Slide 8-10 | Course Notes, Chapter 3

**Example 2: Formula-Based Question**
- **Your Question:** "What is the formula for calculating cross-entropy loss?"
- **System Response:** "Cross-entropy loss is calculated as: L = -Σ(y_i * log(ŷ_i)), where y_i is the true label (0 or 1) and ŷ_i is the predicted probability. For multi-class problems, sum across all classes. This formula penalizes predictions that are confidently wrong more severely than those that are slightly wrong."
- **Sources:** Week 6 Lecture Transcript, Slide 5 | Loss Functions Notes, Section 2.1

**Example 3: Comparative Question**
- **Your Question:** "How does random forest differ from a single decision tree?"
- **System Response:** "Random forests build multiple decision trees on random subsets of data and average their predictions, reducing variance. Individual decision trees are prone to overfitting on the training data. Random forests improve generalization by decorrelating individual trees and leveraging ensemble averaging. This comes at the cost of interpretability, as random forest predictions are harder to explain than a single tree."
- **Sources:** Week 8 Lecture Transcript, Slides 12-15 | Ensemble Methods Notes

### 2.3 Question Tips for Better Answers

**Tip 1: Be Specific**
- ❌ Vague: "Tell me about trees"
- ✓ Specific: "Explain how information gain is calculated in decision trees"

**Tip 2: Provide Context**
- ❌ Unclear: "What about regularization?"
- ✓ Clear: "Explain L1 and L2 regularization and when to use each one"

**Tip 3: Ask One Thing at a Time**
- ❌ Multiple questions: "What's overfitting, why is it bad, and how do we prevent it?"
- ✓ Single question: "What is overfitting?" (then ask follow-ups)

**Tip 4: Use Course Terminology**
- Course-specific terms increase answer precision
- E.g., "Information Gain" rather than "measure of feature importance"

### 2.4 Conversation Memory

The system maintains conversation context across queries:
- Your entire chat history is preserved during your session
- The system remembers previous questions and can refer to earlier topics
- If you ask "Explain this further," the system understands which topic you mean
- Session history is saved to your learner profile for later review

## 3. Interpreting Answers

### 3.1 Answer Components

Each response consists of:

**Main Answer:**
- Concise, direct response to your question
- Typically 2-4 sentences
- Uses technical terminology accurately
- Cites specific concepts and formulas when relevant

**Source Passages:**
Below the main answer, you see relevant excerpts from course materials. Each passage includes:
- Source indicator: Document name and section (e.g., "Week 3 Lecture, Slide 5")
- Exact text from the course material
- Relevance score (1-10 scale) indicating how relevant the passage is to your question

**Context Links:**
- Click on any source passage to view the full document context
- Access links to related topics in the course material

### 3.2 Evaluating Answer Quality

**High Quality Indicators:**
- Answer directly addresses your question
- Sources are relevant and recent (from core course material, not side notes)
- Multiple sources support the answer
- Technical terminology is used correctly
- References to specific slides or chapters are accurate

**Lower Quality Indicators:**
- Answer is vague or incomplete
- Source passages seem tangentially related
- Only one source found
- Answer contradicts what you recall from lectures
- → **Action:** Refine your question with more specific terms or ask for clarification

### 3.3 Confidence Indicators

The system provides confidence metrics:
- **Retrieval Confidence:** How well did we find relevant material? (Shown as percentage)
  - >90% = Excellent, high confidence in sources
  - 70-90% = Good, reliable sources found
  - <70% = Lower confidence, consider refining question

- **Generation Confidence:** How grounded is the answer in sources?
  - Automatically computed and shown with answer
  - Low confidence (<80%) = Answer might be incomplete
  - → **Action:** Review source passages carefully or rephrase question

## 4. Taking Quizzes (Personalized Assessment)

### 4.1 Quiz Generation

**Accessing Quizzes:**
1. Navigate to the "Quiz" tab
2. Select "Generate New Quiz"
3. Choose options:
   - **Topic Focus:** Select a specific topic (e.g., "Decision Trees") or "Random Topics"
   - **Difficulty Level:** Beginner, Intermediate, or Advanced
   - **Number of Questions:** 3, 5, 10, or 20 questions
   - **Quiz Type:** Multiple Choice (recommended for quick practice) or Short Answer

**Quiz Generation Process:**
- System analyzes your learning profile and identifies weak areas
- Generates questions from topics you've struggled with
- Creates questions grounded in actual course material
- Each question includes the correct answer plus three plausible distractors

### 4.2 Taking a Quiz

**For Each Question:**
1. Read the question carefully
2. Choose your answer from the options
3. Click "Next" or "Submit" to proceed
4. The system records your response and the time taken
5. After completing the quiz, you get immediate feedback:
   - Score (percentage correct)
   - Breakdown by topic
   - Explanation for each answer with source references
   - Recommendations for topics needing review

### 4.3 Quiz Performance and Recommendations

The system tracks:
- Overall quiz scores
- Performance by topic
- Questions you get wrong repeatedly (indicates knowledge gaps)
- Time spent per question (too fast = potentially guessing)

**Using Results:**
- Review explanations for missed questions
- Use source references to re-read relevant material
- Request targeted quizzes on weak topics
- Track improvement over time in the Progress tab

## 5. Tracking Learning Progress

### 5.1 Progress Dashboard

The "Progress" tab displays:

**Topic Mastery Overview:**
- Visual representation of your proficiency in each course topic
- Color-coded: Red (needs work), Yellow (moderate), Green (mastered)
- Shows topics you've engaged with most

**Statistics:**
- Total questions asked: Tracks your engagement
- Average answer rating: How helpful you found the answers
- Quiz performance: Latest scores and trends
- Time spent learning: Engagement metric

**Personalized Recommendations:**
- Topics recommended for review based on quiz performance
- Suggested questions to ask for weak areas
- Learning paths: Recommended sequence for studying related topics

### 5.2 Knowledge Gap Detection

The system automatically identifies:
- Topics where you have low quiz scores (<70%)
- Concepts mentioned in questions but not well understood
- Topics related to weak areas but not yet explored

**Using Gap Detection:**
- Review recommended materials for identified gaps
- Ask clarifying questions about weak topics
- Take targeted quizzes to verify understanding after studying

## 6. Uploading and Managing Documents

### 6.1 Adding New Course Materials

**Accessing Upload Feature:**
1. Navigate to "Upload" tab (if visible) or contact your instructor
2. Click "Upload New Document"

**Supported File Formats:**
- `.md` (Markdown) — Recommended, preserves formatting
- `.txt` (Plain text) — Works well
- `.pdf` — Supported via OCR conversion
- `.docx` (Word documents) — Convert to .md or .txt first

**Upload Process:**
1. Select file from your computer
2. Enter document metadata:
   - Title (e.g., "Week 5 Lecture Transcript")
   - Topic/Course section
   - Source (e.g., "Lecture", "Notes", "FAQ", "PYQ")
3. Click "Upload and Process"
4. System processes the document (typically <5 minutes for large files)
5. Notification confirms document is indexed and searchable

**Post-Upload:**
- Document is automatically chunked and embedded
- Relevant topics are tagged automatically
- Available for queries immediately after processing
- You can ask questions that reference the newly uploaded material

### 6.2 File Preparation Tips

**For Best Results:**
- **Markdown Format:** Use `.md` files with proper heading hierarchy (# for topics, ## for subtopics)
- **Clean PDFs:** Ensure PDFs are text-based (not scanned images)
- **Reasonable Size:** Single documents should be <50 MB (typically not an issue for course materials)
- **Meaningful Names:** Use descriptive filenames ("Week5_Lecture_Notes" rather than "document1")

**PDF Conversion:**
If you have scanned PDFs, convert them first:
```bash
python scripts/pdf_to_text.py --input old_format.pdf --output course_notes.txt
```

## 7. Troubleshooting and Common Issues

### 7.1 System Not Responding

**Problem:** Web interface is blank or unresponsive

**Solutions (in order):**
1. Refresh the page (Ctrl+R or Cmd+R)
2. Clear browser cache (Settings → Clear browsing data)
3. Try a different browser (Chrome, Firefox, Safari)
4. Check your internet connection
5. Contact your instructor or system administrator

### 7.2 Query Returns No Results

**Problem:** System says "No relevant passages found"

**Possible Causes and Solutions:**
1. **Question is out of scope:**
   - Example: "What's the weather?"
   - Solution: Ask about course content instead

2. **Using non-standard terminology:**
   - Example: "What's the splitting criterion?" instead of "Information Gain"
   - Solution: Use exact terms from course materials

3. **Asking about material not yet covered:**
   - Example: Asking Week 10 material when only Weeks 1-6 are indexed
   - Solution: Check course calendar or upload the missing materials

4. **Overly complex compound question:**
   - Example: "How do decision trees, random forests, and boosting differ?"
   - Solution: Ask simpler questions first, then follow up with comparisons

### 7.3 Poor Quality Answers

**Problem:** Answer is incomplete or doesn't directly address question

**Diagnostic Approach:**
1. Check source passages—does the course material actually address your question?
2. Review the relevance scores of sources—are they highly relevant (>80%)?
3. Note the answer rating option—provide feedback by rating the answer

**Solutions:**
1. **Rephrase your question:** Add more context, use course terminology
   - ❌ "Explain trees"
   - ✓ "Explain how decision trees select splitting attributes using Information Gain"

2. **Ask a follow-up question:** Break complex questions into steps
   - Ask: "What is entropy?"
   - Then ask: "How is Information Gain calculated from entropy?"
   - Finally ask: "How does Information Gain guide feature selection?"

3. **Verify material is indexed:** Upload or request the instructor upload specific course materials

### 7.4 Slow Response Times

**Problem:** System takes >5 seconds to respond

**Possible Causes:**
- Peak usage times (when many students are using system)
- Large vector database searches
- LLM provider delays (external service)

**Solutions:**
1. Try again in a few minutes
2. During peak hours, be more specific in questions (reduces search complexity)
3. Contact instructor if consistently slow (indicates need for infrastructure upgrade)

### 7.5 Login Issues

**Problem:** Cannot log in to the system

**Solutions:**
1. Verify you're using correct IIT Madras credentials
2. Check for CAPS LOCK and ensure password is correct
3. Use "Forgot Password" option to reset credentials
4. Clear browser cookies and try again
5. Contact IT support if issue persists

### 7.6 File Upload Errors

**Problem:** File upload fails or processing hangs

**Solutions:**
1. Check file size (should be <50 MB)
2. Verify file format is supported (.md, .txt, .pdf)
3. Ensure PDF is text-based, not scanned image
4. Try converting file to plain text (.txt) format first
5. Retry after a few minutes

## 8. Advanced Features

### 8.1 Conversation Management

**Exporting Chat History:**
1. Open conversation
2. Click menu (three dots) → "Export Conversation"
3. Choose format: PDF, TXT, or JSON
4. Download to your device

**Searching Previous Conversations:**
1. Click "History" in sidebar
2. Use search box to find previous questions
3. Click to restore conversation

### 8.2 Customizing Learning Preferences

**Settings Menu:**
1. Click your profile icon (top right)
2. Select "Preferences"
3. Options available:
   - **Answer Length:** Short (2 sentences), Medium (3-4 sentences), Detailed (5+ sentences)
   - **Include Examples:** Always, Sometimes, Rarely
   - **Source Detail:** Full passages, Summary references, Minimal
   - **Quiz Difficulty:** Auto (matched to your level), Always Easy, Always Hard

### 8.3 Using API (Advanced Users)

For programmers and advanced users, the system exposes REST APIs:

**Query Endpoint:**
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is gradient descent?", "top_k": 5}'
```

**Response includes:**
- Generated answer
- Retrieved passages with metadata
- Relevance scores
- Execution time

**Full API documentation:** Visit `http://localhost:8000/docs` for interactive Swagger documentation

## 9. Best Practices

### 9.1 Study Strategies Using the Assistant

**Active Learning Approach:**
1. **Pre-reading:** Ask "What are the main topics in Week 3?"
2. **During lecture:** Ask clarifying questions about concepts
3. **Post-lecture:** Ask application questions and generate quizzes
4. **Before exam:** Use assistant for targeted review of weak topics

**Effective Workflow:**
1. Read assignment/syllabus to identify learning objectives
2. Ask assistant 3-5 questions targeting each objective
3. Review source passages to deepen understanding
4. Take a quiz to assess comprehension
5. Review failed questions and re-study referenced material
6. Retake quiz to verify improvement

### 9.2 Instructor Tips (for Faculty Access)

**Monitoring Student Engagement:**
- Review query analytics to identify frequently asked topics
- Use this data to refine unclear lecture content
- Identify students seeking help on weak topics

**Using Quiz Analytics:**
- Analyze which questions students consistently miss
- Identifies topics requiring additional explanation in lectures
- Tracks overall class performance trends

**Content Management:**
- Periodically upload new materials to keep system current
- Version-control materials (mark old versions)
- Review feedback on answer quality and improve prompts

## 10. Support and Feedback

### 10.1 Getting Help

**Within the Application:**
- Click "?" button in top-right corner for contextual help
- Review FAQ section for common questions
- Access video tutorials for feature walkthroughs

**Outside the Application:**
- Email instructor with specific questions about course content
- Post questions in course discussion forum
- Visit instructor office hours for complex learning issues

### 10.2 Providing Feedback

**Rate Answers:**
- After receiving an answer, use thumbs-up/thumbs-down to rate helpfulness
- Your ratings help improve system performance over time

**Report Issues:**
- Click "Report Problem" if answer is incorrect or unhelpful
- Provide specific feedback about what was wrong
- Include your question and the problematic answer

**Feature Requests:**
- Submit ideas for new features via settings → "Feedback"
- Vote on existing feature requests

## Conclusion

The MLT Course Assistant is designed to support your learning journey through efficient, accurate information retrieval from course materials. By combining structured study practices with this tool, you'll develop a deeper understanding of machine learning concepts while reducing time spent searching course materials. Remember: the assistant complements, not replaces, active engagement with course materials and critical thinking about the subject matter.

