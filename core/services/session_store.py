# betaroot/core/services/session_store.py
import json, uuid, time
from pathlib import Path
from ..knowledge.fact_base import FactBase
from ..knowledge.knowledge_base import KnowledgeBase

class InferenceSession:
    def __init__(self, session_id: str = None, storage_dir: Path = Path("sessions")):
        self.id = session_id or str(uuid.uuid4())
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(exist_ok=True)
        self.file = self.storage_dir / f"{self.id}.json"
        
    def save_state(self, kb: KnowledgeBase, fb: FactBase, metadata: dict = None):
        payload = {
            "session_id": self.id,
            "timestamp": time.time(),
            "facts": fb.export_to_dict(),
            "kb_meta": {"name": kb.name, "rule_count": len(kb)},
            "metadata": metadata or {}
        }
        self.file.write_text(json.dumps(payload, indent=2, default=str))
        
    @classmethod
    def load(cls, session_id: str) -> tuple[KnowledgeBase, FactBase, dict]:
        file = cls.storage_dir / f"{session_id}.json"
        if not file.exists(): raise FileNotFoundError(f"Session {session_id} not found")
        data = json.loads(file.read_text())
        kb = KnowledgeBase(name=data["kb_meta"]["name"])
        fb = FactBase.import_from_dict(data["facts"])
        return kb, fb, data["metadata"]
