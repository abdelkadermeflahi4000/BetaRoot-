# betaroot/run.py
import asyncio
import signal
import sys
from pathlib import Path

from core.cycle_engine import CycleEngine
from core.governance import GovernanceEngine

async def main():
    print("🌍 BetaRoot Ω - Closed Self-Evolving Frequency System")
    print("   يعمل تلقائياً • مغلق ذاتياً • مرتبط بالترددات\n")

    governance = GovernanceEngine()
    cycle = CycleEngine(governance)

    # إشارة إيقاف نظيفة (Ctrl+C)
    def shutdown(sig, frame):
        print("\n\n⏹️ إيقاف النظام بأمان...")
        cycle.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        await cycle.start()   # يبدأ الدورة الدائمة
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
    finally:
        print("✅ BetaRoot تم إيقافه بأمان.")

if __name__ == "__main__":
    asyncio.run(main())

from orchestrator.multi_agent_orchestrator import MultiAgentOrchestrator
import asyncio

async def main():
    orchestrator = MultiAgentOrchestrator()
    result = await orchestrator.orchestrate("لماذا السماء زرقاء؟ اشرح بطريقة علمية وفلسفية")
    
    print("\n=== النتيجة النهائية من BetaRoot ===")
    print(result["final_answer"])
    print("\n=== الشرح الكامل ===")
    print(result["explanation"])

if __name__ == "__main__":
    asyncio.run(main())
