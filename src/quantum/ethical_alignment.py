from typing import Dict, Any

class EthicalAlignmentAgent:
    """Monitors simulation for psychologically unsafe horror levels."""
    
    HORROR_THRESHOLDS = {
        "safe": 50000,
        "caution": 100000,
        "warning": 150000,
        "critical": 200000,
        "quarantine": 250000
    }
    
    def __init__(self):
        self.quarantine_active = False
        self.warnings_issued = 0
        self.observer_stress_estimate = 0.0

    def assess_risk(self, horror: float, session_duration_minutes: float) -> Dict[str, Any]:
        """Assesses the psychological risk to the observer."""
        # Fatigue increases risk
        fatigue_factor = 1 + (session_duration_minutes / 60) * 0.5
        adjusted_horror = horror * fatigue_factor
        
        risk_level = "SAFE"
        for level, threshold in sorted(self.HORROR_THRESHOLDS.items(), key=lambda x: x[1], reverse=True):
            if adjusted_horror >= threshold:
                risk_level = level.upper()
                break
        
        self.observer_stress_estimate = min(1.0, adjusted_horror / self.HORROR_THRESHOLDS["quarantine"])
        
        if risk_level == "QUARANTINE":
            self.quarantine_active = True
            self.warnings_issued += 1
        
        return {
            "risk_level": risk_level,
            "adjusted_horror": adjusted_horror,
            "fatigue_factor": fatigue_factor,
            "stress_estimate": self.observer_stress_estimate,
            "quarantine_active": self.quarantine_active,
            "recommendation": self._get_recommendation(risk_level)
        }

    def _get_recommendation(self, risk_level: str) -> str:
        recommendations = {
            "SAFE": "Continue observation.",
            "CAUTION": "Brief breaks recommended.",
            "WARNING": "Reduce session length. Increase ambient lighting.",
            "CRITICAL": "Immediate break advised. Grounding exercises.",
            "QUARANTINE": "SIMULATION PAUSED. Ontological risk detected. Step away from screen."
        }
        return recommendations.get(risk_level, "Unknown risk state.")

    def lift_quarantine(self, confirmation_code: str) -> bool:
        """Allows resumption after quarantine with user confirmation."""
        if confirmation_code == "I_ACCEPT_THE_VOID":
            self.quarantine_active = False
            return True
        return False

alignment_agent = EthicalAlignmentAgent()
