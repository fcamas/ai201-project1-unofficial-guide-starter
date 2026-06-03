import gradio as gr
from ingest import load_documents, chunk_document
from retriever import get_collection, embed_and_store, retrieve
from generator import generate_response


def ingest_documents():
    collection = get_collection()
    if collection.count() > 0:
        print(f"Skipping ingestion — {collection.count()} chunks already stored.")
        return

    documents = load_documents()
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc["text"], doc["source"])
        all_chunks.extend(chunks)

    print(f"Total chunks produced: {len(all_chunks)}")
    embed_and_store(all_chunks)


def ask(question):
    chunks = retrieve(question)
    answer = generate_response(question, chunks)
    sources = "\n".join(f"- {c['source']} (distance: {c['distance']:.3f})" for c in chunks)
    return answer, sources


ingest_documents()

with gr.Blocks(title="New York Unofficial Guide") as demo:
    gr.Markdown("# New York Unofficial Guide\nAsk any question about traveling and exploring New York.")
    inp = gr.Textbox(label="Your question", placeholder="What are good activities for kids in New York?")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=4)
    btn.click(ask, inputs=inp, outputs=[answer, sources])
    inp.submit(ask, inputs=inp, outputs=[answer, sources])

demo.launch()
