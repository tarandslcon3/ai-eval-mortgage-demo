"""BM25-based retrieval over the mortgage policy corpus."""
from rank_bm25 import BM25Okapi
from .corpus import load_chunks

_chunks: list[dict] | None = None
_bm25: BM25Okapi | None = None


def _build_index():
    global _chunks, _bm25
    _chunks = load_chunks()
    tokenized = [c["text"].lower().split() for c in _chunks]
    _bm25 = BM25Okapi(tokenized)


def retrieve(query: str, k: int = 3) -> list[dict]:
    if _bm25 is None:
        _build_index()
    tokens = query.lower().split()
    scores = _bm25.get_scores(tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    return [_chunks[i] for i in top_indices]
