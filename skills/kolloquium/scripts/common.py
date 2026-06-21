"""Geteilte Konstanten fuer index_corpus.py und retrieve.py.

Beide Skripte muessen denselben Embedder und dieselbe Collection nutzen,
sonst passen Query-Vektoren nicht zu den gespeicherten und das Retrieval
liefert Muell. Deshalb leben beide Werte hier an einer Stelle.
"""
from __future__ import annotations

COLLECTION_NAME = "kolloquium_passages"
EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
