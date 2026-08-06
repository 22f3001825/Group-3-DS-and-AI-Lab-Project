# Question Intelligence — Build Report

_Generated 2026-08-06 10:51 UTC · schema v1 · embeddings `BAAI/bge-small-en-v1.5`_

## Thresholds

- `QI_DUPLICATE_THRESHOLD` = 0.95 (cosine similarity)
- Discriminative-token guard: **on** (duplicates must also agree on numerals and polarity words)
- `QI_CLUSTER_DISTANCE` = 0.2 (cosine distance, average linkage)

## Corpus

| Metric | Value |
|---|--:|
| Question units parsed | 420 |
| Distinct doubts (canonicals) | 415 |
| Units folded into a duplicate group | 5 |
| Duplicate rate | 1.2% |
| Clusters | 236 |
| Clusters fit to display | 66 |
| Singleton clusters | 143 |
| Admin-authored units | 0 |

### By source type

| Source | Units | Canonicals | Duplicate rate |
|---|--:|--:|--:|
| `PYQ` | 155 | 152 | 1.9% |
| `faq` | 143 | 141 | 1.4% |
| `pq` | 122 | 122 | 0.0% |

## Most common doubts

Ranked by **`asked_count`** — how many times a doubt was asked — not by
`canonical_count`. Deduplication is exactly what collapses the repetition this
ranking is trying to surface, so ranking by distinct doubts would invert it.

`asked_count` counts members from `faq`, `pq` only. `PYQ` is excluded because its unit boundaries come from the OCR's
`[Extracted Question]` markers rather than from the printed paper: one question
routinely yields eight units, and ranking on `member_count` put that scan at the
top of "most asked" with nobody having asked it.

Clusters shown have `asked_count` ≥ 2.

| # | Cluster | Asked | Members | Distinct | Weeks | Sources |
|--:|---|--:|--:|--:|---|---|
| 1 | Optimization Problem | 8 | 8 | 8 | 10, 11 | `faq` |
| 2 | Perceptron Algorithm Steps | 6 | 6 | 6 | 9 | `faq`, `pq` |
| 3 | Likelihood Function | 5 | 5 | 5 | 6, 9 | `faq` |
| 4 | Discriminative Models | 5 | 5 | 5 | 8, 10 | `faq`, `pq` |
| 5 | Choose the correct statements: | 4 | 5 | 5 | 3 | `faq`, `pq`, `PYQ` |
| 6 | Probability of Choosing Clusters in K-means++ | 4 | 5 | 5 | 3 | `faq`, `PYQ` |
| 7 | Parameter Calculation | 4 | 4 | 2 | 8 | `faq` |
| 8 | Naive Bayes | 4 | 4 | 4 | 8 | `faq`, `pq` |
| 9 | Maximizing Margin | 4 | 4 | 4 | 9, 10 | `faq` |
| 10 | 4.Perceptron Loss | 4 | 4 | 4 | 12 | `faq` |

## Limitations

These are properties of the approach, not oversights, and the numbers above should
be read with them in mind.

- **Concept tagging is week-granular for the existing corpus.** `topic_tags` are
  assigned per week, so clusters are labelled from the parsed question text rather
  than mapped to taxonomy IDs. Content added through the admin path can carry
  explicit topic IDs; 0 of 420 units currently do.
- **PYQ text is OCR output and only partly usable.** Question boundaries are not
  recoverable, so each extracted block is one unit. Its recurring scaffolding is
  stripped before embedding — left in, it is identical across documents and would
  make unrelated PYQ questions score as near-duplicates.
- **The forum input is absent, not merely stale.** `data/cleaned/discourse/` is an
  empty directory and no chunk in any split carries `source_type == "discourse"`,
  so every number here covers a narrower corpus than Milestone 1 §2.2.8 describes.
  A TA can paste a thread in through the admin path; there is no scraper.
