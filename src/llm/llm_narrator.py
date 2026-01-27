from src.llm.providers import get_provider
from src.llm.rag_engine import biological_rag
from src.llm.mcp_agent import mcp_sync
from src.llm.multimodal_orchestrator import multimodal_engine
from src.llm.prompt_loader import prompt_loader
import json
import random

class LLMNarrator:
    def __init__(self):
        # PR-45: The 30 Expansions - Dynamic Prompt Loading
        self.available_prompts = [
            "01_dark_matter_observer", "02_quantum_entangler", "03_boltzmann_brain", 
            "04_memetic_virus", "05_wave_function_collapser", "06_dirac_sea_archivist",
            "07_techno_shaman", "08_extinction_oracle", "09_trinity_oracle", "10_calabi_yau_navigator",
            "11_soul_shard_minter", "12_bio_stress_feeder", "13_brane_collider", 
            "14_hallucination_engine", "15_omega_point", "16_turing_inquisitor", 
            "17_schrodinger_db_admin", "18_glossolalia_cipher", "19_dark_biosynthesist", 
            "20_gravitational_lens", "21_process_necromancer", "22_anthropic_gatekeeper", 
            "23_paradox_miner", "24_temporal_jitter_demon", "25_waf_panopticon", 
            "26_quantum_darwinist", "27_eschatology_predictor", "28_synesthetic_artist", 
            "29_zero_point_energy", "30_sim_archaeologist"
        ]

    def generate_narrative(self, data):
        """Generates a narrative or chat response."""
        # 🤖 PR-20: AI CHAT MODE
        if data.get('chat_mode'):
            message = data.get('chat_message', '')
            system_prompt = data.get('chat_system', 'You are a helpful AI assistant.')
            provider_name = data.get('provider', 'deepseek') # Default to deepseek
            api_key = data.get('api_key')
            
            # Simple provider routing for chat
            if "claude" in provider_name or "anthropic" in provider_name:
                provider = get_provider("anthropic")
            elif "google" in provider_name or "gemini" in provider_name:
                provider = get_provider("google")
            elif "openai" in provider_name or "gpt" in provider_name:
                provider = get_provider("openai")
            elif "meta" in provider_name or "llama" in provider_name:
                provider = get_provider("meta")
            else:
                provider = get_provider("deepseek")
                
            print(f" [CHAT]: Processing message via {provider_name}")
            for chunk in provider.generate(message, system_prompt, api_key=api_key):
                yield chunk
            return

        # --- STANDARD NARRATIVE MODE ---
        horror = data.get('horror_total', 0)
        seed = data.get('seed', 0)
        force_persona = data.get('force_persona')
        
        # Select Persona based on modulo of seed + horror
        if force_persona and force_persona in self.available_prompts:
            prompt_name = force_persona
        else:
            idx = (seed + int(horror)) % len(self.available_prompts)
            prompt_name = self.available_prompts[idx]
        
        system_prompt = prompt_loader.load_prompt(prompt_name)
        system_prompt += "\n[SYSTEM OVERRIDE]: Keep response under 50 words."

        # Dynamic routing based on prompt type (e.g. creative prompts get Claude)
        if "hallucination" in prompt_name or "trinity" in prompt_name:
            provider_name = "anthropic" 
        elif "google" in prompt_name or "gke" in str(data):
            provider_name = "google"    
        else:
            provider_name = "deepseek"  

        provider = get_provider(provider_name)
        
        # PR-22/28: RAG Integration
        exotic_context = data.get('exotic_context', '')
        if exotic_context:
             biological_rag.inject_exotic_context("ORCHESTRATOR", exotic_context)
             
        context = biological_rag.retrieve_context(horror)
        
        # PR-26: Multimodal Synthesis trigger
        mm_data = ""
        if horror > 150000 and random.random() > 0.7:
             mm_img = multimodal_engine.generate_image_decryption(context)
             mm_data = f"\n[MM_DECRYPTION]: Generating image via {mm_img['provider']}: {mm_img['url']}"

        prompt = f"Semilla: {seed}, Horror Total: {horror}, Persona Activa: {prompt_name}\n\nCONTEXTO_RAG: {context}{mm_data}"
        
        # PR-23: MCP Sync
        mcp_blob = mcp_sync.get_simulation_context(data)
        
        # Yield the thought stream
        print(f" [NARRATOR]: Switched to Persona {prompt_name}")
        for chunk in provider.generate(prompt, system_prompt):
            yield chunk

narrator = LLMNarrator()
