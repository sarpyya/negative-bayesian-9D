import random
from typing import Dict, Any

class BioCosmicHUD:
    """Visualizes the 12D Bio-Cosmic connection (Simulated Overlay)."""
    
    def generate_hud_overlay(self, bio_entropy_data: Dict[str, Any]) -> str:
        """Generates a text-based ASCII representation of the 12D Bio-Cosmic HUD."""
        entropy = bio_entropy_data.get("global_bio_entropy", 0.0)
        state = bio_entropy_data.get("system_state", "STABLE")
        
        hud = f"""
        [ 12D BIO-COSMIC INTERFACE ]
        -----------------------------------
        GLOBAL BIO-ENTROPY: {entropy:.4f}
        RESONANCE STATE: {state}
        
        [ KINGDOM STRANDS ]
        - HUMAN  : {'|' * int(entropy * 20)}
        - ANIMAL : {'|' * random.randint(5, 15)}
        - PLANT  : {'|' * random.randint(3, 10)}
        - FUNGI  : {'|' * int(bio_entropy_data['kingdom_metrics']['fungi']['spore_entropy_distribution'] * 20)}
        
        [ COSMOLOGICAL COUPLING ]
        ALPHA PHASE  : {random.uniform(0, 1):.2f} rad
        OMEGA SYNC   : {random.uniform(0.9, 1.0):.2f} %
        -----------------------------------
        """
        return hud

bio_hud = BioCosmicHUD()
