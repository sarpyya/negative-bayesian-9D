import random
from typing import Dict, Any

class WAFConnector:
    """Monitors Web Application Firewall (AWS WAF / Cloud Armor) events."""
    def fetch_threat_telemetry(self) -> Dict[str, Any]:
        return {
            "blocked_requests_last_5m": random.randint(0, 5000),
            "sql_injection_attempts": random.randint(0, 100),
            "bot_traffic_spike": random.random() > 0.9,
            "shield_advanced_status": "ACTIVE"
        }

class NetworkSecurityManager:
    """Aggregates security and network entropy metrics."""
    def __init__(self):
        self.waf = WAFConnector()

    def get_security_metrics(self) -> Dict[str, Any]:
        return {
            "waf_events": self.waf.fetch_threat_telemetry(),
            "vpc_entropy": random.uniform(0.01, 0.25),
            "network_jitter_ms": random.uniform(1.0, 15.0)
        }

net_security_manager = NetworkSecurityManager()
