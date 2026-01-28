from typing import Dict, Any, List

class NeuroSymbolicValidator:
    """Fuses LLM creativity with rigid logical rules (Prolog-style)."""
    
    def __init__(self):
        self.rules = {
            "entropy_law": lambda e: e >= 0,
            "dimension_bound": lambda d: 1 <= d <= 11,
            "horror_positivity": lambda h: h >= 0,
            "probability_bound": lambda p: 0.0 <= p <= 1.0,
            "causality": lambda cause, effect: cause <= effect
        }
        self.violations = []

    def validate_statement(self, statement: str, context: Dict[str, float]) -> Dict[str, Any]:
        """Validates an LLM-generated statement against physics rules."""
        self.violations = []
        
        # Check dimension claims
        if "dimension" in statement.lower():
            d = context.get("dimensions", 9)
            if not self.rules["dimension_bound"](d):
                self.violations.append(f"DIMENSION_VIOLATION: {d} is out of bounds [1,11]")
        
        # Check entropy claims
        if "entropy" in statement.lower() or "negentropy" in statement.lower():
            e = context.get("entropy", 0)
            if not self.rules["entropy_law"](e):
                self.violations.append(f"ENTROPY_VIOLATION: Negative entropy {e} is forbidden")
        
        # Check probability claims
        if "probability" in statement.lower() or "%" in statement:
            p = context.get("probability", 0.5)
            if not self.rules["probability_bound"](p):
                self.violations.append(f"PROBABILITY_VIOLATION: {p} is not in [0,1]")

        return {
            "valid": len(self.violations) == 0,
            "violations": self.violations,
            "statement": statement[:100] + "..." if len(statement) > 100 else statement,
            "method": "NEURO_SYMBOLIC_VALIDATION"
        }

    def inject_rule(self, name: str, rule_fn):
        """Adds a new physics rule to the validator."""
        self.rules[name] = rule_fn

neuro_validator = NeuroSymbolicValidator()
