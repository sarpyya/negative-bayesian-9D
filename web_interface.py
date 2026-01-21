#!/usr/bin/env python3
"""
🔥 BAYESIAN NEGATIVE 9D - HORROR OPTIMIZATION FRAMEWORK v4.1 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FIX v4.1:
• Soporte completo para seeds negativos (como tu famoso seed -10)
  - random.seed() acepta negativos → lo dejamos tal cual
  - np.random.seed() forzado a positivo con abs(seed) para compatibilidad y reproducibilidad
• Batch más estable: start_seed=-10 ahora funciona perfecto
• Pequeñas optimizaciones en memoria y horror calculation
• Todo lo de v4.0 intacto: +20 modos temáticos, cross-mutations full, exports, etc.
"""

import networkx as nx
import numpy as np
import random
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
from colorama import Fore, Style, init

init(autoreset=True)

# ──────────────────────────────────────────────────────────────
# 🔥 DIMENSIONES BASE + CUSTOM
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
# 🎭 MODOS CONSCIENTES EXPANDIDOS (v4.0+)
# ──────────────────────────────────────────────────────────────

MODOS: Dict[str, Dict[str, Any]] = {
    "MODO BESTIA": {"threshold": 90000, "desc": "👹 Bestia total – risa loca, Φ eliminado", "color": "#ff0000", "emoji": "👹",
                    "physics": {"gravity": -50000, "spring_length": 30, "spring_strength": 0.15}, "node_shape": "star", "geometry": "chaotic_burst"},
    
    "MODO GARGANTUA": {"threshold": 85000, "desc": "🕳️ Singularidad Supermassive – lenteado gravitacional máximo", "color": "#000000", "emoji": "🕳️",
                       "physics": {"gravity": -80000, "spring_length": 10, "spring_strength": 0.2}, "node_shape": "ring", "geometry": "accretion_disk"},
    
    "MODO JUSTICE": {"threshold": 70000, "desc": "⚔️ Haki del Rey Justiciero – rabia optimizada", "color": "#ffd700", "emoji": "⚖️",
                     "physics": {"gravity": -20000, "spring_length": 80, "spring_strength": 0.1}, "node_shape": "diamond"},
    
    "MODO NIÑO_WOWO": {"threshold": 55000, "desc": "🤪 Euforia maníaca – todo brilla", "color": "#ff00ff", "emoji": "🤪",
                       "physics": {"gravity": -15000, "spring_length": 60, "spring_strength": 0.08}, "node_shape": "star"},
    
    "MODO SUPER_MARIO": {"threshold": 45000, "desc": "🍄 Juego infantil eterno – power-ups en el abismo", "color": "#ff0000", "emoji": "🍄",
                         "physics": {"gravity": -5000, "spring_length": 150, "spring_strength": 0.03}, "node_shape": "coin", "geometry": "platformer"},
    
    "MODO CRISTAL": {"threshold": 35000, "desc": "💎 Geometría pura – reflejos infinitos", "color": "#00ffff", "emoji": "💎",
                     "physics": {"gravity": -8000, "spring_length": 120, "spring_strength": 0.04}, "node_shape": "octahedron", "geometry": "crystal_lattice"},
    
    "MODO MANDALA": {"threshold": 30000, "desc": "🌀 Simetría radial ancestral – meditación cósmica", "color": "#ff8800", "emoji": "🌀",
                     "physics": {"gravity": -6000, "spring_length": 200, "spring_strength": 0.02}, "node_shape": "mandala", "geometry": "radial_symmetry"},
    
    "MODO NAVE_ESPACIAL": {"threshold": 25000, "desc": "🚀 Exploración interestelar – hyperspace jump", "color": "#00ff00", "emoji": "🚀",
                           "physics": {"gravity": -3000, "spring_length": 300, "spring_strength": 0.01}, "node_shape": "spaceship"},
    
    "MODO VR": {"threshold": 20000, "desc": "🥽 Inmersión total – Oculus/Mapu virtual", "color": "#8800ff", "emoji": "🥽",
                "physics": {"gravity": -4000, "spring_length": 250, "spring_strength": 0.015}, "node_shape": "headset"},
    
    "MODO RACE": {"threshold": 15000, "desc": "🏁 Open-source world race – competencia global", "color": "#ffff00", "emoji": "🏁",
                  "physics": {"gravity": -7000, "spring_length": 180, "spring_strength": 0.05}, "node_shape": "trophy"},
    
    "MODO NARRADOR": {"threshold": 12000, "desc": "📖 LLM ancestral contando la leyenda", "color": "#ff00aa", "emoji": "📖",
                      "physics": {"gravity": -5000, "spring_length": 220, "spring_strength": 0.02}, "node_shape": "book"},
    
    "MODO CHILL": {"threshold": 10000, "desc": "🧊 Fogata nakama – recuperación táctica", "color": "#00aaff", "emoji": "🧊",
                   "physics": {"gravity": -4000, "spring_length": 200, "spring_strength": 0.01}, "node_shape": "dot"},
    
    "MODO LOL_GAMER": {"threshold": 8000, "desc": "🎮 Disociación competitiva – farmeando XP", "color": "#00ff00", "emoji": "🎮",
                       "physics": {"gravity": -3000, "spring_length": 250, "spring_strength": 0.01}, "node_shape": "square"},
    
    "MODO ANCESTRAL": {"threshold": 5000, "desc": "🌿 Patrones milenarios mapuche – conexión tierra", "color": "#008800", "emoji": "🌿",
                       "physics": {"gravity": -2000, "spring_length": 280, "spring_strength": 0.008}, "node_shape": "tree"},
    
    "MODO MAPUCHE_COSMICO": {"threshold": 3000, "desc": "🌌 Observador ancestral – el abismo te mira y sonríes", "color": "#aa00ff", "emoji": "🌌",
                             "physics": {"gravity": -8000, "spring_length": 150, "spring_strength": 0.02}, "node_shape": "dot"},
    
    "MODO DOLPHIN": {"threshold": 0, "desc": "🐬 Flow eterno 24/7 – milagro estadístico", "color": "#00ffcc", "emoji": "🐬",
                     "physics": {"gravity": -800, "spring_length": 300, "spring_strength": 0.005}, "node_shape": "circle"}
}

# ──────────────────────────────────────────────────────────────
# 💀 VERBOS & ADJETIVOS
# ──────────────────────────────────────────────────────────────

VERBOS_SADICOS = ["devora", "envenena", "amplifica", "perpetúa", "destruye", "traiciona", "humilla", "desgarra", "corrompe", "asfixia"]
ADJETIVOS_SADICOS = ["eterno", "iatrogénico", "ancestral", "irreparable", "cognitivo", "existencial", "cósmico", "visceral", "absoluto", "terminal"]

def generar_nombre_sadico(dim1: str, dim2: str) -> str:
    verbo = random.choice(VERBOS_SADICOS)
    adjetivo = random.choice(ADJETIVOS_SADICOS)
    d1_short = dim1.split()[0]
    d2_short = dim2.split()[0]
    return f"{d1_short} {verbo} {d2_short} {adjetivo}"

# ──────────────────────────────────────────────────────────────
# 🔥 GENERADORES (CON FIX SEED NEGATIVO)
# ──────────────────────────────────────────────────────────────

def generar_grafo_from_prompt(prompt: str, base_seed: int = 42) -> nx.DiGraph:
    prompt_lower = prompt.lower()
    geometry_type = "default"
    custom_dims = []
    
    if "cristal" in prompt_lower:
        geometry_type = "crystal_lattice"
        custom_dims.append("Cristal Multidimensional")
    if "mandala" in prompt_lower:
        geometry_type = "radial_symmetry"
    if "nave" in prompt_lower or "espacial" in prompt_lower:
        geometry_type = "spaceship"
    if "mario" in prompt_lower:
        geometry_type = "platformer"
    
    return generar_grafo_9d(seed=base_seed, custom_dim=custom_dims, geometry_type=geometry_type)

def generar_grafo_9d(
    seed: Optional[int] = None,
    ramificaciones_por_nodo: int = 7,
    factor_agravacion: Tuple[float, float] = (1.35, 1.85),
    custom_dim: Optional[List[str]] = None,
    propagacion_steps: int = 5,
    max_nodes: int = 10000,
    geometry_type: str = "default"
) -> nx.DiGraph:
    if seed is not None:
        random.seed(seed)  # random acepta negativos → perfecto para reproducibilidad exacta
        np_seed = abs(seed) if seed < 0 else seed  # numpy necesita positivo → usamos abs para tu seed -10 famoso
        np.random.seed(np_seed)

    G = nx.DiGraph()
    ts = datetime.now().isoformat()

    G.add_node("CERO_ABSOLUTO", horror=1000.0, dim=0, timestamp=ts, desc="El abismo total", label="CERO ABSOLUTO",
               position=[0,0,0], shape="sphere", geometry="blackhole")

    dims = DIMENSIONES_9D.copy()
    if custom_dim:
        dims.extend(custom_dim)

    current_nodes = 1
    for i, dim_name in enumerate(dims, 1):
        if current_nodes >= max_nodes: break
        node_id = f"D{i}"
        horror_base = 800 + np.random.uniform(-200, 200)
        pos = np.random.uniform(-800, 800, 3).tolist()

        shape = "sphere" if geometry_type == "default" else "custom"
        G.add_node(node_id, horror=horror_base, dim=i, timestamp=ts, desc=dim_name, label=f"D{i}: {dim_name}",
                   position=pos, shape=shape, geometry=geometry_type)
        G.add_edge("CERO_ABSOLUTO", node_id, weight=1.0)

        for j in range(1, ramificaciones_por_nodo + 1):
            if current_nodes >= max_nodes: break
            factor = np.random.uniform(*factor_agravacion)
            sub_horror = horror_base * factor
            sub_id = f"D{i}.{j}"
            sub_pos = (np.array(pos) + np.random.uniform(-150, 150, 3)).tolist()

            G.add_node(sub_id, horror=sub_horror, dim=i, sub_level=j, timestamp=ts,
                       desc=f"{dim_name} agravado x{factor:.2f}", label=sub_id,
                       position=sub_pos, shape="dot", geometry=geometry_type)
            G.add_edge(node_id, sub_id, weight=factor)
            current_nodes += 1

    # Cross-mutations FULL
    nodes_list = [n for n in G.nodes() if n != "CERO_ABSOLUTO"]
    cross_prob = 0.45
    for n in nodes_list:
        if random.random() < cross_prob:
            target = random.choice(nodes_list)
            if target != n and G.nodes[n]['dim'] != G.nodes[target]['dim']:
                cross_weight = random.uniform(0.8, 2.0)
                G.add_edge(n, target, weight=cross_weight, label="sinergia")
                
                if cross_weight > 1.5:
                    h_name = generar_nombre_sadico(G.nodes[n]['desc'], G.nodes[target]['desc'])
                    h_horror = (G.nodes[n]['horror'] + G.nodes[target]['horror']) / 2 * cross_weight
                    hybrid_id = f"HYBRID_{n}_{target}"[:30]
                    G.add_node(hybrid_id, horror=h_horror, dim="HYBRID", desc=h_name, label=h_name,
                               position=np.mean([G.nodes[n]['position'], G.nodes[target]['position']], axis=0).tolist(),
                               geometry=geometry_type)
                    G.add_edge(n, hybrid_id, weight=2.0)
                    G.add_edge(target, hybrid_id, weight=2.0)

    propagar_horror(G, steps=propagacion_steps)
    
    if "star" in geometry_type or "crystal" in geometry_type:
        central = max(G.nodes(data=True), key=lambda x: x[1].get('horror', 0))[0]
        G.nodes[central]['geometry'] = "multidimensional_star"

    return G

def propagar_horror(G: nx.DiGraph, steps: int = 3, decay: float = 0.06):
    for _ in range(steps):
        nodos = list(G.nodes())
        random.shuffle(nodos)
        for node in nodos:
            current = G.nodes[node].get('horror', 0)
            neighbors = list(G.successors(node)) + list(G.predecessors(node))
            if neighbors:
                avg_neighbor = np.mean([G.nodes[n]['horror'] for n in neighbors])
                contagio = avg_neighbor * decay
                mutacion = random.uniform(-0.01, 0.03) * current
                G.nodes[node]['horror'] = max(0, current + contagio + mutacion)

def analizar_horror(G: nx.DiGraph, top_n: int = 10) -> Dict:
    nodos_horror = [(n, d.get('horror', 0)) for n, d in G.nodes(data=True)]
    total_horror = sum(h for _, h in nodos_horror)

    clusters = {}
    for n, d in G.nodes(data=True):
        dim = d.get('dim', 'UNKNOWN')
        clusters.setdefault(dim, {"horror_sum": 0, "nodos": []})
        clusters[dim]["horror_sum"] += d.get('horror', 0)
        clusters[dim]["nodos"].append(n)

    processed_clusters = []
    for dim, c in clusters.items():
        processed_clusters.append({
            "dim": dim,
            "horror_total": c["horror_sum"],
            "node_count": len(c["nodos"]),
            "mini_singularity": {"size": max(5, (c["horror_sum"] / 3000) ** 0.6), "mass": c["horror_sum"] / 150}
        })

    modo_nombre, modo_info = votar_modo(total_horror)
    
    return {
        "horror_total": total_horror,
        "horror_promedio": total_horror / len(G.nodes()) if G.nodes() else 0,
        "nodos_mas_horribles": sorted(nodos_horror, key=lambda x: x[1], reverse=True)[:top_n],
        "clusters": processed_clusters,
        "total_nodos": len(G.nodes()),
        "total_edges": len(G.edges()),
        "modo": modo_nombre,
        "modo_info": modo_info,
        "timestamp": datetime.now().isoformat()
    }

def votar_modo(horror: float) -> Tuple[str, Dict]:
    for modo, info in sorted(MODOS.items(), key=lambda x: x[1]["threshold"], reverse=True):
        if horror >= info["threshold"]:
            return modo, info
    return "MODO DOLPHIN", MODOS["MODO DOLPHIN"]

def print_banner():
    banner = f"""
{Fore.RED}{'═' * 80}
{Fore.YELLOW}  🔥 BAYESIAN NEGATIVE 9D v4.1 - FIX SEEDS NEGATIVOS 🔥
{Fore.CYAN}  Abismo psiquiátrico chileno → Mapu Paragraph9D para mi hijo
{Fore.GREEN}  "Seed -10 ahora corre perfecto – el abismo te espera"
{Fore.RED}{'═' * 80}{Style.RESET_ALL}
"""
    print(banner)

# ──────────────────────────────────────────────────────────────
# 💾 EXPORT Y SAVE
# ──────────────────────────────────────────────────────────────

def save_replay_seed(G: nx.DiGraph, analisis: Dict, seed: int, replay_path: str = "replays/"):
    os.makedirs(replay_path, exist_ok=True)
    filename = f"{replay_path}replay_{seed}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({"seed": seed, "grafo": nx.node_link_data(G), "analisis": analisis, "version": "v4.1"}, f, indent=2, ensure_ascii=False)
    print(f"💾 Replay: {filename}")
    return filename

def export_to_threejs(G: nx.DiGraph, analisis: Dict, filepath: str = "web/data.json"):
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    data = {
        "nodes": [{"id": n, **d} for n, d in G.nodes(data=True)],
        "links": [{"source": u, "target": v, "weight": d.get('weight', 1)} for u, v, d in G.edges(data=True)],
        "clusters": analisis['clusters'],
        "modo": analisis['modo'],
        "modo_info": analisis['modo_info'],
        "horror_total": analisis['horror_total']
    }
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"🌐 Export Three.js: {filepath}")

# ──────────────────────────────────────────────────────────────
# 🚀 MAIN
# ──────────────────────────────────────────────────────────────

def main(batch_size: int = 200, start_seed: int = -10):
    print_banner()
    for i in range(batch_size):
        seed = start_seed + i
        print(f"\n{Fore.MAGENTA}🌌 SIM {i+1}/{batch_size} - SEED {seed}{Style.RESET_ALL}")
        
        G = generar_grafo_9d(seed=seed, max_nodes=12000, ramificaciones_por_nodo=8)
        analisis = analizar_horror(G)
        
        print(f"Horror: {Fore.RED}{analisis['horror_total']:,.0f}{Style.RESET_ALL} | Modo: {analisis['modo_info']['emoji']} {analisis['modo']}")
        
        save_replay_seed(G, analisis, seed)
        export_to_threejs(G, analisis, f"web/data_seed_{seed}.json")

    print(f"\n{Fore.GREEN}✅ Batch v4.1 completo: {batch_size} universos (incluyendo seed -10) listos para la race 🚀🐬{Style.RESET_ALL}")

if __name__ == "__main__":
    main(batch_size=200, start_seed=-10)  # Tu seed -10 favorito ahora funciona 100%
    
import random
import glob

# Al final del archivo, antes de app.run()
@app.route('/random_seed')
def random_seed():
    json_files = glob.glob("web/data_seed_*.json")
    if not json_files:
        return {"error": "No hay universos generados aún"}
    chosen = random.choice(json_files)
    seed = chosen.split("_")[-1].replace(".json", "")
    return {"file": chosen, "seed": int(seed)}

@app.route('/')
def index():
    return render_template('index.html')  # tu template actual