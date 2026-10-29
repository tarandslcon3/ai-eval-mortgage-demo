"""Load and chunk mortgage policy documents for indexing."""
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"

CHUNK_SIZE = 400


def load_chunks() -> list[dict]:
    chunks = []
    for path in sorted(DOCS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        current = ""
        for para in paragraphs:
            if not current:
                current = para
            elif len(current) + len(para) + 2 < CHUNK_SIZE:
                current = current + "\n\n" + para
            else:
                if len(current) > 300:
                    # Hard split oversized blocks to stay under limit
                    for i in range(0, len(current), CHUNK_SIZE):
                        piece = current[i : i + CHUNK_SIZE]
                        if piece:
                            chunks.append({"text": piece, "source": path.name})
                    current = para
                else:
                    chunks.append({"text": current, "source": path.name})
                    current = para
        if current:
            chunks.append({"text": current, "source": path.name})
    return chunks
