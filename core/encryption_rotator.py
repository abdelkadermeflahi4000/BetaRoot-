# core/encryption_rotator.py
import os
import hashlib
from pathlib import Path
import asyncio

class EncryptionRotator:
    """يغير تشفير الملفات كل 10 ثواني"""
    
    def __init__(self, memory_dir: str = "data/memory"):
        self.memory_dir = Path(memory_dir)
        self.current_key = self._generate_key()

    def _generate_key(self):
        return hashlib.sha256(str(datetime.now().timestamp()).encode()).hexdigest()[:32]

    async def rotate(self):
        """تغيير المفتاح وإعادة تشفير الملفات"""
        self.current_key = self._generate_key()
        print(f"🔐 Encryption rotated | New key hash: {self.current_key[:8]}...")

        # هنا يمكن إضافة منطق إعادة التشفير الفعلي للملفات
        # في V1 نكتفي بالتدوير + تسجيل

    async def start_rotation(self):
        while True:
            await self.rotate()
            await asyncio.sleep(10)   # كل 10 ثواني
