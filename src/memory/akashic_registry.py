import random
from typing import Dict, Any, List

class AkashicRegistry:
    """A global collective memory pool that simulates leakage between different simulation runs."""
    
    def __init__(self):
        self.global_pool = [
            "User 0xF3 saw the Void in session 202",
            "The 11D manifold collapsed at seed 4401",
            "Memetic infection detected in GCP-Central nodes"
        ]

    def record_global_event(self, event_desc: str):
        """Adds an event to the collective consciousness."""
        self.global_pool.append(event_desc)
        if len(self.global_pool) > 100:
            self.global_pool.pop(0)

    def inhale_collective_memory(self) -> str:
        """Retrieves a random 'inherited' memory from the pool."""
        return random.choice(self.global_pool)

    def get_registry_status(self) -> Dict[str, Any]:
        return {
            "collective_events_stored": len(self.global_pool),
            "cross_linkage_active": True,
            "origin": "UNIVERSAL_ARCHIVE"
        }

akashic_registry = AkashicRegistry()
