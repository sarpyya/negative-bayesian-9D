import random
from typing import Dict, Any

class SyntheticDNAStorage:
    """Cold storage using nucleotide bases (A, T, C, G) for extreme long-term data preservation."""
    
    def __init__(self):
        self.strands = {}

    def synthesize_strand(self, label: str, data: str):
        """Encodes a string into a DNA strand."""
        # Convert to hex then to DNA
        hex_data = data.encode().hex()
        dna = ""
        mapping = {'0': 'AA', '1': 'AT', '2': 'AC', '3': 'AG', '4': 'TA', '5': 'TT', '6': 'TC', '7': 'TG', '8': 'CA', '9': 'CT', 'a': 'CC', 'b': 'CG', 'c': 'GA', 'd': 'GT', 'e': 'GC', 'f': 'GG'}
        for char in hex_data:
            dna += mapping.get(char, 'NN')
        
        self.strands[label] = {
            "dna": dna,
            "length": len(dna),
            "stability_index": random.uniform(0.9, 1.0)
        }

    def read_strand(self, label: str) -> str:
        return self.strands.get(label, {}).get("dna", "NONE")

    def get_dna_metrics(self) -> Dict[str, Any]:
        return {
            "strands_synthesized": len(self.strands),
            "total_bases": sum(s["length"] for s in self.strands.values()),
            "storage_type": "BIOLOGICAL_COLD_STORAGE"
        }

dna_storage = SyntheticDNAStorage()
