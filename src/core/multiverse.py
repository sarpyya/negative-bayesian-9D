import random
import networkx as nx
from typing import List, Dict, Any

class MultiverseEngine:
    """Manages parallel timelines branching from critical nodes."""
    def __init__(self):
        self.timelines = {} # seed -> {branches: [], parent: seed}

    def detect_chp(self, G: nx.DiGraph, threshold: float = 50000.0) -> List[str]:
        """Detects Critical Horror Points (CHP) where a branching could occur."""
        chps = [n for n, d in G.nodes(data=True) if d.get('horror', 0) > threshold]
        return chps

    def spawn_parallel_timeline(self, parent_seed: int, node_id: str) -> int:
        """Spawns a new timeline (seed) based on a specific node's state."""
        # The new seed is a deterministic but mutated version of the parent + node offset
        branch_seed = parent_seed + hash(node_id) % 1000000
        
        if parent_seed not in self.timelines:
            self.timelines[parent_seed] = {"branches": [], "parent": None}
            
        self.timelines[parent_seed]["branches"].append({
            "node_origin": node_id,
            "branch_seed": branch_seed
        })
        
        self.timelines[branch_seed] = {"branches": [], "parent": parent_seed}
        return branch_seed

    def get_timeline_dissonance(self, s1_analysis: dict, s2_analysis: dict) -> float:
        """Calculates the distance/difference between two parallel realities."""
        h1 = s1_analysis.get('horror_total', 0)
        h2 = s2_analysis.get('horror_total', 0)
        return abs(h1 - h2) / ((h1 + h2) / 2 + 1)
