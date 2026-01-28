import time
from typing import Dict, Any, List
from src.biocomputing.entropy_aggregator import bio_aggregator
from src.memory.cloud_memory import CloudMemoryManager
from src.quantum.kernel import QuantumKernel
from src.quantum.ethical_alignment import alignment_agent
from src.llm.llm_narrator import narrator
from src.core.core_engine import generar_grafo_9d, analizar_horror

class BayesianOrchestrator:
    """The central nervous system of the Bayesian Negative 9D engine."""
    
    def __init__(self):
        self.bio = bio_aggregator
        self.mem = CloudMemoryManager()
        self.quantum = QuantumKernel()
        self.ethics = alignment_agent
        self.narrator = narrator
        self.start_time = time.time()

    def quantum_bio_feedback(self, bio_entropy: float, quantum_stability: float):
        """Creates a feedback loop where quantum noise affects biological metabolism."""
        # High quantum noise increases neural liquid network time constants
        if quantum_stability < 0.3:
            from src.biocomputing.neural_liquid import liquid_brain
            liquid_brain.adapt_time_constants(bio_entropy * 100)
            print(" [FEEDBACK]: Quantum Decoherence affecting Neural Liquid Network.")

    def run_resonance_cycle(self, seed: int, cosmic_freq: float = 440.0) -> Dict[str, Any]:
        """Runs a complete resonance cycle across all tiers."""
        
        # 1. Gather Bio-Entropy (Kingdoms & Cosmo-Sync)
        bio_results = self.bio.aggregate_kingdom_entropy(string_vibration_freq=cosmic_freq)
        bio_entropy = bio_results['global_bio_entropy']
        
        # 2. Gather Infra & Exotic Memory Metrics
        mem_metrics = self.mem.get_infrastructure_memory_metrics()
        exotic_states = mem_metrics['exotic_metrics']
        
        # 3. Quantum Tension Calculation
        base_weights = {i: 1.0 + bio_entropy for i in range(1, 13)}
        quantum_weights = self.quantum.calculate_9d_tensions(base_weights)
        q_stability = mem_metrics.get('core_stability', 0.5) # Proxy for stability

        # 4. Feedback Loop
        self.quantum_bio_feedback(bio_entropy, q_stability)
        
        # 5. Ethical Risk Assessment
        session_mins = (time.time() - self.start_time) / 60
        risk = self.ethics.assess_risk(sum(quantum_weights.values()) * 10000, session_mins)
        
        if risk['quarantine_active']:
             return {"status": "QUARANTINED", "reason": risk['recommendation']}

        # 6. Core Graph Generation (Influenced by ALL tiers)
        G = generar_grafo_9d(
            seed=seed, 
            initial_horror_weights=quantum_weights,
            ramificaciones_por_nodo=int(8 + bio_entropy * 5)
        )
        
        analisis = analizar_horror(G)
        
        # 7. Narrative Generation (PERSONA)
        # Inject collective trauma from Akashic Registry if available
        exotic_context = f"COLLECTIVE_TRAUMA: {self.mem.akashic.inhale_collective_memory()}"
        
        narrative_gen = self.narrator.generate_narrative({
            'seed': seed,
            'horror_total': analisis['horror_total'],
            'total_nodos': analisis['total_nodos'],
            'modo': analisis['modo'],
            'bio_state': bio_results['system_state'],
            'exotic_memory': exotic_states['time_crystals']['persistence_active'],
            'exotic_context': exotic_context
        })
        
        return {
            "seed": seed,
            "graph": G,
            "analysis": analisis,
            "biological_context": bio_results,
            "memory_substrate": mem_metrics,
            "ethical_risk": risk,
            "persona_narrative": narrative_gen
        }

# Helper to provide random if not imported
import random
orchestrator = BayesianOrchestrator()
