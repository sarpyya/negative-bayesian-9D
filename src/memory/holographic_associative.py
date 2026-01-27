import numpy as np
import hashlib
from typing import Dict, Any, List

class HolographicAssociativeMemory:
    """Retrieves data based on semantic/emotional similarity instead of strict keys."""
    
    def __init__(self, dimension: int = 128):
        self.dimension = dimension
        self.memory_matrix = np.zeros((dimension, dimension))
        self.stored_traumas = []

    def _vectorize(self, text: str) -> np.ndarray:
        # Simple deterministic vectorization for mock purposes
        hash_val = hashlib.sha256(text.encode()).digest()
        vec = np.frombuffer(hash_val * (self.dimension // 32 + 1), dtype=np.uint8)[:self.dimension]
        return (vec.astype(float) / 255.0) * 2 - 1

    def store_memory_hologram(self, description: str, data: Any):
        """Stores a 'trauma' in the holographic matrix."""
        vec = self._vectorize(description)
        # Outer product to simulate holographic storage
        self.memory_matrix += np.outer(vec, vec)
        self.stored_traumas.append({"vec": vec, "data": data, "desc": description})

    def retrieve_by_resonance(self, current_state_desc: str) -> List[Dict[str, Any]]:
        """Finds memories that 'resonate' with the current state."""
        query_vec = self._vectorize(current_state_desc)
        results = []
        for t in self.stored_traumas:
            similarity = np.dot(query_vec, t["vec"]) / (np.linalg.norm(query_vec) * np.linalg.norm(t["vec"]))
            if similarity > 0.7:
                results.append({"data": t["data"], "resonance": float(similarity)})
        return sorted(results, key=lambda x: x["resonance"], reverse=True)

    def get_ham_status(self) -> Dict[str, Any]:
        return {
            "stored_holograms": len(self.stored_traumas),
            "matrix_rank": int(np.linalg.matrix_rank(self.memory_matrix)),
            "retrieval_mode": "SEMANTIC_RESONANCE"
        }

ham_memory = HolographicAssociativeMemory()
