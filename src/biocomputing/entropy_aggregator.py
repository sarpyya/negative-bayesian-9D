from typing import Dict, Any, List
from src.biocomputing.eukaryote_gate import eukaryote_gate
from src.biocomputing.cosmo_bio_sync import cosmo_bio_sync

class MultiKingdomEntropyAggregator:
    """Aggregates entropy from all biological kingdoms and synchronizes with the cosmos."""
    
    def __init__(self):
        self.gate = eukaryote_gate
        self.sync = cosmo_bio_sync

    def aggregate_kingdom_entropy(self, string_vibration_freq: float) -> Dict[str, Any]:
        """Collects metrics from all kingdoms and computes the global bio-entropy."""
        bio_data = self.gate.get_all_eukaryote_data()
        
        # Calculate Kingdom-specific Sync
        kingdom_syncs = {}
        total_bio_entropy = 0.0
        
        for kingdom, metrics in bio_data.items():
            if kingdom == "origin": continue
            # Use specific markers as kingdom-entropy proxies
            k_entropy = metrics.get("cognitive_entropy", metrics.get("spore_entropy_distribution", 0.5))
            sync_data = self.sync.sync_vibration_to_growth(string_vibration_freq, k_entropy)
            kingdom_syncs[kingdom] = sync_data
            total_bio_entropy += k_entropy

        return {
            "kingdom_metrics": bio_data,
            "cosmic_synchronization": kingdom_syncs,
            "global_bio_entropy": total_bio_entropy / 4.0,
            "system_state": "SYNCHRONIZED" if total_bio_entropy < 3.0 else "BIO_HYPER_ENTROPY"
        }

bio_aggregator = MultiKingdomEntropyAggregator()
