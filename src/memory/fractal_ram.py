import random
from typing import Dict, Any, List

class FractalRAM:
    """Recursive data structures where each memory block contains a nested simulation state."""
    
    def __init__(self, depth: int = 3):
        self.depth = depth
        self.structure = self._generate_fractal(depth)

    def _generate_fractal(self, depth: int) -> Dict[str, Any]:
        if depth <= 0:
            return {"data": random.uniform(0, 1), "type": "LEAF"}
        return {
            "sub_sim_1": self._generate_fractal(depth - 1),
            "sub_sim_2": self._generate_fractal(depth - 1),
            "recursion_level": depth,
            "type": "NODE"
        }

    def access_sub_reality(self, path: List[str]) -> Dict[str, Any]:
        """Traverses the fractal structure to find a nested reality."""
        current = self.structure
        for step in path:
            if step in current:
                current = current[step]
            else:
                return {"error": "REALITY_NOT_FOUND"}
        return current

    def get_fractal_metrics(self) -> Dict[str, Any]:
        return {
            "max_recursion_depth": self.depth,
            "total_nested_realities": 2**self.depth,
            "topology": "RECURSIVE_FRACTAL"
        }

fractal_ram = FractalRAM()
