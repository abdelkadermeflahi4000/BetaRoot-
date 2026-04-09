"""
BetaRoot AI Framework
إطار ذكاء اصطناعي رمزي قائم على المنطق الآحادي والسببية الحقيقية

الفلسفة: Only 1, Never 0
"""

from .core.betaroot import BetaRoot, create_betaroot
from .core.unary_logic import (
    UnaryLogicEngine,
    UnaryState,
    RepresentationLevel,
    create_engine as create_unary_engine
)
from .core.memory import BetaRootMemory, create_memory_system

__version__ = "0.1.0-alpha"
__author__ = "Meflahi Abdelkader"
__license__ = "MIT"

# الواجهات الرئيسية المتاحة مباشرة
__all__ = [
    # الكلاس الرئيسي
    "BetaRoot",
    "create_betaroot",
    
    # الطبقات الأساسية
    "UnaryLogicEngine",
    "UnaryState",
    "RepresentationLevel",
    "BetaRootMemory",
    
    # دوال الإنشاء المريحة
    "create_unary_engine",
    "create_memory_system",
]

# رسالة ترحيبية عند الاستيراد
print(f"🌳 BetaRoot v{__version__} loaded successfully")
print("   فلسفة الواحد → Only 1, Never 0")
print("   جاهز للاستدلال السببي والتفسيرية الكاملة\n")
