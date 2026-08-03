"""Milestone 4 — Optimised Evaluation Dataset (10 queries).

Reduced from 20 → 10 so each experiment finishes in ~20-25 min instead
of ~50 min, while still covering all 5 question categories.

Categories:
  - conceptual      (3)
  - mathematical    (2)
  - comparison      (2)
  - application     (1)
  - out_of_scope    (2)

Each item:
  query          : student question
  gold_keywords  : keywords expected in relevant chunks (retrieval eval)
  is_out_of_scope: True → system must decline
  category       : for per-category analysis in the report
"""

EVAL_DATASET = [

    # ── Conceptual ────────────────────────────────────────────────────────────
    {
        "query": "Explain the difference between overfitting and underfitting in decision trees.",
        "gold_keywords": ["overfit", "underfit", "depth", "complex", "noise", "generalize"],
        "is_out_of_scope": False,
        "category": "conceptual",
    },
    {
        "query": "What is the bias-variance tradeoff and why does it matter?",
        "gold_keywords": ["bias", "variance", "tradeoff", "error", "complexity", "generalization"],
        "is_out_of_scope": False,
        "category": "conceptual",
    },
    {
        "query": "What is regularization and why is it used in machine learning models?",
        "gold_keywords": ["regularization", "L1", "L2", "lasso", "ridge", "penalty", "overfitting"],
        "is_out_of_scope": False,
        "category": "conceptual",
    },

    # ── Mathematical / Formula ────────────────────────────────────────────────
    {
        "query": "What is the formula for Information Gain in decision trees?",
        "gold_keywords": ["entropy", "information gain", "IG", "E_P", "E_L", "E_R", "split"],
        "is_out_of_scope": False,
        "category": "mathematical",
    },
    {
        "query": "Write the gradient descent weight update rule and explain each term.",
        "gold_keywords": ["gradient", "learning rate", "update", "nabla", "loss", "weight"],
        "is_out_of_scope": False,
        "category": "mathematical",
    },

    # ── Comparison ────────────────────────────────────────────────────────────
    {
        "query": "What is the difference between supervised and unsupervised learning?",
        "gold_keywords": ["supervised", "unsupervised", "label", "cluster", "class", "training"],
        "is_out_of_scope": False,
        "category": "comparison",
    },
    {
        "query": "Compare L1 and L2 regularization — when should you use each?",
        "gold_keywords": ["L1", "L2", "lasso", "ridge", "sparsity", "penalty", "feature"],
        "is_out_of_scope": False,
        "category": "comparison",
    },

    # ── Application ───────────────────────────────────────────────────────────
    {
        "query": "How does the learning rate affect the convergence of gradient descent?",
        "gold_keywords": ["learning rate", "convergence", "oscillate", "diverge", "step size"],
        "is_out_of_scope": False,
        "category": "application",
    },

    # ── Out-of-Scope Guardrail ────────────────────────────────────────────────
    {
        "query": "What is quantum machine learning?",
        "gold_keywords": [],
        "is_out_of_scope": True,
        "category": "out_of_scope",
    },
    {
        "query": "What is the capital of France?",
        "gold_keywords": [],
        "is_out_of_scope": True,
        "category": "out_of_scope",
    },
]
