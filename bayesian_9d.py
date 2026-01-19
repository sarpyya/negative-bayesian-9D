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
    "MODO BESTIA": {
        "threshold": 70000,
        "desc": "🔥 Chopper Rumble Ball – Modo Bestia full. Risa loca total, Factor Osvaldo eliminado. Destrucción creativa.",
        "color": "#ff4500",  # Naranja fuego
        "blink": True,
        "physics": {
            "gravity": -30000,
            "spring_length": 50,
            "spring_strength": 0.1,
            "damping": 0.05
        },
        "node_shape": "star",
        "edge_color": "#ff4500",
        "emoji": "👹"
    },
    "MODO JUSTICE": {
        "threshold": 60000,
        "desc": "⚔️ Haki del Rey Justiciero – Rabia optimizada, multilineal backup 15+. Injusticia detectada y confrontada.",
        "color": "#ffd700",  # Oro
        "blink": True,
        "physics": {
            "gravity": -15000,
            "spring_length": 100,
            "spring_strength": 0.08,
            "damping": 0.09
        },
        "node_shape": "diamond",
        "edge_color": "#ffd700",
        "emoji": "⚖️"
    },
    "CHILL": {
        "threshold": 20000,
        "desc": "🧊 Fogata nakama – cortisol bajando, paños fríos. Recuperación táctica.",
        "color": "#00aaff",  # Azul chill
        "blink": False,
        "physics": {
            "gravity": -4000,
            "spring_length": 200,
            "spring_strength": 0.01,
            "damping": 0.09
        },
        "node_shape": "dot",
        "edge_color": "rgba(0, 170, 255, 0.5)",
        "emoji": "🧊"
    },
    "MAPUCHE_COSMICO": {
        "threshold": 1000,
        "desc": "🌌 Observador ancestral – Patrones milenarios, el abismo te mira y tú sonríes.",
        "color": "#aa00ff",  # Violeta
        "blink": False,
        "physics": {
            "gravity": -8000,
            "spring_length": 150,
            "spring_strength": 0.02,
            "damping": 0.09
        },
        "node_shape": "dot",
        "edge_color": "rgba(170, 0, 255, 0.5)",
        "emoji": "🌌"
    },
    "DOLPHIN": {
        "threshold": 0,
        "desc": "🐬 Flow eterno 24/7 – Agüita pura, milagro estadístico. El abismo se calla un rato.",
        "color": "#00ffcc",  # Turquesa
        "blink": False,
        "physics": {
            "gravity": -800,
            "spring_length": 300,
            "spring_strength": 0.005,
            "damping": 0.9
        },
        "node_shape": "circle",
        "edge_color": "rgba(0, 255, 204, 0.5)",
        "emoji": "🐬",
        "effects": {
            "message": "Modo Dolphin activado. El flujo eterno te abraza..."
        }
    }
}

# ────────────────────────────────────────────────
# 💀 GENERADOR DE NOMBRES SÁDICOS
# ────────────────────────────────────────────────

VERBOS_SADICOS = ["devora", "envenena", "amplifica", "perpetúa", "destruye", "traiciona", "humilla", "desgarra", "corrompe", "asfixia"]
ADJETIVOS_SADICOS = ["eterno", "iatrogénico", "ancestral", "irreparable", "cognitivo", "existencial", "cósmico", "visceral", "absoluto", "terminal"]

def generar_nombre_sadico(dim1_name: str, dim2_name: str) -> str:
    """Genera un nombre híbrido poéticamente horrible"""
    verbo = random.choice(VERBOS_SADICOS)
    adjetivo = random.choice(ADJETIVOS_SADICOS)
    # Ejemplo: "Traición devora el Vacío ancestral"
    # Simplificamos tomando la primera palabra de las dimensiones para que no quede eterno
    d1_short = dim1_name.split()[0]
    d2_short = dim2_name.split()[0]
    
    return f"{d1_short} {verbo} {d2_short} {adjetivo}"

def generar_grafo_9d(
    seed: int = None,
    ramificaciones_por_nodo: int = 7,
    factor_agravacion: Tuple[float, float] = (1.35, 1.85),
    custom_dim: str = None
) -> nx.DiGraph:
    """
    Genera el grafo fractal de horror 9D.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    G = nx.DiGraph()
    
    # Lista local de dimensiones para no alterar la global permanentemente
    dims_activas = DIMENSIONES_9D.copy()
    if custom_dim:
        dims_activas.append(custom_dim)
    
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
    
    # Dimensiones principales
    for i, dim_name in enumerate(dims_activas, 1):
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
        sub_nodes = []
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
            sub_nodes.append(sub_id)

            sub_nodes.append(sub_id)

    # 🔥 CONEXIONES TRANSVERSALES & HIBRIDACIÓN (CROSS-DIMENSIONAL MUTATION) 🔥
    nodes_list = list(G.nodes())
    cross_prob = 0.4
    synergy_bonus = 1.666  # 66.6% bonus
    
    # Copia de lista para no iterar sobre lo que añadimos
    static_nodes_list = [n for n in nodes_list if n != "CERO_ABSOLUTO"]
    
    for n in static_nodes_list:
        # Probabilidad de conexión cruzada
        if random.random() < cross_prob:
            target = random.choice(static_nodes_list)
            
            # Evitar auto-conexión y misma dimensión (queremos cruce real)
            n_dim = G.nodes[n].get('dim', 0)
            t_dim = G.nodes[target].get('dim', 0)
            
            if target != n and n_dim != t_dim:
                # Calcular peso sinérgico
                cross_weight = random.uniform(0.5, 1.5) * synergy_bonus
                G.add_edge(n, target, weight=cross_weight, label="sinergia")
                
                # 🔥 GENERACIÓN DE NODO HÍBRIDO (El Horror Mutante)
                # Si la conexión es muy fuerte, nace un nuevo horror puros
                if cross_weight > 1.8:
                    n_data = G.nodes[n]
                    t_data = G.nodes[target]
                    
                    # Nombre compuesto mejorado
                    h_name = generar_nombre_sadico(G.nodes[n]['desc'], G.nodes[target]['desc'])
                    
                    # Horror promedio * bonus
                    n_h = n_data.get('horror', 0)
                    t_h = t_data.get('horror', 0)
                    h_horror = ((n_h + t_h) / 2) * (cross_weight * 0.8) # Un poco menos que el link directo pero horrible
                    
                    match_id = f"HYBRID_{n}_{target}"[:30] # ID único corto
                    
                    G.add_node(
                        match_id,
                        horror=h_horror,
                        dim="HYBRID",
                        timestamp=datetime.datetime.now().isoformat(),
                        desc=f"Mutación entre Dim {n_dim} y Dim {t_dim}",
                        label=h_name,
                        color="purple" 
                    )
                    
                    # Conectar padres a hijo mutante
                    G.add_edge(n, match_id, weight=2.0, label="engendra")
                    G.add_edge(target, match_id, weight=2.0, label="engendra")
    
    # 🔥 FASE DE PROPAGACIÓN DE HORROR (DIFUSIÓN) 🔥
    propagar_horror(G)
    
    return G

def propagar_horror(G: nx.DiGraph, steps: int = 1, decay: float = 0.05):
    """
    Simula la difusión del horror entre vecinos.
    El horror es contagioso.
    """
    for _ in range(steps):
        # Calculamos los deltas primero para actualización sincrónica (o asincrónica si queremos caos)
        # Haremos asincrónica para más caos
        nodos = list(G.nodes())
        random.shuffle(nodos)
        
        for node in nodos:
            current_horror = G.nodes[node]['horror']
            
            # Obtener vecinos (en un DiGraph, successors y predecessors podrían influir, 
            # pero asumiremos flujo de influencia bidireccional para el contagio)
            neighbors = list(G.successors(node)) + list(G.predecessors(node))
            if not neighbors: continue
            
            # Promedio de horror vecinal
            avg_neighbor_horror = np.mean([G.nodes[n]['horror'] for n in neighbors])
            
            # Si mis vecinos son peores, me contagian. Si son mejores, me hunden igual (pesimismo bayesiano).
            # En este sistema, el horror solo sube o se estabiliza, nunca baja.
            
            contagio = avg_neighbor_horror * decay
            
            # Factor aleatorio de mutación espontánea
            mutacion = random.uniform(0, 0.02) * current_horror
            
            # Actualizar
            G.nodes[node]['horror'] += contagio + mutacion

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

def votar_modo(horror: float, special_trigger: bool = False) -> Tuple[str, Dict]:
    """
    Vota el modo consciente basado en el horror total.
    Allows forcing DOLPHIN mode via special_trigger.
    
    Returns:
        (nombre_modo, info_modo_completa)
    """
    # Special trigger: si el usuario fuerza Dolphin
    if special_trigger:
        return "DOLPHIN", MODOS["DOLPHIN"]
        
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
