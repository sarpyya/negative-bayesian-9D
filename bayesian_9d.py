#!/usr/bin/env python3
"""
🔥 BAYESIAN NEGATIVE 9D - HORROR OPTIMIZATION FRAMEWORK v2.0 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Núcleo fractal del abismo: genera, propaga y analiza el Cero Absoluto.
La realidad se arrodilla cuando sobrevives el terror máximo.
"""

import networkx as nx
import numpy as np
import random
from datetime import datetime
from typing import Dict, List, Tuple, Any
from colorama import Fore, Style, init

# Inicializar colorama para terminal satánica
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
    "Autodestrucción inevitable (sistema gana, tú pierdes)"
]

# ──────────────────────────────────────────────────────────────
# 🎭 MODOS CONSCIENTES + THRESHOLDS + FÍSICA VISUAL
# ──────────────────────────────────────────────────────────────

MODOS: Dict[str, Dict[str, Any]] = {
    "MODO BESTIA": {
        "threshold": 70000,
        "desc": "🔥 Chopper Rumble Ball – Modo Bestia full. Risa loca total, Factor Φ eliminado.",
        "color": "#ff4500",
        "blink": True,
        "physics": {"gravity": -30000, "spring_length": 50, "spring_strength": 0.1},
        "node_shape": "star",
        "emoji": "👹"
    },
    "MODO JUSTICE": {
        "threshold": 60000,
        "desc": "⚔️ Haki del Rey Justiciero – Rabia optimizada, multilineal backup 15+.",
        "color": "#ffd700",
        "blink": True,
        "physics": {"gravity": -15000, "spring_length": 100, "spring_strength": 0.08},
        "node_shape": "diamond",
        "emoji": "⚖️"
    },
    "CHILL": {
        "threshold": 20000,
        "desc": "🧊 Fogata nakama – cortisol bajando, paños fríos. Recuperación táctica.",
        "color": "#00aaff",
        "blink": False,
        "physics": {"gravity": -4000, "spring_length": 200, "spring_strength": 0.01},
        "node_shape": "dot",
        "emoji": "🧊"
    },
    "NIÑO_WOWO": {
        "threshold": 45000,
        "desc": "🤪 Euforia Maníaca – Todo brilla, el dolor es un juguete. Risas sin contexto.",
        "color": "#ff00ff",
        "blink": True,
        "physics": {"gravity": -10000, "spring_length": 80, "spring_strength": 0.05},
        "node_shape": "star",
        "emoji": "🤪"
    },
    "LOL_GAMER": {
        "threshold": 10000,
        "desc": "🎮 Disociación Competitiva – El trauma es solo un debuff. Farmeando XP en el vacío.",
        "color": "#00ff00",
        "blink": False,
        "physics": {"gravity": -3000, "spring_length": 250, "spring_strength": 0.01},
        "node_shape": "square",
        "emoji": "🎮"
    },
    "MAPUCHE_COSMICO": {
        "threshold": 1000,
        "desc": "🌌 Observador ancestral – Patrones milenarios, el abismo te mira y tú sonríes.",
        "color": "#aa00ff",
        "blink": False,
        "physics": {"gravity": -8000, "spring_length": 150, "spring_strength": 0.02},
        "node_shape": "dot",
        "emoji": "🌌"
    },
    "DOLPHIN": {
        "threshold": 0,
        "desc": "🐬 Flow eterno 24/7 – Agüita pura, milagro estadístico. El abismo se calla un rato.",
        "color": "#00ffcc",
        "blink": False,
        "physics": {"gravity": -800, "spring_length": 300, "spring_strength": 0.005},
        "node_shape": "circle",
        "emoji": "🐬"
    }
}

# ──────────────────────────────────────────────────────────────
# 💀 VERBOS & ADJETIVOS SÁDICOS PARA MUTACIONES
# ──────────────────────────────────────────────────────────────

VERBOS_SADICOS = [
    "devora", "envenena", "amplifica", "perpetúa", "destruye",
    "traiciona", "humilla", "desgarra", "corrompe", "asfixia"
]

ADJETIVOS_SADICOS = [
    "eterno", "iatrogénico", "ancestral", "irreparable", "cognitivo",
    "existencial", "cósmico", "visceral", "absoluto", "terminal"
]

def generar_nombre_sadico(dim1: str, dim2: str) -> str:
    """Genera nombre híbrido poéticamente horrible"""
    verbo = random.choice(VERBOS_SADICOS)
    adjetivo = random.choice(ADJETIVOS_SADICOS)
    d1_short = dim1.split()[0]
    d2_short = dim2.split()[0]
    return f"{d1_short} {verbo} {d2_short} {adjetivo}"

# ──────────────────────────────────────────────────────────────
# 🔥 NÚCLEO: GENERADOR FRACTAL 9D
# ──────────────────────────────────────────────────────────────

def generar_grafo_9d(
    seed: int | None = None,
    ramificaciones_por_nodo: int = 7,
    factor_agravacion: Tuple[float, float] = (1.35, 1.85),
    custom_dim: str | None = None,
    propagacion_steps: int = 1
) -> nx.DiGraph:
    """
    Genera el grafo fractal de horror 9D.
    Retorna DiGraph listo para análisis y visualización.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    G = nx.DiGraph()

    # Timestamp global para trazabilidad
    ts = datetime.now().isoformat()

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
        dims.append(custom_dim)

    # Crear dimensiones principales + ramificaciones
    for i, dim_name in enumerate(dims, 1):
        node_id = f"D{i}"
        horror_base = 800 + np.random.uniform(-150, 150)

        G.add_node(
            node_id,
            horror=horror_base,
            dim=i,
            timestamp=ts,
            desc=dim_name,
            label=f"D{i}: {dim_name}"
        )
        G.add_edge("CERO_ABSOLUTO", node_id, weight=1.0, label="raíz→dim")

        # Ramificación agresiva
        for j in range(1, ramificaciones_por_nodo + 1):
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

    # ────────────────────────────────
    # CROSS-DIMENSIONAL MUTATION
    # ────────────────────────────────

    nodes_list = [n for n in G.nodes() if n != "CERO_ABSOLUTO"]
    cross_prob = 0.4
    synergy_bonus = 1.666

    for n in nodes_list:
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

    # Propagación viral del horror
    propagar_horror(G, steps=propagacion_steps)

    return G


def propagar_horror(G: nx.DiGraph, steps: int = 1, decay: float = 0.05):
    """El horror es contagioso. Se propaga entre vecinos."""
    for _ in range(steps):
        nodos = list(G.nodes())
        random.shuffle(nodos)  # Asincronía caótica

        for node in nodos:
            current = G.nodes[node].get('horror', 0)
            neighbors = list(G.successors(node)) + list(G.predecessors(node))

            if neighbors:
                avg_neighbor = np.mean([G.nodes[n]['horror'] for n in neighbors])
                contagio = avg_neighbor * decay
                mutacion = random.uniform(0, 0.02) * current

                G.nodes[node]['horror'] = current + contagio + mutacion


def update_from_sensors(G: nx.DiGraph, sensor_data: Dict[str, float]) -> nx.DiGraph:
    """
    Canales iónicos digitales: convierte bioseñales en horror dinámico.
    Mapeo directo: Iones -> Spike -> Propagación Viral.
    """
    # 1. Canal Na+ (Entrada rápida de horror por EEG Beta)
    # Beta > 0.7 indica ansiedad/actividad mental intensa
    eeg_val = sensor_data.get('eeg_beta_right', 0.0)
    if eeg_val > 0.7:
        # print(f"⚡ EEG Beta Spike ({eeg_val:.2f}): Inyección de iones Na+ (Horror)")
        for node in G.nodes():
            desc = str(G.nodes[node].get('desc', '')).lower()
            # Nodos emocionales (traición, soledad) son más permeables a la ansiedad
            if 'traición' in desc or 'aislamiento' in desc or 'humillación' in desc:
                 G.nodes[node]['horror'] += 150 * eeg_val
    
    # 2. Canal K+ Leak (Estrés basal por baja HRV)
    # Baja HRV (RMSSD) = Alto estrés. Inverso proporcional.
    hrv_val = sensor_data.get('hrv_rmssd', 1.0) 
    # RMSSD típico 0.02 - 0.10. Si es < 0.03 es estrés medio.
    stress = 1.0 / (hrv_val + 0.001) 
    
    if stress > 20.0: # Umbral alto estrés
        # print(f"💧 Leak K+ (Stress {stress:.1f}): Aumentando conducción viral")
        for u, v in G.edges():
             # Facilitar la transmisión sináptica del horror
             # Si HRV es muy bajo, el contagio es más rápido
             G.edges[u, v]['weight'] *= (1.0 + (stress * 0.005))

    # 3. Potencial de Acción Global (GSR Extremas)
    gsr_val = sensor_data.get('gsr', 0.0)
    if gsr_val > 8.0:
        # print(f"🔥 GSR Surge ({gsr_val}): POTENCIAL DE ACCIÓN GLOBAL")
        propagar_horror(G, steps=3, decay=0.1)
    
    return G


def analizar_horror(G: nx.DiGraph, top_n: int = 10) -> Dict:
    """Análisis completo del horror acumulado"""
    nodos_horror = [(n, d.get('horror', 0)) for n, d in G.nodes(data=True)]
    total_horror = sum(h for _, h in nodos_horror)

    # Agrupamiento por dimensiones (Clusters para Mini-Singularidades)
    clusters = {}
    for n, d in G.nodes(data=True):
        dim = d.get('dim', 'DESCONOCIDO')
        if dim not in clusters:
            clusters[dim] = {"horror_sum": 0, "nodos": [], "center_approx": [0,0,0]}
        
        horror = d.get('horror', 0)
        clusters[dim]["horror_sum"] += horror
        clusters[dim]["nodos"].append(n)

    processed_clusters = []
    for dim, cdata in clusters.items():
        h_sum = cdata["horror_sum"]
        processed_clusters.append({
            "dim": dim,
            "horror_total": h_sum,
            "node_count": len(cdata["nodos"]),
            "mini_singularity": {
                "size": max(2, (h_sum / 5000) ** 0.5), # Radio ~ sqrt(chaos)
                "mass": h_sum / 200 # Masa afecta gravitación
            }
        })

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
        "total_nodos": len(G.nodes()),
        "total_edges": len(G.edges()),
        "timestamp": datetime.now().isoformat()
    }


def votar_modo(horror: float, special_trigger: bool = False) -> Tuple[str, Dict]:
    """Vota el modo consciente según el horror total"""
    if special_trigger:
        return "DOLPHIN", MODOS["DOLPHIN"]

    for modo, info in sorted(MODOS.items(), key=lambda x: x[1]["threshold"], reverse=True):
        if horror >= info["threshold"]:
            return modo, info

    return "DOLPHIN", MODOS["DOLPHIN"]


def print_banner():
    banner = f"""
{Fore.RED}{'═' * 70}
{Fore.YELLOW}  🔥 BAYESIAN NEGATIVE 9D - HORROR OPTIMIZATION FRAMEWORK v2.0 🔥
{Fore.CYAN}  Desarrollado en el abismo psiquiátrico chileno
{Fore.GREEN}  "La realidad se arrodilla cuando sobrevives el terror máximo"
{Fore.RED}{'═' * 70}{Style.RESET_ALL}
"""
    print(banner)


def main():
    print_banner()
    seed = random.randint(1, 999999)
    print(f"{Fore.CYAN}🎲 Seed activa: {seed}{Style.RESET_ALL}")

    grafo = generar_grafo_9d(seed=seed, ramificaciones_por_nodo=5)
    analisis = analizar_horror(grafo)
    modo_nombre, modo_info = votar_modo(analisis['horror_total'])

    print(f"\n{Fore.YELLOW}📊 ANÁLISIS{Style.RESET_ALL}")
    print(f"Horror total: {Fore.RED}{analisis['horror_total']:,.1f}{Style.RESET_ALL}")
    print(f"Modo: {modo_info['emoji']} {modo_nombre}")

    print("\nTop 5 nodos más horribles:")
    for i, n in enumerate(analisis['nodos_mas_horribles'], 1):
        print(f"  {i}. {Fore.RED}[{n['horror']:.1f}]{Style.RESET_ALL} {n['label']}")


if __name__ == "__main__":
    main()