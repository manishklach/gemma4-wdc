from __future__ import annotations

from difflib import SequenceMatcher
from math import sqrt


def token_bag(text: str) -> dict[str, int]:
    tokens = [token for token in text.replace("|", " ").replace(":", " ").split() if token]
    counts: dict[str, int] = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    return counts


def cosine_from_bags(left: dict[str, int], right: dict[str, int]) -> float:
    shared = set(left) | set(right)
    numerator = sum(left.get(token, 0) * right.get(token, 0) for token in shared)
    left_norm = sqrt(sum(value * value for value in left.values()))
    right_norm = sqrt(sum(value * value for value in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)


class EmbeddingProvider:
    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled
        self._model = None
        if enabled:
            try:
                from sentence_transformers import SentenceTransformer

                self._model = SentenceTransformer("all-MiniLM-L6-v2")
            except Exception:
                self.enabled = False

    def similarity(self, first: str, second: str) -> float:
        lexical = cosine_from_bags(token_bag(first), token_bag(second))
        sequence_ratio = SequenceMatcher(None, first, second).ratio()
        base_score = max(lexical, sequence_ratio)
        if not self.enabled or self._model is None:
            return base_score
        embeddings = self._model.encode([first, second], normalize_embeddings=True)
        vector_a, vector_b = embeddings[0], embeddings[1]
        embedding_score = float((vector_a * vector_b).sum())
        return max(base_score, embedding_score)
