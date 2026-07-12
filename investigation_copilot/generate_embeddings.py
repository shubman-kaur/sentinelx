import os
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

CHUNKS_FOLDER = "docs/chunks"
EMBEDDINGS_FOLDER = "embeddings"

os.makedirs(EMBEDDINGS_FOLDER, exist_ok=True)

print("Loading embedding model (first time will download, may take a while)...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded!\n")


all_chunks = []      
all_metadata = []     
for doc_folder in os.listdir(CHUNKS_FOLDER):
    doc_path = os.path.join(CHUNKS_FOLDER, doc_folder)
    if not os.path.isdir(doc_path):
        continue

    chunk_files = sorted(os.listdir(doc_path))
    for chunk_file in chunk_files:
        chunk_path = os.path.join(doc_path, chunk_file)
        with open(chunk_path, "r", encoding="utf-8") as f:
            text = f.read()

        all_chunks.append(text)
        all_metadata.append({
            "source_document": doc_folder,
            "chunk_file": chunk_file
        })

print(f"Total chunks loaded: {len(all_chunks)}")


print("Generating embeddings...")
embeddings = model.encode(all_chunks, show_progress_bar=True)
print(f"Embeddings shape: {embeddings.shape}")


np.save(os.path.join(EMBEDDINGS_FOLDER, "chunk_embeddings.npy"), embeddings)

with open(os.path.join(EMBEDDINGS_FOLDER, "chunks_data.pkl"), "wb") as f:
    pickle.dump({
        "chunks": all_chunks,
        "metadata": all_metadata
    }, f)

print("\n✅ Embeddings generated and saved!")
print(f"   - {EMBEDDINGS_FOLDER}/chunk_embeddings.npy")
print(f"   - {EMBEDDINGS_FOLDER}/chunks_data.pkl")