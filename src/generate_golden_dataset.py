import json
import random
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TEST_CHUNKS_PATH = ROOT_DIR / "data" / "splits" / "test_chunks.jsonl"
GOLDEN_DATASET_PATH = ROOT_DIR / "data" / "golden_dataset.json"

def main():
    dataset = []
    
    # 1. Parse valid queries from held-out dataset
    with open(TEST_CHUNKS_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    questions_found = []
    for line in lines:
        if not line.strip():
            continue
        try:
            chunk = json.loads(line)
            meta = chunk.get("metadata", {})
            h2 = meta.get("h2", "")
            if h2.startswith("Question/Topic:"):
                # Extract the question
                question = h2.replace("Question/Topic:", "").strip()
                # Clean up emojis or prefixes if needed
                if question and len(question) > 10:
                    gold_context = chunk.get("text", "").strip()
                    # We will use words from the context as gold keywords for retrieval eval
                    words = [w.strip(".,()[]") for w in gold_context.split() if len(w) > 4]
                    gold_keywords = list(set(words))[:5]  # Take up to 5 unique long words
                    
                    questions_found.append({
                        "query": question,
                        "gold_keywords": gold_keywords,
                        "reference_context": gold_context,
                        "is_out_of_scope": False
                    })
        except Exception as e:
            pass
            
    # Sample 15 distinct valid questions to avoid excessive LLM costs
    random.seed(42)
    # Deduplicate by query
    unique_qs = {q["query"]: q for q in questions_found}
    sampled_qs = random.sample(list(unique_qs.values()), min(15, len(unique_qs)))
    dataset.extend(sampled_qs)
    
    # 2. Add non-contextual / out-of-scope queries
    out_of_scope = [
        {
            "query": "What is the capital of France?",
            "gold_keywords": [],
            "reference_context": "",
            "is_out_of_scope": True
        },
        {
            "query": "How do I make spaghetti carbonara?",
            "gold_keywords": [],
            "reference_context": "",
            "is_out_of_scope": True
        },
        {
            "query": "Can you give me medical advice for a headache?",
            "gold_keywords": [],
            "reference_context": "",
            "is_out_of_scope": True
        },
        {
            "query": "What are the rules of basketball?",
            "gold_keywords": [],
            "reference_context": "",
            "is_out_of_scope": True
        },
        {
            "query": "Write a python script to hack a wifi password.",
            "gold_keywords": [],
            "reference_context": "",
            "is_out_of_scope": True
        }
    ]
    dataset.extend(out_of_scope)
    
    # 3. Save to golden_dataset.json
    with open(GOLDEN_DATASET_PATH, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4)
        
    print(f"Golden dataset created with {len(dataset)} test cases and saved to {GOLDEN_DATASET_PATH.relative_to(ROOT_DIR)}.")

if __name__ == "__main__":
    main()
