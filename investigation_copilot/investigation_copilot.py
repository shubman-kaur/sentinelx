import numpy as np
import pickle
import requests
from sentence_transformers import SentenceTransformer
from groq import Groq

# ---- Configuration ----
EMBEDDINGS_FOLDER = "embeddings"
GROQ_API_KEY = "YOUR_GROQ_API_HERE"
GROQ_MODEL = "llama-3.3-70b-versatile"
SCAM_API_URL = "http://127.0.0.1:8000/predict-scam"

# ---- Load embedding model and saved chunk data (only once, at startup) ----
print("Loading model and embeddings...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = np.load(f"{EMBEDDINGS_FOLDER}/chunk_embeddings.npy")

with open(f"{EMBEDDINGS_FOLDER}/chunks_data.pkl", "rb") as f:
    data = pickle.load(f)
    chunks = data["chunks"]
    metadata = data["metadata"]

print(f"Loaded {len(chunks)} chunks with embeddings.\n")

# ---- Groq client ----
client = Groq(api_key=GROQ_API_KEY)


def cosine_similarity(query_vec, chunk_vecs):
    """Calculates cosine similarity between the query vector and all chunk vectors"""
    query_norm = query_vec / np.linalg.norm(query_vec)
    chunk_norms = chunk_vecs / np.linalg.norm(chunk_vecs, axis=1, keepdims=True)
    return np.dot(chunk_norms, query_norm)


def retrieve_top_chunks(query, top_k=5):
    """Returns the top-k most relevant chunks for a given query"""
    query_embedding = embed_model.encode([query])[0]
    similarities = cosine_similarity(query_embedding, embeddings)
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "text": chunks[idx],
            "source": metadata[idx]["source_document"],
            "similarity_score": float(similarities[idx])
        })
    return results


def get_scam_classifier_result(query):
    """Calls the running Scam Classifier FastAPI service and returns its result"""
    response = requests.post(SCAM_API_URL, json={"text": query})
    response.raise_for_status()
    return response.json()


def build_prompt(query, scam_result, retrieved_chunks):
    """Builds a structured prompt that grounds the LLM in retrieved context only"""

    context_text = ""
    for i, chunk in enumerate(retrieved_chunks):
        context_text += f"\n[Source {i+1}: {chunk['source']}]\n{chunk['text']}\n"

    scam_probability_pct = round(scam_result["scam_probability"] * 100, 2)

    # Only keep the red flags that were actually detected (value = 1)
    detected_flags = [
        flag for flag, value in scam_result["red_flags_detected"].items() if value == 1
    ]
    detected_flags_text = ", ".join(detected_flags) if detected_flags else "None detected"

    prompt = f"""You are a cyber fraud investigation assistant for Indian citizens.
You must answer ONLY using the information given in the CONTEXT below.
Do NOT use any outside knowledge. If the context does not contain enough
information, say so honestly instead of guessing.

USER QUERY:
{query}

SCAM CLASSIFIER OUTPUT:
Verdict: {scam_result["verdict"]}
Scam Probability: {scam_probability_pct}%
Red Flags Detected by Classifier: {detected_flags_text}

CONTEXT (retrieved from official CERT-In / RBI / NCRB advisories):
{context_text}

Based on the above, respond in this EXACT structure:

1. Scam Probability: (state the given scam probability)
2. Red Flags Identified: (list the suspicious patterns relevant to this query)
3. Evidence from Official Sources: (summarize what the context says, mention source names)
4. Recommended Action: (what should the user do right now)
5. How to Report (FIR / Complaint Steps): (steps based on context, e.g. cybercrime.gov.in, 1930 helpline)
6. Do's and Don'ts: (short bullet list)
"""
    return prompt


def get_investigation_response(query):
    """
    Full pipeline: get scam score, retrieve relevant chunks, then generate a
    grounded structured answer. Returns both the text report and the raw
    numeric scam classifier data (needed later by the Central Intelligence Engine).
    """

    scam_result = get_scam_classifier_result(query)
    retrieved_chunks = retrieve_top_chunks(query, top_k=5)
    prompt = build_prompt(query, scam_result, retrieved_chunks)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "report": response.choices[0].message.content,
        "scam_probability": scam_result["scam_probability"],
        "verdict": scam_result["verdict"],
        "red_flags_detected": scam_result["red_flags_detected"]
    }


# ---- Test ----
if __name__ == "__main__":
    test_query = "I got a call from someone claiming to be a CBI officer saying I am under investigation and need to pay a fine immediately"

    result = get_investigation_response(test_query)
    print(result["report"])
    print("\n---")
    print(f"Numeric scam probability: {result['scam_probability']}")