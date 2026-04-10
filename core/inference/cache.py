# betaroot/core/inference/cache.py
import hashlib, time
from typing import Optional, Dict
from dataclasses import dataclass

@dataclass
class CacheEntry:
    result: Dict
    timestamp: float
    ttl: int = 300  # 5 دقائق افتراضياً

class InferenceCache:
    def __init__(self, max_size: int = 1000):
        self._cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        
    def _make_key(self, query: str, evidence: Dict) -> str:
        raw = f"{query}::{hash(frozenset(evidence.items()))}"
        return hashlib.sha256(raw.encode()).hexdigest()
        
    def get(self, query: str, evidence: Dict) -> Optional[Dict]:
        key = self._make_key(query, evidence)
        entry = self._cache.get(key)
        if entry and time.time() - entry.timestamp < entry.ttl:
            return entry.result
        if entry: del self._cache[key]  # منتهي الصلاحية
        return None
        
    def put(self, query: str, evidence: Dict, result: Dict, ttl: int = 300):
        if len(self._cache) >= self.max_size:
            oldest = min(self._cache, key=lambda k: self._cache[k].timestamp)
            del self._cache[oldest]
        key = self._make_key(query, evidence)
        self._cache[key] = CacheEntry(result, time.time(), ttl)
