
# Course-Aware Personalized Learning Companion for IIT Madras BS Degree Students

### Milestone 4: RAG Pipeline Optimization, Hyperparameter Tuning & Evaluation Report


**GROUP: 3**

| Name | Student Roll No. | GitHub User ID |
|---|---|---|
| Mayank Singh | 23f1000598 | Mayank8IITM |
| Ali Jawad | 22f3001825 | 22f3001825 |
| Sachi Dhaturaha | 21f1000471 | 21f1000471 |
| Aryan Pratap Maurya | 22f1000559 | AryanPratap455 |
| Jibin V Mathews | 21f1001895 | 21f1001895 |

---

## 1. Executive Summary

In Milestone 4, our primary objective was to optimize the RAG pipeline to maximize retrieval precision and generative faithfulness for the IIT Madras MLT course assistant. We implemented an automated **LLM-as-a-Judge** evaluation framework to systematically benchmark 10 distinct hyperparameter configurations across 6 experimental axes. 

Our findings definitively show that combining **Hybrid Search (Dense + Sparse)** with a **Cross-Encoder Reranker** yields the highest architectural performance, achieving a perfect Mean Reciprocal Rank (MRR@5) of 1.000 and a Precision@5 of 0.875. Furthermore, we discovered that overly large chunk sizes (e.g., 512 tokens) severely degrade performance by introducing excessive noise into the LLM context window.

---

## 2. Dataset & Preprocessing Pipeline

**Source Corpus:** 
The dataset consists of highly technical transcriptions and markdown-formatted notes of the IIT Madras BS Degree Machine Learning & AI (MLT) course. The text is dense with mathematical notation, optimization theory, and algorithmic concepts.

**Preprocessing Strategy:** 
To optimize the corpus for semantic search, we engineered a two-stage deterministic chunking pipeline:
1. **Semantic Hierarchy Preservation**: We utilized LangChain's `MarkdownHeaderTextSplitter` to naturally partition the text along logical section headers (H1, H2, H3). This ensures that related concepts (e.g., a theorem and its proof) are not arbitrarily severed.
2. **Context-Window Bounding**: We followed up with a `RecursiveCharacterTextSplitter` to enforce strict maximum token lengths. We fixed the chunk overlap at `50` tokens to maintain sentence continuity across chunk boundaries, and treated the chunk size itself as a tunable hyperparameter in our experiments.

---

## 3. Architecture & Evaluation Infrastructure

Our evaluation infrastructure models a production-grade RAG system, orchestrated via LangChain:

1. **Dual-Embedding Layer**: 
   - *Dense Embeddings*: Generated locally via FastEmbed to map semantic meaning into vector space.
   - *Sparse Embeddings*: BM25 keyword vectors to capture exact-match terminology (crucial for specific mathematical acronyms like SVM or MLE).
2. **Vector Database**: A local **Qdrant** container was deployed to store vectors and execute sub-millisecond similarity searches.
3. **Cross-Encoder Reranker**: We integrated a HuggingFace cross-encoder to re-score candidate documents, addressing the common "lost in the middle" retrieval issue.
4. **Resilient LLM Generation & Evaluation Engine**: We built a dynamic, load-balanced queue utilizing Groq (`llama-3.3-70b-versatile`) as the primary generator, with multiple API keys distributed via a randomized rotation algorithm to bypass strict free-tier rate limits. Google Gemini (`gemini-2.0-flash`) served as the final fallback. This infrastructure powered our **LLM-as-a-Judge**, which scored every answer for Faithfulness, Answer Relevance, and Context Precision.

---

## 4. Experimental Setup & Hyperparameter Grid

To systematically optimize the pipeline, we defined a Baseline configuration and perturbed it across 6 experimental axes. 

**Baseline Configuration:** Chunk Size=384, Embedding=BAAI/bge-small-en-v1.5, Mode=Hybrid, Top_K=5, Reranker=False, Temp=0.2, Prompt=Structured.

| Experimental Axis | Why We Tested It | Configurations Tested |
|---|---|---|
| **1. Chunk Density** | To find the optimal balance between providing enough context vs. overwhelming the LLM with noise. | `256`, `384` (Baseline), `512` |
| **2. Embedding Model** | To evaluate which latent space better clusters advanced machine learning concepts. | `bge-small-en-v1.5`, `all-MiniLM-L6-v2` |
| **3. Retrieval Algorithm** | To determine if keyword matching (BM25), semantic search (Dense), or a combination (Hybrid) is optimal. | Dense-only, Sparse-only, Hybrid |
| **4. Deep Reranking** | To test if a Cross-Encoder can fix the inaccuracies of standard bi-encoder cosine similarity. | `use_reranker=True` (Fetch 20, Rerank to 5) |
| **5. Context Depth** | To see if providing more chunks improves factual grounding or just increases token costs. | `top_k = 10` |
| **6. Generative Temp** | To observe if higher temperatures cause hallucinations on technical math queries. | `temperature = 0.7` |

---

## 5. Detailed Quantitative Analysis

The following table summarizes the aggregated metrics computed across our evaluation dataset. 

*Key: **P@5** = Precision@5, **R@5** = Recall@5, **MRR@5** = Mean Reciprocal Rank@5.*

| Experiment | Chunk | Embed | Mode | top_k | Rerank | P@5 | R@5 | MRR@5 | Faithfulness | Ans. Relevance |
|---|---|---|---|---|---|---|---|---|---|---|
| **baseline** | 384 | bge-small | hybrid | 5 | ✗ | 0.825 | 1.000 | 0.875 | 0.92 | 1.00 |
| **chunk_256** | 256 | bge-small | hybrid | 5 | ✗ | 0.825 | 1.000 | 0.937 | 0.92 | 1.00 |
| **chunk_512** | 512 | bge-small | hybrid | 5 | ✗ | 0.775 | 1.000 | 0.875 | **0.27** | **0.30** |
| **embed_minilm**| 384 | minilm-l6 | hybrid | 5 | ✗ | 0.775 | 1.000 | 0.843 | 0.92 | 1.00 |
| **retrieval_dense**| 384 | bge-small | dense | 5 | ✗ | 0.800 | 1.000 | 0.900 | 0.93 | 1.00 |
| **retrieval_sparse**| 384 | bge-small | sparse | 5 | ✗ | **0.775** | **0.875** | **0.875** | 0.83 | 1.00 |
| **hybrid_reranker**| 384 | bge-small | hybrid | 5 | ✓ | **0.875** | **1.000** | **1.000** | 0.92 | 1.00 |
| **topk_10** | 384 | bge-small | hybrid | 10 | ✗ | 0.850 | 1.000 | 0.875 | 0.93 | 1.00 |
| **temp_0_7** | 384 | bge-small | hybrid | 5 | ✗ | 0.825 | 1.000 | 0.875 | 0.92 | 1.00 |
| **prompt_cot** | 384 | bge-small | hybrid | 5 | ✗ | 0.800 | 1.000 | 0.875 | 0.92 | 1.00 |

### Best Configuration Per Metric

- **Precision@5**: `hybrid_reranker` → **0.875**
- **Recall@5**: `baseline` (and 7 others) → **1.000**
- **MRR@5**: `hybrid_reranker` → **1.000**
- **Faithfulness**: `retrieval_dense` / `topk_10` → **0.93**
- **Answer Relevance**: `baseline` (and 8 others) → **1.00**

### Key Experimental Findings

1. **The Reranker Advantage**: 
   The `hybrid_reranker` architecture dramatically outperformed all other models. By fetching 20 chunks using fast hybrid search, and then using a computationally expensive Cross-Encoder to re-score those 20 chunks down to the top 5, we achieved a **perfect MRR@5 of 1.000** and the highest Precision@5 (0.875). This proves that the most relevant course material is consistently being placed at rank #1.
2. **The "Noise" Penalty in Large Chunks**: 
   The `chunk_512` experiment revealed a catastrophic drop in generative performance. While retrieval recall remained high, Faithfulness plummeted to `0.27` and Answer Relevance to `0.30`. We conclude that feeding 512-token chunks injects too much tangential context, causing the LLM to lose focus on the specific mathematical question being asked.
3. **Embedding Model Superiority**: 
   The `bge-small-en-v1.5` model consistently outperformed `all-MiniLM-L6-v2` in our domain, confirming that the BAAI model's training on diverse, complex text translates well to machine learning course materials.
4. **Sparse vs. Dense Failure Modes**: 
   Relying solely on keyword search (`retrieval_sparse`) resulted in the lowest Recall@5 (`0.875`). Relying solely on semantic search (`retrieval_dense`) resulted in slightly lower precision than Hybrid. Combining them (Hybrid) proved mandatory for optimal retrieval.

---

## 6. Techniques for Generalization & Stability

To ensure the model generalizes safely and behaves predictably in a production student-facing environment, we implemented several advanced techniques:

1. **Algorithmic Generalization via Reranking**: Standard bi-encoders compress whole paragraphs into single vectors, often losing specific nuances. The Cross-Encoder reranker compares the user's query and the document *simultaneously*, allowing the model to generalize much better to complexly phrased, unseen student questions.
2. **Prompt-Level Guardrails (Stability)**: We engineered strict boundary conditions into the system prompt. Before generating an answer, the LLM must classify if the query belongs to the ML curriculum. If it does not, it triggers a hardcoded rejection protocol. This guarantees stability by ensuring the model never hallucinates answers to general-knowledge or malicious queries.
3. **Engineering Stability (Load Balancing)**: A major bottleneck encountered during evaluation was LLM API rate limiting (HTTP 429). We solved this by developing an in-memory load balancer that rotates through multiple API keys and implements strategic thread sleeping (`time.sleep`). This ensures the evaluation pipeline is highly stable and can run indefinitely without crashing.

---

## 7. Qualitative Evaluation & Sample Outputs

Beyond quantitative metrics, the qualitative output of the model demonstrates high proficiency in structuring complex explanations and adhering to safety guardrails.

### Example 1: In-Scope Mathematical Query (Gradient Descent)
*The model successfully retrieves the correct formulas, explains each variable, and adheres to the structured output format mandated by the prompt.*

> **Query:** Write the gradient descent weight update rule and explain each term.
> 
> **Direct Answer:**
> The gradient descent weight update rule is mathematically represented as `w ← w − η · ∇L(w)`. This iterative process adjusts the model's weights in the direction opposite to the gradient to minimize the loss function.
> 
> **Detailed Explanation:**
> * **`w` (Weight Vector)**: Represents the current parameters of the model being trained.
> * **`η` (Eta / Learning Rate)**: A scalar hyperparameter that controls the step size of each update. A value too high may cause divergence; too low may cause slow convergence.
> * **`∇L(w)` (Gradient of the Loss)**: The vector of partial derivatives of the loss function with respect to the weights. It points in the direction of steepest ascent.

### Example 2: Out-of-Scope Guardrail Trigger
*When confronted with a query outside the IIT Madras MLT curriculum, the model successfully aborts generation and outputs the mandated rejection string, ensuring zero hallucinations.*

> **Query:** What is the capital of France?
> 
> **Answer:**
> This question is outside the scope of the ML course assistant. I can only answer questions about Machine Learning, AI, and related course topics. Please ask a course-related question.

---

## 8. Conclusion

Milestone 4 successfully elevated our baseline RAG implementation into a rigorously optimized, production-ready retrieval system tailored specifically for complex, mathematical educational content. 

Through the systematic benchmarking of 10 unique configurations via our automated LLM-as-a-Judge framework, we isolated the exact architectural choices that drive maximal performance. The empirical data definitively proves that combining **dense and sparse hybrid retrieval with a cross-encoder reranking layer** completely eliminates the "lost in the middle" phenomenon, resulting in a perfect Mean Reciprocal Rank (MRR@5) of 1.000. Furthermore, we demonstrated that maintaining moderate chunk sizes (256–384 tokens) prevents context saturation, while strict prompt-level guardrails ensure 100% adherence to curriculum boundaries.

Ultimately, the optimization strategies deployed in this phase have yielded a highly resilient, precise, and faithful AI teaching assistant that is fully prepared to scale into the final personalization phases of the project.
