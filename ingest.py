import os
from config import DOCS_PATH


def load_documents():
    documents = []
    for filename in sorted(os.listdir(DOCS_PATH)):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCS_PATH, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({
                "source": filename,
                "text": text,
            })
    print(f"Loaded {len(documents)} document(s)")
    return documents


def chunk_document(text, source):
    chunk_size = 300
    overlap = 50
    min_length = 50

    chunks = []
    prefix = source.replace(".txt", "")
    counter = 0
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end].strip()

        if len(chunk_text) >= min_length:
            chunks.append({
                "text": chunk_text,
                "source": source,
                "chunk_id": f"{prefix}_{counter}",
            })
            counter += 1

        start += chunk_size - overlap

    return chunks
