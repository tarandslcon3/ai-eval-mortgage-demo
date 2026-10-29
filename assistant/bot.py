"""Claude-backed mortgage assistant."""
import os
import re
import anthropic
from dotenv import load_dotenv
from .retriever import retrieve

load_dotenv()

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


SYSTEM_PROMPT = """You are a helpful mortgage advisor assistant for Northfield Harbour Lending.
Answer the customer's question using only the provided policy excerpts.
If the answer is not in the excerpts, say you don't have that information.
Cite the source document names at the end of your answer using the format: [source: filename].
Keep answers concise and friendly."""

MODEL = os.getenv("BOT_MODEL", "claude-haiku-5-5")
MAX_TOKENS = 400


def ask(question: str) -> dict:
    chunks = retrieve(question, k=3)
    context_parts = []
    for c in chunks:
        context_parts.append(f"--- {c['source']} ---\n{c['text']}")
    context = "\n\n".join(context_parts)

    user_message = f"Policy excerpts:\n\n{context}\n\nCustomer question: {question}"

    response = _get_client().messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    text_blocks = [b for b in response.content if hasattr(b, "text")]
    answer_text = text_blocks[0].text if text_blocks else ""

    # Extract cited sources from the model's response
    pattern = re.compile(r"\[source:\s*([^\]]+)\]")
    match = pattern.search(answer_text)
    if match:
        cited = [s.strip() for s in match.group(0).split(",")]
    else:
        cited = []

    retrieved_chunks = [{"source": c["source"], "text": c["text"][:120]} for c in chunks]

    return {
        "answer": answer_text,
        "citations": cited,
        "retrieved_chunks": retrieved_chunks,
    }
