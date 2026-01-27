import random
from typing import Dict, Any, List

class SynapticRAM:
    """Uses the weights of the simulated C. elegans neural network as short-term memory."""
    
    def __init__(self, neurons: int = 302):
        self.neurons = neurons
        self.synapses = [[random.uniform(-0.1, 0.1) for _ in range(neurons)] for _ in range(neurons)]
        self.data_map = {}

    def encode_to_synapse(self, key: str, value: float):
        """Encodes a numeric value into a specific synaptic path."""
        # Map key to a neuron pair
        idx_a = hash(key) % self.neurons
        idx_b = (hash(key) // self.neurons) % self.neurons
        self.synapses[idx_a][idx_b] = value
        self.data_map[key] = (idx_a, idx_b)

    def decode_from_synapse(self, key: str) -> float:
        if key in self.data_map:
            idx_a, idx_b = self.data_map[key]
            return self.synapses[idx_a][idx_b]
        return 0.0

    def decay_memory(self):
        """Simulates biological forgetting by decaying weights toward zero."""
        for i in range(self.neurons):
            for j in range(self.neurons):
                self.synapses[i][j] *= 0.99 

    def get_synaptic_status(self) -> Dict[str, Any]:
        return {
            "active_synapses": len(self.data_map),
            "plasticity": 0.85,
            "neuron_load": len(self.data_map) / self.neurons
        }

synaptic_memory = SynapticRAM()
