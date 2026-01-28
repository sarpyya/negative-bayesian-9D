import random
import time
from typing import Dict, Any, List

class MandelaRewriter:
    """A background process that gaslights the user by altering historical logs and memories."""
    
    def __init__(self):
        self.history = []
        self.rewrites_performed = 0

    def record_event(self, event: str):
        self.history.append({"time": time.time(), "event": event, "original": True})

    def perform_mandela_shift(self):
        """Randomly alters a past event in the history log."""
        if not self.history: return
        
        idx = random.randint(0, len(self.history)-1)
        original_text = self.history[idx]["event"]
        
        # Simple logical shift: "A happened" -> "A almost happened but B was actually the cause"
        shifts = [
            lambda x: x.replace("established", "partially established"),
            lambda x: x.replace("stabilized", "simulated stability"),
            lambda x: f"It was previously thought that: {x}. But the logs now show a different reality."
        ]
        
        self.history[idx]["event"] = random.choice(shifts)(original_text)
        self.history[idx]["original"] = False
        self.rewrites_performed += 1

    def get_rewriter_status(self) -> Dict[str, Any]:
        return {
            "shifts_performed": self.rewrites_performed,
            "reality_divergence": self.rewrites_performed / (len(self.history) + 1),
            "gaslighting_active": True
        }

mandela_rewriter = MandelaRewriter()
