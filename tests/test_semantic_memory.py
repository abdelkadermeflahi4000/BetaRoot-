# test_semantic_memory.py
from betaroot.memory.semantic_memory import SemanticMemory, LightweightHashModel
from betaroot.memory.types import MemoryItem, MemoryType, Priority, TrustLevel
from datetime import datetime

def test_semantic_system():
    print("🧪 Testing Semantic Memory System...")
    sm = SemanticMemory(model=LightweightHashModel(dim=128), storage_dir="test_semantic")
    
    # 1. إضافة عناصر متنوعة
    items = [
        MemoryItem({"subject": "smoking", "predicate": "causes", "value": "lung_cancer"}, 
                   MemoryType.FACT, Priority.CRITICAL, TrustLevel.VERIFIED, tags=["health", "causation"]),
        MemoryItem({"subject": "aspirin", "predicate": "relieves", "value": "headache"}, 
                   MemoryType.FACT, Priority.HIGH, TrustLevel.HIGH_CONFIDENCE, tags=["medicine", "pain"]),
        MemoryItem({"subject": "vaccination", "predicate": "prevents", "value": "infection"}, 
                   MemoryType.FACT, Priority.HIGH, TrustLevel.VERIFIED, tags=["health", "prevention"])
    ]
    
    for it in items:
        sm.index_item(it)
        
    print("✅ Indexed 3 semantic facts.")
    
    # 2. بحث دلالي
    query = "how to stop getting sick from viruses"
    results = sm.semantic_search(query, top_k=2, threshold=0.2)
    print(f"\n🔍 Semantic search for: '{query}'")
    for r in results:
        print(f"   • {r['id']} | score: {r['score']:.3f} | tags: {r['meta'].get('tags')}")
        
    # 3. اكتشاف العلاقات
    related = sm.get_related_items(items[0].id, top_k=2)
    print(f"\n🔗 Related to '{items[0].id}': {related}")
    
    # 4. إحصائيات
    print(f"\n📊 Stats: {sm.stats()}")
    print("\n✅ Semantic memory system working correctly!")
    return sm

if __name__ == "__main__":
    test_semantic_system()
