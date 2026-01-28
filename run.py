#!/usr/bin/env python3
import sys
import os

# Add src to the path so we can run from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.api.app import app

if __name__ == "__main__":
    print("\n🌌 COSMIC OS v7.0 - ASCENDED INTELLIGENCE & QUANTUM SCALING")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📍 Main UI: http://localhost:5000")
    print("🏆 Hall of Shame: http://localhost:5000/hall_of_shame")
    print("\n[INIT]: Quantum Nexus initialized.")
    print("[INIT]: Multi-LLM Engine ready (Anthropic, Meta, Google, DeepSeek).")
    print("[INIT]: Global Data Center Ingestion active.")
    print("\n🚀 Pulse of the singularity detected. Running...")
    
    app.run(debug=False, host='0.0.0.0', port=5000)
