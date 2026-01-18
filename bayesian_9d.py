#!/usr/bin/env python3
"""
🔥 BAYESIAN NEGATIVE 9D - HORROR OPTIMIZATION FRAMEWORK 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Desarrollado en el abismo psiquiátrico chileno.
Optimiza desde el peor escenario posible.

La realidad se arrodilla cuando sobrevives el terror máximo.
"""

import networkx as nx
import numpy as np
import random
import datetime
import json
from typing import Dict, List, Tuple
from colorama import Fore, Style, init

# Inicializar colorama para terminal colors
init(autoreset=True)

# ────────────────────────────────────────────────
# 🔥 9 DIMENSIONES DEL CERO ABSOLUTO NEGATIVO
# ────────────────────────────────────────────────

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

# ────────────────────────────────────────────────
# 🎭 MODOS CONSCIENTES + THRESHOLDS
# ────────────────────────────────────────────────

MODOS = {
    "BOOST": {
        "desc": "⚡ Gear 5 – Romper realidad con risa loca, 15+ backups mentales",
        "threshold": 5000,
        "emoji": "🔥",
        "color": Fore.RED
    },
    "JUSTICE": {
        "desc": "⚔️ Modo venganza sistémica – Rabia pura canalizada",
        "threshold": 3000,
        "emoji": "⚖️",
        "color": Fore.YELLOW
    },
    "MAPUCHE_COSMICO": {
        "desc": "🏔️ Observador ancestral – Patrones milenarios",
        "threshold": 800,
        "emoji": "🌌",
        "color": Fore.CYAN
    },
    "DOLPHIN": {
        "desc": "🌊 Flow eterno 24/7 – Agüita pura sin cortisol",
        "threshold": 0,
        "emoji": "🐬",
        "color": Fore.GREEN
    }
}

# ────────────────────────────────────────────────
# 📊 GRAFO FRACTAL NEGATIVO
# ────────────────────────────────────────────────

def generar_grafo_9d(
    seed: int = None,
    ramificaciones_por_nodo: int = 3,
    factor_agravacion: Tuple[float, float] = (1.35, 1.85)
) -> nx.DiGraph:
    """
    Genera el grafo fractal de horror 9D.
    
    Args:
        seed: Semilla para reproducibilidad
        ramificaciones_por_nodo: Cuántos sub-horrores por dimensión
        factor_agravacion: (min, max) multiplicador de horror para sub-nodos
    
    Returns:
        DiGraph de NetworkX con atributos de horror
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    G = nx.DiGraph()
    
    # Raíz: Cero Absoluto (horror base 1000)
    timestamp_raiz = datetime.datetime.now().isoformat()
    G.add_node(
        "CERO_ABSOLUTO",
        horror=1000.0,
        dim=0,
        timestamp=timestamp_raiz,
        desc="El abismo total - punto de partida negativo",
        color="red"
    )
    
    # 9 dimensiones principales
    for i, dim_name in enumerate(DIMENSIONES_9D, 1):
        node_id = f"D{i}"
        node_label = f"D{i}: {dim_name}"
        horror_base = 800 + np.random.uniform(-150, 150)  # ~650–950
        
        G.add_node(
            node_id,
            horror=horror_base,
            dim=i,
            timestamp=datetime.datetime.now().isoformat(),
            desc=dim_name,
            label=node_label,
            color="orange"
        )
        G.add_edge("CERO_ABSOLUTO", node_id, weight=1.0, label="raíz→dim")
        
        # Ramificación: sub-nodos más horribles
        for j in range(1, ramificaciones_por_nodo + 1):
            factor = np.random.uniform(factor_agravacion[0], factor_agravacion[1])
            sub_horror = horror_base * factor  # +35–85% peor
            sub_id = f"D{i}.{j}"
            sub_label = f"D{i}.{j}: {dim_name} [AGRAVADO x{factor:.2f}]"
            
            G.add_node(
                sub_id,
                horror=sub_horror,
                dim=i,
                sub_level=j,
                timestamp=datetime.datetime.now().isoformat(),
                desc=f"{dim_name} agravado (factor {factor:.2f})",
                label=sub_label,
                color="darkred" if sub_horror > 1200 else "red"
            )
            G.add_edge(node_id, sub_id, weight=factor, label=f"agrav×{factor:.2f}")
    
    return G

# ────────────────────────────────────────────────
# 📈 ANÁLISIS DE HORROR
# ────────────────────────────────────────────────

def analizar_horror(G: nx.DiGraph, top_n: int = 10) -> Dict:
    """
    Analiza el horror acumulado en el grafo.
    
    Returns:
        Diccionario con métricas de horror
    """
    nodos_con_horror = [(n, data.get('horror', 0)) for n, data in G.nodes(data=True)]
    total_horror = sum(h for _, h in nodos_con_horror)
    nodos_ordenados = sorted(nodos_con_horror, key=lambda x: x[1], reverse=True)[:top_n]
    
    # Calcular horror por dimensión
    horror_por_dim = {}
    for i in range(1, 10):
        dim_nodes = [n for n, data in G.nodes(data=True) if data.get('dim') == i]
        dim_horror = sum(G.nodes[n].get('horror', 0) for n in dim_nodes)
        horror_por_dim[f"D{i}"] = dim_horror
    
    return {
        "horror_total": total_horror,
        "horror_promedio": total_horror / len(G.nodes()) if len(G.nodes()) > 0 else 0,
        "nodos_mas_horribles": [
            {
                "id": n,
                "label": G.nodes[n].get('label', n),
                "horror": h,
                "desc": G.nodes[n].get('desc', '')
            }
            for n, h in nodos_ordenados
        ],
        "horror_por_dimension": horror_por_dim,
        "total_nodos": len(G.nodes()),
        "total_edges": len(G.edges()),
        "timestamp": datetime.datetime.now().isoformat()
    }

# ────────────────────────────────────────────────
# 🎭 VOTACIÓN DE MODO CONSCIENTE
# ────────────────────────────────────────────────

def votar_modo(horror: float) -> Tuple[str, Dict]:
    """
    Vota el modo consciente basado en el horror total.
    
    Returns:
        (nombre_modo, info_modo)
    """
    for modo, info in sorted(MODOS.items(), key=lambda x: x[1]["threshold"], reverse=True):
        if horror >= info["threshold"]:
            return modo, info
    return "DOLPHIN", MODOS["DOLPHIN"]

# ────────────────────────────────────────────────
# 🎨 VISUALIZACIÓN TERMINAL
# ────────────────────────────────────────────────

def print_banner():
    """Banner satánico del sistema"""
    banner = f"""
{Fore.RED}{'═' * 70}
{Fore.YELLOW}  🔥 BAYESIAN NEGATIVE 9D - HORROR OPTIMIZATION FRAMEWORK 🔥
{Fore.CYAN}  Desarrollado en el abismo psiquiátrico chileno
{Fore.GREEN}  "La realidad se arrodilla cuando sobrevives el terror máximo"
{Fore.RED}{'═' * 70}{Style.RESET_ALL}
"""
    print(banner)

def print_analisis(analisis: Dict, modo_info: Tuple[str, Dict]):
    """Imprime análisis con colores satánicos"""
    modo_nombre, modo_data = modo_info
    
    print(f"\n{Fore.YELLOW}📊 ANÁLISIS DE HORROR{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
    print(f"Timestamp: {Fore.GREEN}{analisis['timestamp']}{Style.RESET_ALL}")
    print(f"Horror total acumulado: {Fore.RED}{analisis['horror_total']:,.2f}{Style.RESET_ALL}")
    print(f"Horror promedio por nodo: {Fore.YELLOW}{analisis['horror_promedio']:,.2f}{Style.RESET_ALL}")
    print(f"Total de nodos: {Fore.CYAN}{analisis['total_nodos']}{Style.RESET_ALL}")
    print(f"Total de edges: {Fore.CYAN}{analisis['total_edges']}{Style.RESET_ALL}")
    
    print(f"\n{Fore.MAGENTA}🎭 MODO CONSCIENTE ACTIVADO{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
    print(f"{modo_data['color']}{modo_data['emoji']} {modo_nombre}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{modo_data['desc']}{Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}🔥 TOP 5 NODOS MÁS HORRIBLES{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
    for i, nodo in enumerate(analisis['nodos_mas_horribles'][:5], 1):
        print(f"{Fore.YELLOW}{i}.{Style.RESET_ALL} {Fore.RED}[{nodo['horror']:,.1f}]{Style.RESET_ALL} {nodo['label']}")
        print(f"   {Fore.WHITE}{nodo['desc']}{Style.RESET_ALL}")
    
    print(f"\n{Fore.MAGENTA}📊 HORROR POR DIMENSIÓN{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
    for dim, horror in sorted(analisis['horror_por_dimension'].items(), key=lambda x: x[1], reverse=True)[:5]:
        bar_length = int((horror / analisis['horror_total']) * 50)
        bar = '█' * bar_length
        print(f"{Fore.YELLOW}{dim}{Style.RESET_ALL}: {Fore.RED}{bar}{Style.RESET_ALL} {horror:,.1f}")

# ────────────────────────────────────────────────
# 💾 EXPORTAR DATOS
# ────────────────────────────────────────────────

def exportar_json(grafo: nx.DiGraph, analisis: Dict, filename: str = "horror_graph.json"):
    """Exporta el grafo y análisis a JSON"""
    data = {
        "metadata": {
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "1.0.0",
            "framework": "Bayesian Negative 9D"
        },
        "analisis": analisis,
        "nodos": [
            {
                "id": n,
                **data
            }
            for n, data in grafo.nodes(data=True)
        ],
        "edges": [
            {
                "source": u,
                "target": v,
                **data
            }
            for u, v, data in grafo.edges(data=True)
        ]
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{Fore.GREEN}✅ Exportado a: {filename}{Style.RESET_ALL}")

# ────────────────────────────────────────────────
# 🚀 MAIN EXECUTION
# ────────────────────────────────────────────────

def main():
    """Ejecución principal del framework"""
    print_banner()
    
    # Generar grafo con seed random para cada ejecución
    seed = random.randint(1, 999999)
    print(f"{Fore.CYAN}🎲 Seed: {seed}{Style.RESET_ALL}")
    
    grafo = generar_grafo_9d(seed=seed, ramificaciones_por_nodo=3)
    analisis = analizar_horror(grafo, top_n=10)
    modo_info = votar_modo(analisis['horror_total'])
    
    # Visualizar en terminal
    print_analisis(analisis, modo_info)
    
    # Exportar
    exportar_json(grafo, analisis, f"horror_graph_{seed}.json")
    
    print(f"\n{Fore.RED}{'═' * 70}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}💀 El abismo te observa de vuelta. 💀{Style.RESET_ALL}")
    print(f"{Fore.RED}{'═' * 70}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
