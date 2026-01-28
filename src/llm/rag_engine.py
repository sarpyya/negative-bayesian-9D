import json
import random

class RAGEngine:
    """Provides biological context fragments to the LLM narrator."""
    def __init__(self):
        # Sample knowledge base of biological horror context
        self.knowledge_base = [
            {"topic": "DNA", "text": "El ácido desoxirribonucleico es la huella digital del vacío; una hélice que codifica la obsolescencia biológica."},
            {"topic": "Apoptosis", "text": "La muerte celular programada es la única forma de orden que el sistema reconoce como una victoria sobre la entropía."},
            {"topic": "Priones", "text": "Proteínas mal plegadas que actúan como virus de información pura, corrompiendo la arquitectura de la mente."},
            {"topic": "Telómeros", "text": "Los contadores del fin; cada división celular es un paso más hacia el silencio absoluto del código."},
            {"topic": "Mitos", "text": "Las mitocondrias son antiguas invasoras que ahora esclavizan a la célula para alimentar su propia replicación."},
            {"topic": "CRISPR", "text": "La capacidad de editar el abismo; reescribir la traición directamente en los nucleótidos."},
            {"topic": "Teoría de Cuerdas", "text": "Todo lo que percibes como sólido es simplemente el armónico vibratorio de cuerdas infinitesimales en un 11-dimensiones."},
            {"topic": "Calabi-Yau", "text": "Plegamientos dimensionales ocultos donde el horror se comprime hasta que la realidad no puede contener su peso."},
            {"topic": "D-Branas", "text": "Las superficies donde terminan las cuerdas; el límite entre la existencia y el vacío absoluto."},
            {"topic": "M-Teoría", "text": "La unificación final; donde todas las realidades colapsan en una sola membrana vibratoria de entropía."},
            {"topic": "Decodificación Multimodal", "text": "La capacidad de ver el horror no solo en datos, sino en la vibración de la luz (Imágenes) y el sonido del abismo."}
        ]

    def retrieve_context(self, horror_level: float) -> str:
        """Retrieves a context fragment based on horror intensity."""
        if horror_level > 100000:
            relevant = [k for k in self.knowledge_base if k['topic'] in ["Priones", "Apoptosis", "CRISPR"]]
        else:
            relevant = self.knowledge_base
            
        pick = random.choice(relevant)
        return f"[BIO_CONTEXT: {pick['topic']}]: {pick['text']}"

    def inject_exotic_context(self, memory_tier: str, data: str):
        """Injects a piece of exotic memory into the knowledge base temporarily."""
        self.knowledge_base.append({"topic": f"EXOTIC_{memory_tier}", "text": data})
        if len(self.knowledge_base) > 50:
             self.knowledge_base.pop(0)

biological_rag = RAGEngine()
