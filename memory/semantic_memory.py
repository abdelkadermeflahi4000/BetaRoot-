# betaroot/memory/semantic_memory.py
"""
Semantic Memory Module for BetaRoot
Supports vector embeddings, semantic indexing, and meaning-based retrieval.
Transforms memory from "keyword matching" to "concept understanding".

Features:
- Pluggable embedding models (Lightweight fallback → Production SentenceTransformers)
- Fast cosine similarity search with threshold filtering
- Semantic relationship discovery & concept linking
- Persistent vector index + text cache
- Seamless integration with MemoryManager

Author: BetaRoot Team
Date: April 2026
"""
import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import logging
from .types import MemoryItem

logger = logging.getLogger(__name__)


# ==========================================
# 📦 1. نماذج التضمين (Embedding Models)
# ==========================================
class BaseEmbeddingModel:
    """واجهة أساسية لنماذج التضمين المتجهي"""
    def encode(self, texts: List[str]) -> np.ndarray: raise NotImplementedError
    @property
    def dim(self) -> int: raise NotImplementedError


class SentenceTransformerModel(BaseEmbeddingModel):
    """نموذج إنتاجي دقيق (يحتاج pip install sentence-transformers)"""
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
            self._dim = self.model.get_sentence_embedding_dimension()
        except ImportError:
            raise ImportError("sentence-transformers غير مثبت. شغّل: pip install sentence-transformers")
    
    def encode(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, normalize_embeddings=True)
    
    @property
    def dim(self) -> int: return self._dim


class LightweightHashModel(BaseEmbeddingModel):
    """نموذج خفيف صفر الاعتماديات (Fallback للعمل فوراً دون مكتبات خارجية)"""
    def __init__(self, dim: int = 128):
        self._dim = dim
        self._vocab: Dict[str, int] = {}
    
    def encode(self, texts: List[str]) -> np.ndarray:
        embeddings = []
        for text in texts:
            vec = np.zeros(self._dim)
            for token in text.lower().split():
                h = hash(token) % self._dim
                vec[h] += 1.0
            norm = np.linalg.norm(vec)
            if norm > 0: vec /= norm
            embeddings.append(vec)
        return np.array(embeddings)
    
    @property
    def dim(self) -> int: return self._dim


# ==========================================
# 📐 2. الفهرس المتجهي (Vector Index)
# ==========================================
class VectorIndex:
    """فهرس متجهي سريع للبحث الدلالي باستخدام تشابه جيب التمام (Cosine Similarity)"""
    def __init__(self, dim: int, storage_path: Optional[str] = None):
        self.dim = dim
        self.vectors = np.empty((0, dim))
        self.ids: List[str] = []
        self.meta: Dict[str, Dict] = {}
        self.path = Path(storage_path) if storage_path else None
        if self.path and self.path.with_suffix('.npy').exists():
            self.load()

    def add(self, item_id: str, vec: np.ndarray, meta: Dict = None):
        if vec.shape != (self.dim,):
            raise ValueError(f"Dimension mismatch: expected {self.dim}, got {vec.shape}")
        self.vectors = np.vstack([self.vectors, vec.reshape(1, -1)])
        self.ids.append(item_id)
        self.meta[item_id] = meta or {}

    def search(self, query_vec: np.ndarray, top_k: int = 5, threshold: float = 0.25) -> List[Tuple[str, float]]:
        """بحث دلالي سريع. المتجهات مُطَبَّعة مسبقاً → الضرب النقطي = تشابه جيب التمام"""
        if len(self.ids) == 0: return []
        sims = self.vectors @ query_vec
        mask = sims >= threshold
        if not np.any(mask): return []
        idx = np.argsort(-sims[mask])[:top_k]
        return [(self.ids[i], float(sims[mask][i])) for i in idx]

    def save(self):
        if not self.path: return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        np.save(self.path.with_suffix('.npy'), self.vectors)
        with open(self.path.with_suffix('.json'), 'w', encoding='utf-8') as f:
            json.dump({"ids": self.ids, "meta": self.meta}, f, ensure_ascii=False, indent=2)

    def load(self):
        self.vectors = np.load(self.path.with_suffix('.npy'))
        with open(self.path.with_suffix('.json'), 'r', encoding='utf-8') as f:
            d = json.load(f)
            self.ids = d["ids"]
            self.meta = d["meta"]


# ==========================================
# 🧠 3. مدير الذاكرة الدلالية (Semantic Memory)
# ==========================================
class SemanticMemory:
    """
    الواجهة العليا للذاكرة الدلالية
    تربط التضمين المتجهي، الفهرسة، واكتشاف العلاقات المعنوية
    """
    def __init__(self, model: Optional[BaseEmbeddingModel] = None, storage_dir: Optional[str] = None):
        self.model = model or LightweightHashModel(dim=128)
        self.index = VectorIndex(dim=self.model.dim, storage_path=f"{storage_dir}/semantic_index" if storage_dir else None)
        self.text_cache: Dict[str, str] = {}
        self._load_cache()
        logger.info(f"SemanticMemory initialized (dim={self.model.dim}, engine={self.model.__class__.__name__})")

    def index_item(self, item: MemoryItem) -> None:
        """ترميز وفهرسة عنصر ذاكرة جديد"""
        text = self._to_text(item)
        if not text or item.id in self.text_cache: return
        
        self.text_cache[item.id] = text
        vec = self.model.encode([text])[0]
        self.index.add(item.id, vec, {"type": item.memory_type.value, "tags": item.tags, "trust": item.trust.name})
        self.index.save()
        self._save_cache()
        logger.debug(f"Indexed semantic vector for {item.id}")

    def semantic_search(self, query: str, top_k: int = 5, threshold: float = 0.3) -> List[Dict]:
        """بحث دلالي نصي: يعيد العناصر الأقرب معنويًا للاستعلام"""
        vec = self.model.encode([query])[0]
        results = self.index.search(vec, top_k, threshold)
        return [{"id": rid, "score": s, "meta": self.index.meta.get(rid, {})} for rid, s in results]

    def get_related_items(self, item_id: str, top_k: int = 3) -> List[str]:
        """اكتشاف العناصر المرتبطة دلاليًا بعنصر معين (Concept Linking)"""
        if item_id not in self.text_cache: return []
        vec = self.model.encode([self.text_cache[item_id]])[0]
        res = self.index.search(vec, top_k + 1, 0.0)  # +1 لاستبعاد العنصر نفسه
        return [r[0] for r in res if r[0] != item_id][:top_k]

    def _to_text(self, item: MemoryItem) -> str:
        """تحويل محتوى عنصر الذاكرة إلى نص قابل للترميز"""
        if isinstance(item.content, dict):
            return " ".join(f"{k}: {v}" for k, v in item.content.items())
        return str(item.content)

    def _save_cache(self):
        if self.index.path:
            with open(self.index.path.with_suffix('.cache.json'), 'w', encoding='utf-8') as f:
                json.dump(self.text_cache, f, ensure_ascii=False, indent=2)

    def _load_cache(self):
        cache_path = self.index.path.with_suffix('.cache.json') if self.index.path else None
        if cache_path and cache_path.exists():
            with open(cache_path, 'r', encoding='utf-8') as f:
                self.text_cache = json.load(f)

    def stats(self) -> Dict[str, Any]:
        return {
            "indexed_items": len(self.ids),
            "vector_dim": self.model.dim,
            "model_type": self.model.__class__.__name__,
            "storage_path": str(self.index.path) if self.index.path else "memory_only"
        }
