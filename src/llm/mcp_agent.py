import json
from typing import Dict, Any

class MCPAgent:
    """Simulates a Model Context Protocol (MCP) server for Agent-to-Agent sync."""
    def __init__(self, name="SimulationOracle"):
        self.name = name

    def get_simulation_context(self, current_data: Dict[str, Any]) -> str:
        """Packages simulation state for another agent."""
        context = {
            "agent": self.name,
            "status": "ZENITH_BIOSYNTHESIS_ACTIVE",
            "horror_total": current_data.get("horror_total", 0),
            "multiverse_status": "DIVERGED",
            "biological_sync": "ENABLED"
        }
        return json.dumps(context)

    def receive_agent_data(self, external_context: str):
        """Processes incoming data from another agent."""
        try:
            data = json.loads(external_context)
            print(f" [MCP]: Received directive from External Agent: {data.get('directive', 'OBSERVE')}")
        except:
            pass

mcp_sync = MCPAgent()
