# examples/intellectual_closure_earth_shape.py
from core.causal_graph import CausalGraph
from memory.knowledge_base import PersistentKnowledgeBase

graph = CausalGraph()
graph.add_causal_link(
    cause="إغلاق_فكري",
    effect="نفي_عدد_الأيام",
    certainty=1,
    explanation="الإغلاق يمنع النظر إلى الزمن الخطي (365 يوم) ويحول التركيز إلى الدورات"
)

graph.add_causal_link(
    cause="نفي_عدد_الأيام",
    effect="تركيز_حصري_على_الفصول_والدورات_والنانو_وتردداتها",
    certainty=1,
    explanation="الواقع يُرى كدورات حياة واهتزازات مجهرية بدلاً من شكل هندسي ثابت"
)

graph.add_causal_link(
    cause="تركيز_حصري_على_الفصول_والدورات_والنانو_وتردداتها",
    effect="توهم_الشكل_الكروي_للأرض",
    certainty=1,
    explanation="التركيز على المستوى النانوي/الترددي يجعل الشكل الميكروسكوبي يطغى على الشكل الكلي"
)

# حفظ في الذاكرة المستمرة
kb = PersistentKnowledgeBase()
kb.store(graph, tags=["فلسفة", "سببية_الأرض", "ترددات_نانو", "دورات_حياة"])
