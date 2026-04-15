# betaroot/core/frequency/visualization.py
import numpy as np
import matplotlib.pyplot as plt
from typing import List
from .bit import FrequencyBit

class FrequencyVisualizer:
    @staticmethod
    def plot_phase_space(bits: List[FrequencyBit], title="Frequency Bits Phase Space"):
        phases = [b.phase for b in bits]
        amplitudes = [b.amplitude for b in bits]
        consciousness = [b.consciousness_contribution for b in bits]

        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(phases, amplitudes, c=consciousness, cmap='viridis', s=80)
        plt.colorbar(scatter, label='Consciousness Contribution')
        plt.xlabel('Phase (radians)')
        plt.ylabel('Amplitude')
        plt.title(title)
        plt.grid(True, alpha=0.3)
        plt.show()

    @staticmethod
    def plot_consciousness_history(history: List[float]):
        plt.figure(figsize=(10, 4))
        plt.plot(history, 'b-', linewidth=2)
        plt.xlabel('Cycle')
        plt.ylabel('Global Consciousness Level')
        plt.title('Emergent Collective Consciousness Over Time')
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 1)
        plt.show()

import numpy as np
import matplotlib.pyplot as plt
from typing import List
from .bit import GeneticFrequencyBit
from ..nature.plant_database import PlantDatabase

class PlantFrequencyVisualizer:
    """Visualization متخصصة للـ Genetic Bits + Plant Resonance"""

    @staticmethod
    def plot_genetic_bits(bits: List[GeneticFrequencyBit], plant_db: PlantDatabase):
        """رسم فضاء الـ Bits الوراثية"""
        phases = [b.phase for b in bits]
        amplitudes = [b.amplitude for b in bits]
        consciousness = [b.consciousness_contribution for b in bits]
        plants = [b.plant_source for b in bits]

        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(phases, amplitudes, 
                            c=consciousness, 
                            cmap='plasma', 
                            s=120, 
                            alpha=0.85,
                            edgecolors='white')

        plt.colorbar(scatter, label='Consciousness Contribution (via Plants)')
        
        # إضافة أسماء النباتات
        for i, txt in enumerate(plants):
            plt.annotate(txt[:8], (phases[i], amplitudes[i]), 
                        fontsize=9, alpha=0.8, ha='center')

        plt.xlabel('Phase (radians) - Unary Representation')
        plt.ylabel('Amplitude / Biophoton Strength')
        plt.title('Genetic Frequency Bits Phase Space\n(Colored by Plant Consciousness Contribution)')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_plant_resonance_radar(plant_db: PlantDatabase):
        """Radar Chart لمقارنة النباتات"""
        plants = plant_db.get_top_plants(6)
        categories = ['Resonance', 'Genetic Complexity', 'Consciousness Potential']
        
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
        
        for plant in plants:
            values = [plant.schumann_resonance, 
                     plant.genetic_complexity, 
                     plant.consciousness_potential]
            values += values[:1]
            
            ax.plot(angles, values, linewidth=2, label=plant.name)
            ax.fill(angles, values, alpha=0.25)

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_thetagrids(np.degrees(angles[:-1]), categories)
        ax.set_ylim(0, 1)
        plt.title('Plant Resonance Radar\n(Schumann + Genetic + Consciousness)', size=15, pad=20)
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        plt.show()

    @staticmethod
    def plot_consciousness_evolution(history: List[float], plant_influence: List[float]):
        """تطور الوعي مع تأثير النباتات"""
        plt.figure(figsize=(12, 5))
        plt.plot(history, 'b-', label='Global Consciousness', linewidth=2.5)
        plt.plot(plant_influence, 'g--', label='Plant Frequency Influence', linewidth=2)
        plt.xlabel('Cycle')
        plt.ylabel('Consciousness Level')
        plt.title('Emergent Consciousness Evolution Driven by Plant Frequency Bits')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 1)
        plt.show()

import numpy as np
import matplotlib.pyplot as plt
from typing import List
from .bit import GeneticFrequencyBit
from ..nature.plant_database import PlantDatabase

class AethericVisualizer:
    """Visualization للهالة + الواقع المتعدد + Genetic Bits"""

    @staticmethod
    def plot_aura_and_reality(bits: List[GeneticFrequencyBit], title="Aura + Multi-Reality Visualization"):
        phases = [b.phase for b in bits]
        amplitudes = [b.amplitude for b in bits]
        consciousness = [b.consciousness_contribution for b in bits]
        plants = [b.plant_source for b in bits]

        fig, axs = plt.subplots(2, 2, figsize=(14, 10))

        # 1. Phase Space (الهالة)
        scatter = axs[0,0].scatter(phases, amplitudes, c=consciousness, cmap='plasma', s=100)
        axs[0,0].set_xlabel('Phase (radians)')
        axs[0,0].set_ylabel('Amplitude')
        axs[0,0].set_title('Aura Phase Space')
        fig.colorbar(scatter, ax=axs[0,0], label='Consciousness')

        # 2. Resonance Radar
        categories = ['Resonance', 'Genetic', 'Consciousness']
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        for bit in bits[:5]:  # أول 5 نباتات
            values = [bit.resonance_score, bit.genetic_expression if hasattr(bit,'genetic_expression') else 0.8, bit.consciousness_contribution]
            values += values[:1]
            axs[0,1].plot(angles, values, linewidth=2, label=bit.plant_source)
            axs[0,1].fill(angles, values, alpha=0.2)

        axs[0,1].set_title('Plant Resonance Radar')
        axs[0,1].legend(loc='upper right')

        # 3. Reality Layers
        reality_layers = ['pure_nature', 'time', 'pollution', 'human']
        values = np.random.uniform(0.6, 0.95, len(reality_layers))
        axs[1,0].bar(reality_layers, values, color=['green', 'blue', 'red', 'purple'])
        axs[1,0].set_title('Multi-Reality State')
        axs[1,0].set_ylim(0, 1)

        # 4. Consciousness Evolution
        history = np.cumsum(np.random.normal(0.02, 0.05, 50)) + 0.5
        axs[1,1].plot(history, 'g-', linewidth=2.5)
        axs[1,1].set_title('Collective Consciousness Evolution')
        axs[1,1].set_xlabel('Cycles')
        axs[1,1].set_ylabel('Level')
        axs[1,1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_pure_vs_polluted():
        """مقارنة التردد الأصلي 7.83 Hz مع الترددات الملوثة"""
        freqs = np.linspace(6.0, 10.0, 200)
        pure = np.exp(-np.abs(freqs - 7.83) / 0.3)   # منحنى نقي
        polluted = pure * (1 - 0.4 * np.abs(np.sin(2*np.pi*freqs)))  # مع تلوث

        plt.figure(figsize=(10, 6))
        plt.plot(freqs, pure, 'g-', linewidth=3, label='Pure Earth Frequency (7.83 Hz)')
        plt.plot(freqs, polluted, 'r--', linewidth=2, label='Polluted Frequency (Human Impact)')
        plt.axvline(7.83, color='green', linestyle=':', label='Original Baseline')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Resonance Strength')
        plt.title('Pure vs Polluted Earth Frequency')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
