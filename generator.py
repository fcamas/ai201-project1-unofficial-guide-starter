from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    if not retrieved_chunks:
        return "I could not find anything relevant in the New York travel guides. Try rephrasing your question."

    context_parts = []
    for i, chunk in enumerate(retrieved_chunks, 1):
        context_parts.append(f"[Source {i} - {chunk['source']}]\n{chunk['text']}")
    context = "\n\n".join(context_parts)

    system_prompt = (
        "You are a helpful New York travel assistant. "
        "Answer using ONLY the travel guide text provided below. "
        "Do not draw on outside knowledge. "
        "If the answer is not in the provided text, say so clearly. "
        "Always state which source file the answer comes from."
    )

    user_message = (
        f"Here are the relevant travel guide excerpts:\n\n{context}\n\n"
        f"Question: {query}"
    )

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )

    return response.choices[0].message.content
