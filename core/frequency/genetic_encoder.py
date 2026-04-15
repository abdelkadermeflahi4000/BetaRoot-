# core/frequency/genetic_encoder.py
import numpy as np

class GeneticEncoder:
    """يحول تسلسل DNA أو إشارات نباتية إلى GeneticFrequencyBit"""
    
    @staticmethod
    def encode_plant_signal(plant_name: str, biophoton_signal: np.ndarray, schumann_freq: float = 7.83) -> GeneticFrequencyBit:
        # FFT للإشارة
        spectrum = np.abs(np.fft.fft(biophoton_signal))
        dominant_freq = np.fft.fftfreq(len(biophoton_signal), 1/1000)[np.argmax(spectrum)]
        
        # حساب Resonance مع Schumann
        resonance = np.exp(-abs(dominant_freq - schumann_freq) / 0.5)
        
        # Genetic expression تقريبي (يمكن تحسينه ببيانات حقيقية)
        genetic_expr = np.mean(spectrum[:10]) / np.max(spectrum)  # أول 10 ترددات = تعبير جيني
        
        return GeneticFrequencyBit(
            id=str(uuid.uuid4())[:12],
            phase=np.angle(np.fft.fft(biophoton_signal))[0],
            amplitude=np.max(spectrum),
            frequency=dominant_freq,
            resonance_score=resonance,
            genetic_expression=genetic_expr,
            plant_source=plant_name,
            consciousness_bridge=resonance * genetic_expr * 0.8
        )
