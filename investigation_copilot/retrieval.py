import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

EMBEDDINGS_FOLDER = "embeddings"

# Load the model and saved data (only once, at startup)
print("Loading model and embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = np.load(f"{EMBEDDINGS_FOLDER}/chunk_embeddings.npy")

with open(f"{EMBEDDINGS_FOLDER}/chunks_data.pkl", "rb") as f:
    data = pickle.load(f)
    chunks = data["chunks"]
    metadata = data["metadata"]

print(f"Loaded {len(chunks)} chunks with embeddings.\n")


def cosine_similarity(query_vec, chunk_vecs):
    """Calculates cosine similarity between the query vector and all chunk vectors"""
    query_norm = query_vec / np.linalg.norm(query_vec)
    chunk_norms = chunk_vecs / np.linalg.norm(chunk_vecs, axis=1, keepdims=True)
    return np.dot(chunk_norms, query_norm)


def retrieve_top_chunks(query, top_k=5):
    """Returns the top-k most relevant chunks for a given query"""
    query_embedding = model.encode([query])[0]

    similarities = cosine_similarity(query_embedding, embeddings)

    # Get indices of the top-k highest similarity scores
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "text": chunks[idx],
            "source": metadata[idx]["source_document"],
            "similarity_score": float(similarities[idx])
        })

    return results


# ---- Test ----
if __name__ == "__main__":
    test_queries = [
        "CBI officer called saying you are under investigation",
        "someone asking for OTP to verify bank account",
        "how to report a cyber fraud complaint"
    ]

    for test_query in test_queries:
        print(f"Query: {test_query}\n")
        results = retrieve_top_chunks(test_query, top_k=2)
        for i, result in enumerate(results):
            print(f"--- Result {i+1} (source: {result['source']}, score: {result['similarity_score']:.4f}) ---")
            print(result["text"][:200])
            print()
        print("=" * 60)