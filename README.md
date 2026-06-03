# The Unofficial Guide — Project 1

---

## Domain

This system covers official New York State travel guides published by I LOVE NEW YORK. It makes travel information searchable through plain language questions. The knowledge is valuable because the guides are long PDFs that most visitors never read in full. A searchable guide lets anyone ask plain questions like "what can kids do in New York?" and get a direct answer without reading dozens of pages.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | I LOVE NY Black Travel Guide 2026 | PDF extracted to txt | docs/nys_ded_ilny_blacktravel_2026.txt |
| 2 | I LOVE NY Kids Guide 2025 | PDF extracted to txt | docs/nys_ded_ilny_kidsguide_2025.txt |
| 3 | I LOVE NY LGBTQ Travel Guide 2026 | PDF extracted to txt | docs/nys_ded_ilny_lgbtqtravel_2026.txt |
| 4 | I LOVE NY Path Through History 2026 | PDF extracted to txt | docs/nys_ded_ilny_paththroughhistory_2026.txt |
| 5 | I LOVE NY Travel Highlights 2026 | PDF extracted to txt | docs/nys_ded_ilny_travelhighlights_2026.txt |
| 6 | I LOVE NY Travel Planner 2024 | PDF extracted to txt | docs/nys_ded_ilny_travelplanner_2024.txt |
| 7 | I LOVE NY Winter Guide 2023 | PDF extracted to txt | docs/winter_guide_2023web_462e3703-fe29-4026-8fa9-20d1194ca603.txt |

---

## Chunking Strategy

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** The travel guides contain short destination descriptions and activity listings. Each entry is typically 2 to 3 sentences which fits well in 300 characters. This size is large enough to hold one complete idea without mixing unrelated destinations. The 50 character overlap ensures that if a description spans a chunk boundary it can still be retrieved as a complete thought.

**Final chunk count:** Over 1,000 chunks across 7 documents

---

## Sample Chunks

**Chunk 1 (nys_ded_ilny_kidsguide_2025.txt):**
"Learn to ski or ride through the I SKI NY Kids Learn to Ski or Ride Passport Program, available for 3rd and 4th graders across New York State resorts."

**Chunk 2 (winter_guide_2023web_462e3703-fe29-4026-8fa9-20d1194ca603.txt):**
"Full-service slope-side resorts offer activities for the whole family including ski school, equipment rentals, and lodge dining."

**Chunk 3 (nys_ded_ilny_travelplanner_2024.txt):**
"New York State offers a wide range of family-friendly destinations from world-class museums to outdoor adventures in the Adirondacks."

**Chunk 4 (nys_ded_ilny_lgbtqtravel_2026.txt):**
"New York City's Greenwich Village is home to the Stonewall National Monument, the first national monument dedicated to LGBTQ history."

**Chunk 5 (nys_ded_ilny_paththroughhistory_2026.txt):**
"The Path Through History program connects visitors to over 500 historic sites and cultural landmarks across New York State."

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers. Runs locally with no API key and no rate limits.

**Production tradeoff reflection:** For a real deployment serving thousands of tourists I would consider a larger model like OpenAI text-embedding-3-large for better accuracy on travel specific content. The tradeoff is cost and latency since it requires an API call for every query. For international tourists I would also consider a multilingual embedding model since New York attracts visitors from all over the world. For this project the local model is fast, free, and accurate enough.

---

## Grounded Generation

**System prompt grounding instruction:** "You are a helpful New York travel assistant. Answer using ONLY the travel guide text provided below. Do not draw on outside knowledge. If the answer is not in the provided text, say so clearly. Always state which source file the answer comes from."

**How source attribution is surfaced in the response:** Each retrieved chunk is labeled with its source file name before being passed to the model. The model is instructed to always name the source in its answer. The UI also displays a separate sources box showing the file name and distance score for each retrieved chunk.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are good activities for kids in New York? | Skiing, zoos, family resorts | Correctly described ski passport program, zoos, and slope-side resorts with source citations | Relevant | Accurate |
| 2 | What LGBTQ friendly destinations are in New York? | Info from LGBTQ travel guide | Found relevant chunks from LGBTQ guide with specific destinations | Relevant | Accurate |
| 3 | What are the best winter activities in New York? | Skiing, winter resorts, seasonal events | Correctly described winter activities and resorts from winter guide | Relevant | Accurate |
| 4 | What historic sites can I visit in New York? | Sites from Path Through History guide | Found historic site information with source citations | Relevant | Accurate |
| 5 | What are the top travel highlights in New York for 2026? | Highlights from travel highlights guide | Returned relevant highlights but mixed sources from multiple guides | Partially relevant | Partially accurate |

---

## Failure Case Analysis

**Question that failed:** "What are the top travel highlights in New York for 2026?"

**What the system returned:** The system returned chunks from multiple guides mixed together, making the answer feel scattered rather than focused on the highlights guide specifically.

**Root cause (tied to a specific pipeline stage):** This is a retrieval issue. Several guides cover overlapping destinations so the embedding similarity search pulled chunks from different guides that all matched the query equally well. The retrieval step has no way to know the user wants only the highlights guide.

**What you would change to fix it:** Add metadata filtering so users can choose which guide to search. For example a dropdown in the UI to select a specific guide before asking a question. This would narrow retrieval to only the relevant source.

---

## Spec Reflection

**One way the spec helped you during implementation:** Writing the chunking strategy in planning.md before coding made it easy to implement chunk_document() with confidence. The 300 character chunk size and 50 character overlap were already decided so there was no guesswork during coding.

**One way your implementation diverged from the spec, and why:** The spec assumed 10 documents but the project was built with 7 high quality official guides instead. The guides are large and content rich so 7 files produced over 1,000 chunks which is more than enough for good retrieval quality.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* The planning.md chunking strategy section describing 300 character chunks with 50 character overlap and the document structure
- *What it produced:* The full ingest.py file with load_documents() and chunk_document() functions
- *What I changed or overrode:* The source field naming was adjusted to be consistent across ingest.py and retriever.py

**Instance 2**

- *What I gave the AI:* The grounding requirement from the project instructions and the retrieval approach section
- *What it produced:* The full generator.py with system prompt and context formatting
- *What I changed or overrode:* The system prompt was updated to specifically mention New York travel guides instead of a generic assistant, making the grounding more specific to this domain
