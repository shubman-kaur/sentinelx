import os

EXTRACTED_FOLDER = "docs/extracted"
CHUNKS_FOLDER = "docs/chunks"

os.makedirs(CHUNKS_FOLDER, exist_ok=True)

CHUNK_SIZE = 800      
CHUNK_OVERLAP = 100   
def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Text ko overlapping chunks mein todta hai.
    Sentence boundary (". ") pe split karne ki koshish karta hai taaki
    sentence beech mein na kate.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        if end < text_length:
           
            last_period = text.rfind(". ", start, end)
            if last_period != -1 and last_period > start:
                end = last_period + 1  
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        
        start = end - overlap if end - overlap > start else end

    return chunks


for filename in os.listdir(EXTRACTED_FOLDER):
    if not filename.endswith(".txt"):
        continue

    filepath = os.path.join(EXTRACTED_FOLDER, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_text(text)

    doc_name = os.path.splitext(filename)[0]
    print(f"{doc_name}: {len(chunks)} chunks created")

    # Har chunk ko alag file mein save 
    doc_chunk_folder = os.path.join(CHUNKS_FOLDER, doc_name)
    os.makedirs(doc_chunk_folder, exist_ok=True)

    for i, chunk in enumerate(chunks):
        chunk_filename = f"chunk_{i:03d}.txt"
        with open(os.path.join(doc_chunk_folder, chunk_filename), "w", encoding="utf-8") as f:
            f.write(chunk)

print("\n✅ Chunking complete!")