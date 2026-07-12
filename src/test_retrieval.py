import os
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

# Load credentials
load_dotenv()

print("Loading Embedding Models (this takes a few seconds)...")
dense_embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")

print("Connecting to Qdrant Cloud...")
qdrant = QdrantVectorStore.from_existing_collection(
    embedding=dense_embeddings,
    sparse_embedding=sparse_embeddings,
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    collection_name="mlt_course_bot",
    retrieval_mode=RetrievalMode.HYBRID
)

retriever = qdrant.as_retriever(search_kwargs={"k": 2})  # Fetch top 2 results

print("\n--- Qdrant Test Engine Ready ---")
while True:
    query = input("\nAsk a question (or type 'exit'): ")
    if query.lower() == 'exit':
        break
        
    print("\nSearching Qdrant...")
    results = retriever.invoke(query)
    
    for i, doc in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(f"Source: {doc.metadata.get('source_type', 'Unknown')} (Week {doc.metadata.get('week', 'Unknown')})")
        print(f"Text Snippet: {doc.page_content[:300]}...")
