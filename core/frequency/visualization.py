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
