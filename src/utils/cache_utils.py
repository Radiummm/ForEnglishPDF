from __future__ import annotations
import hashlib
import json
from typing import Any, Dict

class PageCache:
    def __init__(self):
        self._mem: Dict[str, Any] = {}

    def make_key(self, doc_hash: str, page_index: int, translation_style: str, tech_depth: str, glossary: Dict[str,str]) -> str:
        payload = {
            "doc": doc_hash,
            "page": page_index,
            "style": translation_style,
            "depth": tech_depth,
            "glossary": glossary,
        }
        raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(self, key: str):
        return self._mem.get(key)

    def set(self, key: str, value: Any):
        self._mem[key] = value

    def clear(self):
        self._mem.clear()
