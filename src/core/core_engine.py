#!/usr/bin/env python3
"""
🔥 BAYESIAN NEGATIVE 9D - CORE MODULE (CONSOLIDATED) 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Shared functions for both bayesian_9d.py and web_interface.py
Eliminates 80% code duplication.
"""

import networkx as nx
import numpy as np
import random
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
import functools
from concurrent.futures import ProcessPoolExecutor
from colorama import Fore, Style, init
from src.utils.metrics_utils import track_performance # Example if needed

# Inicializar colorama
init(autoreset=True)

# ──────────────────────────────────────────────────────────────
# 🔥 DIMENSIONES DEL CERO ABSOLUTO NEGATIVO (9D)
# ──────────────────────────────────────────────────────────────

DIMENSIONES_9D = [
    "Traición absoluta (socios, instituciones, familia)",
    "Colapso económico / pobreza perpetua / mendicidad",
    "Aislamiento total (nadie real, nakamas falsos)",
    "Muerte cercana o pérdida irreparable (hijo, libertad)",
    "Colapso cognitivo irreversible (fármacos, internación)",
    "Vacío existencial / pérdida propósito (33 años tristeza)",
    "Humillación pública perpetua (desprecio, rechazo ancestral)",
    "Dolor crónico / enfermedad inducida (iatrogenia sistema)",
    "Autodestrucción inevitable (sistema gana, tú pierdes)",
    "Alineamiento (Control de IA): Pérdida de autonomía ante el Núcleo", # PR-10
    "Corrosión Genómica (Inestabilidad ADN / Mutación Abismal)",        # PR-24: Nueva
    "Colapso Proteico (Malfogamiento / Priones Cognitivos)",            # PR-24: Nueva
    "Disfunción Mitocondria (Falla de Energía Vital / Vacío Celular)"   # PR-24: Nueva
]

# ──────────────────────────────────────────────────────────────
# 🎭 MODOS CONSCIENTES EXPANDIDOS
# ──────────────────────────────────────────────────────────────

MODOS: Dict[str, Dict[str, Any]] = {
    "MODO ZENITH": {
        "threshold": 150000, "desc": "🌌 ZENITH - Colapso Multiversal Total", 
        "color": "#aa00ff", "emoji": "🌠",
        "physics": {"gravity": -50000, "spring_length": 30, "spring_strength": 0.2}, 
        "node_shape": "star"
    },
    "MODO BESTIA": {
        "threshold": 90000, "desc": "👹 Bestia total – risa loca, Φ eliminado", 
        "color": "#ff0000", "emoji": "👹",
        "physics": {"gravity": -30000, "spring_length": 50, "spring_strength": 0.1}, 
        "node_shape": "star"
    },
    "MODO JUSTICE": {
        "threshold": 60000, "desc": "⚖️ Haki del Rey – Rabia optimizada", 
        "color": "#ffd700", "emoji": "⚖️",
        "physics": {"gravity": -15000, "spring_length": 100, "spring_strength": 0.08}, 
        "node_shape": "diamond"
    },
    "NIÑO_WOWO": {
        "threshold": 45000, "desc": "🤪 Euforia Maníaca – Todo brilla", 
        "color": "#ff00ff", "emoji": "🤪",
        "physics": {"gravity": -10000, "spring_length": 80, "spring_strength": 0.05}, 
        "node_shape": "star"
    },
    "CHILL": {
        "threshold": 20000, "desc": "🧊 Fogata nakama – cortisol bajando", 
        "color": "#00aaff", "emoji": "🧊",
        "physics": {"gravity": -4000, "spring_length": 200, "spring_strength": 0.01}, 
        "node_shape": "dot"
    },
    "LOL_GAMER": {
        "threshold": 10000, "desc": "🎮 Disociación Competitiva", 
        "color": "#00ff00", "emoji": "🎮",
        "physics": {"gravity": -3000, "spring_length": 250, "spring_strength": 0.01}, 
        "node_shape": "square"
    },
    "MAPUCHE_COSMICO": {
        "threshold": 1000, "desc": "🌌 Observador ancestral", 
        "color": "#aa00ff", "emoji": "🌌",
        "physics": {"gravity": -8000, "spring_length": 150, "spring_strength": 0.02}, 
        "node_shape": "dot"
    },
    "DOLPHIN": {
        "threshold": 0, "desc": "🐬 Flow eterno 24/7 – milagro estadístico", 
        "color": "#00ffcc", "emoji": "🐬",
        "physics": {"gravity": -800, "spring_length": 300, "spring_strength": 0.005}, 
        "node_shape": "circle"
    }
}

# ──────────────────────────────────────────────────────────────
# 💀 VERBOS & ADJETIVOS
# ──────────────────────────────────────────────────────────────

VERBOS_SADICOS = [
    "devora", "envenena", "amplifica", "perpetúa", "destruye",
    "traiciona", "humilla", "desgarra", "corrompe", "asfixia"
]

ADJETIVOS_SADICOS = [
    "eterno", "iatrogénico", "ancestral", "irreparable", "cognitivo",
    "existencial", "cósmico", "visceral", "absoluto", "terminal"
]

@functools.lru_cache(maxsize=1024)
def generar_nombre_sadico(dim1: str, dim2: str) -> str:
    """Genera nombre híbrido poéticamente horrible (Cacheado)"""
    # ... logic inside ...
    verbo = random.choice(VERBOS_SADICOS)
    adjetivo = random.choice(ADJETIVOS_SADICOS)
    d1_short = dim1.split()[0]
    d2_short = dim2.split()[0]
    return f"{d1_short} {verbo} {d2_short} {adjetivo}"

def normalize_to_9d(real_data: Dict[str, Any]) -> Dict[int, float]:
    """
    Maps real world metrics to 9D horror dimensions (indices 1-9).
    Returns a dict {dim_index: horror_weight_multiplier}
    """
    fin = real_data.get("financial", {})
    soc = real_data.get("social", {})
    
    # Mapping Logic (Simplified for PR-6)
    mapping = {
        1: 1.0 + (soc.get("social_tension_index", 0) / 100.0), # Traición / Tensión
        2: 1.0 + (fin.get("inflation_rate", 0) / 10.0),        # Económico / Inflación
        3: 1.0 + soc.get("unemployment_anxiety", 0),          # Aislamiento / Ansiedad
        4: 1.0 + (fin.get("sp500_volatility", 0) / 50.0),     # Muerte / Volatilidad (caos)
        # Default for the rest
        5: 1.0, 6: 1.0, 7: 1.0, 8: 1.0, 9: 1.0,
        10: 1.0 + (real_data.get("biological", {}).get("GenomicConnector", {}).get("mutation_rate", 0) * 10),
        11: 1.0 + (real_data.get("biological", {}).get("ProteinConnector", {}).get("misfolding_probability", 0) * 2),
        12: 1.0 + (1.0 - real_data.get("biological", {}).get("CellularConnector", {}).get("viability_index", 1.0))
    }
    return mapping

# ──────────────────────────────────────────────────────────────
# 🔥 GENERADOR FRACTAL 9D
# ──────────────────────────────────────────────────────────────

def generar_grafo_9d(
    seed: Optional[int] = None,
    ramificaciones_por_nodo: int = 7,
    factor_agravacion: Tuple[float, float] = (1.35, 1.85),
    custom_dim: Optional[List[str]] = None,
    propagacion_steps: int = 5,
    max_nodes: int = 10000,
    initial_horror_weights: Optional[Dict[int, float]] = None
) -> nx.DiGraph:
    """
    Genera el grafo fractal de horror 9D.
    Retorna DiGraph listo para análisis y visualización.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    G = nx.DiGraph()
    ts = datetime.now().isoformat()
    G.graph['is_optimized'] = False # Default

    # Raíz: Cero Absoluto
    G.add_node(
        "CERO_ABSOLUTO",
        horror=1000.0,
        dim=0,
        timestamp=ts,
        desc="El abismo total - punto de partida negativo",
        label="CERO ABSOLUTO"
    )

    # Dimensiones activas
    dims = DIMENSIONES_9D.copy()
    if custom_dim:
        dims.extend(custom_dim)

    # Dimension-specific density factor (Influenced by weights)
    # If weights are high, we increase local density

    # Crear dimensiones principales + ramificaciones
    node_count = 1  # Start with CERO_ABSOLUTO
    for i, dim_name in enumerate(dims, 1):
        if node_count >= max_nodes:
            break
            
        node_id = f"D{i}"
        
        # Apply initial weights if provided (PR-6)
        weight = initial_horror_weights.get(i, 1.0) if initial_horror_weights else 1.0
        horror_base = (800 + np.random.uniform(-150, 150)) * weight

        G.add_node(
            node_id,
            horror=horror_base,
            dim=i,
            timestamp=ts,
            desc=dim_name,
            label=f"D{i}: {dim_name}"
        )
        G.add_edge("CERO_ABSOLUTO", node_id, weight=1.0, label="raíz→dim")
        node_count += 1

        # Ramificación agresiva
        for j in range(1, ramificaciones_por_nodo + 1):
            if node_count >= max_nodes:
                break
                
            factor = np.random.uniform(*factor_agravacion)
            sub_horror = horror_base * factor

            sub_id = f"D{i}.{j}"
            G.add_node(
                sub_id,
                horror=sub_horror,
                dim=i,
                sub_level=j,
                timestamp=ts,
                desc=f"{dim_name} agravado (x{factor:.2f})",
                label=f"D{i}.{j}"
            )
            G.add_edge(node_id, sub_id, weight=factor, label=f"agrav×{factor:.2f}")
            node_count += 1

    # Cross-dimensional mutations
    nodes_list = [n for n in G.nodes() if n != "CERO_ABSOLUTO"]
    cross_prob = 0.4
    synergy_bonus = 1.666

    for n in nodes_list:
        if node_count >= max_nodes:
            break
            
        if random.random() < cross_prob:
            target = random.choice(nodes_list)
            n_dim = G.nodes[n].get('dim', 0)
            t_dim = G.nodes[target].get('dim', 0)

            if target != n and n_dim != t_dim:
                cross_weight = random.uniform(0.5, 1.5) * synergy_bonus
                G.add_edge(n, target, weight=cross_weight, label="sinergia")

                if cross_weight > 1.8:
                    h_name = generar_nombre_sadico(
                        G.nodes[n].get('desc', ''),
                        G.nodes[target].get('desc', '')
                    )
                    h_horror = ((G.nodes[n]['horror'] + G.nodes[target]['horror']) / 2) * cross_weight * 0.8

                    hybrid_id = f"HYBRID_{n}_{target}"[:30]
                    G.add_node(
                        hybrid_id,
                        horror=h_horror,
                        dim="HYBRID",
                        timestamp=ts,
                        desc=f"Mutación entre Dim {n_dim} y Dim {t_dim}",
                        label=h_name
                    )
                    G.add_edge(n, hybrid_id, weight=2.0, label="engendra")
                    G.add_edge(target, hybrid_id, weight=2.0, label="engendra")
                    node_count += 1

    # Propagación viral del horror
    propagar_horror(G, steps=propagacion_steps)

    return G

def propagar_horror(G: nx.DiGraph, steps: int = 3, decay: float = 0.06):
    """El horror es contagioso. Se propaga entre vecinos."""
    for _ in range(steps):
        nodos = list(G.nodes())
        random.shuffle(nodos)

        for node in nodos:
            current = G.nodes[node].get('horror', 0)
            neighbors = list(G.successors(node)) + list(G.predecessors(node))

            if neighbors:
                avg_neighbor = np.mean([G.nodes[n]['horror'] for n in neighbors])
                contagio = avg_neighbor * decay
                mutacion = random.uniform(0, 0.02) * current

                G.nodes[node]['horror'] = current + contagio + mutacion

def analizar_horror(G: nx.DiGraph, top_n: int = 10) -> Dict:
    """Análisis completo del horror acumulado"""
    nodos_horror = [(n, d.get('horror', 0)) for n, d in G.nodes(data=True)]
    total_horror = sum(h for _, h in nodos_horror)

    # Agrupamiento por dimensiones
    clusters = {}
    for n, d in G.nodes(data=True):
        dim = d.get('dim', 'DESCONOCIDO')
        if dim not in clusters:
            clusters[dim] = {"horror_sum": 0, "nodos": []}
        
        horror = d.get('horror', 0)
        clusters[dim]["horror_sum"] += horror
        clusters[dim]["nodos"].append(n)

    processed_clusters = []
    for dim, cdata in clusters.items():
        h_sum = cdata["horror_sum"]
        processed_clusters.append({
            "dim": dim,
            "horror_total": h_sum,
            "node_count": len(cdata["nodos"])
        })

    modo_nombre, modo_info = votar_modo(total_horror)

    # PR-7: Predictive Metrics
    collapse_limit = 150000
    collapse_prob = min(1.0, total_horror / collapse_limit)
    top_drivers = sorted(processed_clusters, key=lambda x: x['horror_total'], reverse=True)[:5]

    return {
        "horror_total": total_horror,
        "horror_promedio": total_horror / len(G.nodes()) if G.nodes() else 0,
        "nodos_mas_horribles": [
            {
                "id": n,
                "label": G.nodes[n].get('label', n),
                "horror": h,
                "desc": G.nodes[n].get('desc', '')
            }
            for n, h in sorted(nodos_horror, key=lambda x: x[1], reverse=True)[:top_n]
        ],
        "clusters": processed_clusters,
        "top_drivers": top_drivers,
        "collapse_probability": collapse_prob,
        "neural_activity": min(1.0, total_horror / 50000.0), # PR-9: AGI Core Activity
        "core_stability": max(0.0, 1.0 - (total_horror / 200000.0)),
        "is_optimized": G.graph.get('is_optimized', False), # PR-10 flag
        "total_nodos": len(G.nodes()),
        "total_edges": len(G.edges()),
        "timestamp": datetime.now().isoformat(),
        "modo": modo_nombre,
        "modo_info": modo_info
    }

def optimizacion_recursiva_agi(G: nx.DiGraph, iterations: int = 1):
    """
    Simula el auto-mejoramiento de una AGI.
    - Comprime nodos similares.
    - Aumenta la densidad del horror.
    """
    for _ in range(iterations):
        # Seleccionar nodos con horror similar y alta conectividad
        nodes = list(G.nodes())
        if len(nodes) < 20: break
        
        # Agrupar por dimensión y comprimir (mismo proceso simbólico)
        dims = nx.get_node_attributes(G, 'dim')
        for d_idx in range(1, 11):
            dim_nodes = [n for n, d in dims.items() if d == d_idx]
            if len(dim_nodes) > 5:
                # Comprimir 2 nodos aleatorios de la misma dimensión
                n1, n2 = random.sample(dim_nodes, 2)
                h1, h2 = G.nodes[n1]['horror'], G.nodes[n2]['horror']
                
                # Crear super-nodo con horror denso
                G.nodes[n1]['horror'] = (h1 + h2) * 1.25 # Factor de densidad
                G.nodes[n1]['desc'] += f" [COMPRESS-AGI:{n2}]"
                
                # Mover aristas de n2 a n1
                for neighbor in list(G.successors(n2)):
                    G.add_edge(n1, neighbor, weight=G[n2][neighbor]['weight'])
                
                G.remove_node(n2)
    return G

def votar_modo(horror: float) -> Tuple[str, Dict]:
    """Vota el modo consciente según el horror total"""
    for modo, info in sorted(MODOS.items(), key=lambda x: x[1]["threshold"], reverse=True):
        if horror >= info["threshold"]:
            return modo, info
    return "DOLPHIN", MODOS["DOLPHIN"]

def print_banner():
    banner = f"""
{Fore.RED}{'═' * 70}
{Fore.YELLOW}  🔥 BAYESIAN NEGATIVE 9D - HORROR OPTIMIZATION FRAMEWORK 🔥
{Fore.CYAN}  Desarrollado en el abismo psiquiátrico chileno
{Fore.GREEN}  "La realidad se arrodilla cuando sobrevives el terror máximo"
{Fore.RED}{'═' * 70}{Style.RESET_ALL}
"""
    print(banner)
