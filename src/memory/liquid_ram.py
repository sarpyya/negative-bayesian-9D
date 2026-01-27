import random
import numpy as np
from typing import Dict, Any, List

class LiquidRAM:
    """Memory with viscosity; data flows and mixes as system horror increase."""
    
    def __init__(self, size: int = 100):
        self.cells = [random.uniform(0, 1) for _ in range(size)]
        self.viscosity = 1.0 # 1.0 = solid, 0.0 = fluid

    def update_viscosity(self, horror_level: float):
        """As horror increases, memory becomes more fluid and data bleeds."""
        self.viscosity = max(0.1, 1.0 - (horror_level / 200000.0))

    def flow_step(self):
        """Simulates data 'bleeding' between adjacent memory cells."""
        if self.viscosity < 0.9:
            bleed_rate = 1.0 - self.viscosity
            new_cells = []
            for i in range(len(self.cells)):
                prev_idx = (i - 1) % len(self.cells)
                next_idx = (i + 1) % len(self.cells)
                avg = (self.cells[i] + self.cells[prev_idx] * bleed_rate + self.cells[next_idx] * bleed_rate) / (1 + 2 * bleed_rate)
                new_cells.append(avg)
            self.cells = new_cells

    def get_liquid_status(self) -> Dict[str, Any]:
        return {
            "viscosity": self.viscosity,
            "fluid_state": "SOLID" if self.viscosity > 0.8 else "VISCOUS" if self.viscosity > 0.4 else "AQUEOUS",
            "diffusion_rate": 1.0 - self.viscosity
        }

liquid_ram = LiquidRAM()
