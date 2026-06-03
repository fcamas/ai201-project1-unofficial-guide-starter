# Project 1 Planning: The Unofficial Guide

---

## Domain

This project uses official New York State travel guides published by I LOVE NEW YORK, the state tourism program. It covers activities, destinations, history, family travel, LGBTQ travel, winter activities, and travel highlights across New York State. This knowledge is valuable because the guides are long PDFs that most visitors never read fully. A searchable guide lets anyone ask plain questions and get direct answers about what to do and see in New York.

---

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | I LOVE NY Black Travel Guide 2026 | Travel destinations and experiences for Black travelers | docs/nys_ded_ilny_blacktravel_2026.txt |
| 2 | I LOVE NY Kids Guide 2025 | Family and kids activities across New York | docs/nys_ded_ilny_kidsguide_2025.txt |
| 3 | I LOVE NY LGBTQ Travel Guide 2026 | LGBTQ friendly destinations and events | docs/nys_ded_ilny_lgbtqtravel_2026.txt |
| 4 | I LOVE NY Path Through History 2026 | Historic sites and cultural landmarks | docs/nys_ded_ilny_paththroughhistory_2026.txt |
| 5 | I LOVE NY Travel Highlights 2026 | Top highlights and must see destinations | docs/nys_ded_ilny_travelhighlights_2026.txt |
| 6 | I LOVE NY Travel Planner 2024 | Comprehensive travel planning guide | docs/nys_ded_ilny_travelplanner_2024.txt |
| 7 | I LOVE NY Winter Guide 2023 | Winter activities, ski resorts, and seasonal events | docs/winter_guide_2023web_462e3703-fe29-4026-8fa9-20d1194ca603.txt |

---

## Chunking Strategy

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Reasoning:** The travel guides contain short destination descriptions and activity listings. Each entry is typically 2 to 3 sentences long which fits well in 300 characters. The 50 character overlap ensures that if a description spans a chunk boundary it can still be retrieved as a complete thought.

---

## Retrieval Approach

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers. Runs locally with no API key needed.

**Top-k:** 3 chunks per query

**Production tradeoff reflection:** For a real deployment I would consider a larger model like OpenAI text-embedding-3-large for better accuracy on travel specific content. The tradeoff is cost and latency since it requires an API call. For international tourists I would also consider a multilingual model. For this project the local model is fast, free, and accurate enough.

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What are good activities for kids in New York? | Skiing, zoos, family resorts |
| 2 | What LGBTQ friendly destinations are in New York? | Information from the LGBTQ travel guide |
| 3 | What are the best winter activities in New York? | Skiing, winter resorts, seasonal events |
| 4 | What historic sites can I visit in New York? | Sites from the Path Through History guide |
| 5 | What are the top travel highlights in New York for 2026? | Highlights from the travel highlights guide |

---

## Anticipated Challenges

1. Some PDFs contain heavy formatting with bullet points and symbols that survive extraction as noise. This could make chunks harder to read and match to clean queries.

2. Several guides cover overlapping destinations. A question about a specific city could pull chunks from multiple guides, making the answer feel scattered rather than focused.

---

## Architecture

```
docs/*.txt
    |
    v
Document Ingestion (Python, open())
    |
    v
Chunking (300 chars, 50 overlap)
    |
    v
Embedding (sentence-transformers: all-MiniLM-L6-v2)
    |
    v
Vector Store (ChromaDB)
    |
    v
Retrieval (semantic search, top 3 chunks)
    |
    v
Generation (Groq: llama-3.3-70b-versatile)
    |
    v
Answer with source citation
```

---

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:** I gave Claude the chunking strategy section and asked it to implement load_documents() and chunk_document() with 300 character chunks and 50 character overlap.

**Milestone 4 — Embedding and retrieval:** I gave Claude the retrieval approach section and architecture diagram and asked it to implement embed_and_store() using ChromaDB and retrieve() returning the top 3 chunks with source metadata.

**Milestone 5 — Generation and interface:** I gave Claude the grounding requirement from the project instructions and asked it to implement generate_response() using Groq and build a Gradio interface with an input box, answer output, and sources output.
