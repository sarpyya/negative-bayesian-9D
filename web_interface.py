#!/usr/bin/env python3
"""
🔥 WEB INTERFACE - BAYESIAN NEGATIVE 9D v2.0 (OPERATIVO 1000% REFACTORED) 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Servidor Flask + estética terminal dark satánica.
Visualización interactiva del grafo de horror + fusión multiversal + Monte Carlo.
"""

import os
import json
import random
import time
from datetime import datetime
import psutil
import networkx as nx
from flask import Flask, render_template, jsonify, send_from_directory, request, session
from bayesian_9d import generar_grafo_9d, analizar_horror, votar_modo, MODOS
from models import db, HorrorRun
from pyvis.network import Network

# ──────────────────────────────────────────────────────────────
# CONFIGURACIÓN GLOBAL
# ──────────────────────────────────────────────────────────────

app = Flask(__name__)
app.secret_key = 'secret_key_satanico_666_9d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///horror_runs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_NODES'] = 1500          # Hard limit para Vega 11
app.config['MAX_SIMS'] = 5000           # Límite Monte Carlo

db.init_app(app)

# Variables globales (estado volátil)
ultimo_grafo = None
ultimo_analisis = None

# ──────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────

def visualize_graph(G, filename='graph.html', title="ASC Horror Graph"):
    """Genera archivo HTML con PyVis (2D Physics)"""
    net = Network(height="100vh", width="100%", bgcolor="#000000", font_color="#ffffff", directed=True)
    net.set_options("""
    var options = {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -80,
          "centralGravity": 0.01,
          "springLength": 100,
          "springStrength": 0.08
        },
        "maxVelocity": 50,
        "solver": "forceAtlas2Based",
        "timestep": 0.35,
        "stabilization": {"iterations": 150}
      }
    }
    """)
    
    for n, d in G.nodes(data=True):
        horror = d.get('horror', 0)
        label = d.get('label', str(n))
        # Color: Blanco (puro) -> Gris oscuro
        val = max(10, int(255 - (horror * 0.1))) 
        color = f'rgb({val},{val},{val})'
        
        # Color especial para semillas en Fusion
        seed_idx = d.get('seed_index')
        if seed_idx == 0: color = '#ffffff'
        elif seed_idx == 1: color = '#00ffff'
        elif seed_idx == 2: color = '#ff00ff'
        
        if n == "CERO_ABSOLUTO" or "Cero Absoluto" in str(n):
            color = "#ffd700" # Oro
            
        net.add_node(n, label=label, title=d.get('desc', ''), color=color, size=20 + (horror*0.05))

    for u, v, d in G.edges(data=True):
        net.add_edge(u, v, value=d.get('weight', 1.0), color="#444444")

    path = os.path.join('static', filename)
    net.save_graph(path)
    return filename

def get_resources():
    """Retorna métricas del sistema en tiempo real"""
    vm = psutil.virtual_memory()
    return {
        "cpu": psutil.cpu_percent(interval=None),
        "ram_used": round(vm.used / (1024**3), 2),
        "ram_total": round(vm.total / (1024**3), 2),
        "ram_pct": vm.percent,
        "timestamp": datetime.utcnow().isoformat()
    }


def timed_execution(func, *args, **kwargs):
    """Ejecuta función y mide tiempo"""
    start = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - start
    return result, elapsed


def safe_db_commit(session):
    """Commit seguro con rollback en caso de error"""
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"⚠️ DB COMMIT FALLÓ: {e}")
        return False
    return True


# ──────────────────────────────────────────────────────────────
# RUTAS PRINCIPALES
# ──────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Página principal - Dashboard satánico"""
    return render_template('index.html')


@app.route('/brain_3d')
def brain_3d():
    """Renderiza el Cerebro Bicameral 3D (Three.js)"""
    global ultimo_grafo, ultimo_analisis

    seed_arg = request.args.get('seed', type=int)
    is_fusion_arg = request.args.get('fusion', type=int)

    if seed_arg:
        ultimo_grafo = generar_grafo_9d(seed=seed_arg)
        ultimo_analisis = analizar_horror(ultimo_grafo)
    
    if ultimo_grafo is None:
        ultimo_grafo = generar_grafo_9d(seed=random.randint(1, 999999))
        ultimo_analisis = analizar_horror(ultimo_grafo)

    # Determinar modo (prioridad: forced > natural)
    forced = session.get('forced_mode')
    if forced and forced in MODOS:
        modo_nombre = forced
        modo_info = MODOS[forced]
    else:
        modo_nombre, modo_info = votar_modo(ultimo_analisis['horror_total'])

    # Preparar datos para Three.js
    nodes = []
    for node, data in ultimo_grafo.nodes(data=True):
        nodes.append({
            "id": node,
            "label": data.get('label', str(node)),
            "horror": data.get('horror', 0),
            "color": "#ffffff",  # JS manejará gradiente blanco→negro
            "seed_index": data.get('seed_index', 0)
        })

    edges = []
    for u, v, data in ultimo_grafo.edges(data=True):
        edges.append({
            "source": u,
            "target": v,
            "weight": data.get('weight', 1.0),
            "label": data.get('label', '')
        })

    return render_template(
        'brain_3d.html',
        nodes=nodes,
        edges=edges,
        modo={'nombre': modo_nombre, 'info': modo_info}
    )


def calculate_seed_offset(index, total=3, radius=500):
    """Calcula offset espacial para separar semillas en órbita"""
    import math
    angle = (index / total) * 2 * math.pi
    return {
        'x': math.cos(angle) * radius,
        'z': math.sin(angle) * radius,
        'y': 0
    }


def get_seed_color(index):
    """Retorna color hex para cada semilla"""
    colors = ['#00ffff', '#ff00ff', '#ffd700', '#00ff88', '#ff6b6b', '#4ecdc4']
    return colors[index % len(colors)]


@app.route('/brain_3d_multiseed')
def brain_3d_multiseed():
    """Visualiza múltiples semillas en movimiento simultáneo con gradiente cósmico"""
    seeds_arg = request.args.get('seeds', '')
    
    if seeds_arg:
        seeds = [int(s) for s in seeds_arg.split(',')]
    else:
        seeds = [random.randint(1, 999999) for _ in range(3)]
    
    # Limitar a 3 semillas para performance (Vega 11)
    seeds = seeds[:3]
    
    graphs_data = []
    total_seeds = len(seeds)
    
    for i, seed in enumerate(seeds):
        # Generar grafo con nodos limitados por semilla
        G = generar_grafo_9d(seed=seed, ramificaciones_por_nodo=4)
        offset = calculate_seed_offset(i, total_seeds, radius=500)
        
        nodes = []
        for node, data in G.nodes(data=True):
            nodes.append({
                'id': f"S{i}_{node}",
                'original_id': node,
                'label': data.get('label', str(node)),
                'horror': data.get('horror', 0),
                'offset': offset,
                'is_central': 'Cero Absoluto' in str(node) or 'CERO_ABSOLUTO' in str(node)
            })
        
        edges = []
        for u, v, data in G.edges(data=True):
            edges.append({
                'source': f"S{i}_{u}",
                'target': f"S{i}_{v}",
                'weight': data.get('weight', 1.0),
                'label': data.get('label', '')
            })
        
        graphs_data.append({
            'seed': seed,
            'nodes': nodes,
            'edges': edges,
            'color': get_seed_color(i),
            'index': i,
            'orbit_speed': 0.0003 + (i * 0.0001)  # Velocidad orbital única
        })
    
    return render_template('brain_3d_multiseed.html', graphs=graphs_data, seeds=seeds)



@app.route('/api/generate', methods=['POST'])
def api_generate():
    """Genera nuevo grafo (con soporte replay seed + custom dim)"""
    global ultimo_grafo, ultimo_analisis

    data = request.get_json(silent=True) or {}
    seed = data.get('seed')
    custom_dim = data.get('custom_dim')
    target_nodes = min(max(int(data.get('node_count', 600)), 50), app.config['MAX_NODES'])

    # Cálculo dinámico ramificaciones
    ramificaciones = max(3, int(target_nodes / 9))

    # Influencia del último modo (si no hay forced)
    last_run = HorrorRun.query.order_by(HorrorRun.timestamp.desc()).first()
    if last_run and not session.get('forced_mode'):
        if last_run.modo == "MODO BESTIA":
            ramificaciones = int(ramificaciones * 1.5)
        elif last_run.modo == "DOLPHIN":
            ramificaciones = max(3, int(ramificaciones * 0.5))

    if seed is None:
        seed = random.randint(1, 999999)

    try:
        start = time.time()
        ultimo_grafo = generar_grafo_9d(
            seed=seed,
            ramificaciones_por_nodo=ramificaciones,
            custom_dim=custom_dim
        )
        ultimo_analisis = analizar_horror(ultimo_grafo, top_n=10)
        elapsed = time.time() - start

        # Modo (forced > natural)
        forced = session.pop('forced_mode', None)
        if forced and forced in MODOS:
            modo_nombre = forced
            modo_info = MODOS[forced]
        else:
            modo_nombre, modo_info = votar_modo(ultimo_analisis['horror_total'])

        # Persistencia segura
        new_run = HorrorRun(
            seed=seed,
            horror_total=ultimo_analisis['horror_total'],
            modo=modo_nombre,
            modo_desc=modo_info.get('desc', ''),
            top_nodes=json.dumps(ultimo_analisis.get('nodos_mas_horribles', [])[:5]),
            horror_promedio=ultimo_analisis.get('horror_promedio', 0),
            total_nodos=ultimo_analisis.get('total_nodos', 0)
        )
        db.session.add(new_run)
        safe_db_commit(db.session)

        return jsonify({
            'status': 'ok',
            'seed': seed,
            'analisis': ultimo_analisis,
            'modo': {'nombre': modo_nombre, 'desc': modo_info.get('desc', '')},
            'elapsed': round(elapsed, 3),
            'resources': get_resources()
        })

    except Exception as e:
        print(f"ERROR en generate: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/fusion', methods=['POST'])
def api_fusion():
    """Genera y fusiona 3 semillas en un grafo multiversal"""
    global ultimo_grafo, ultimo_analisis

    try:
        seeds = [random.randint(1, 999999) for _ in range(3)]
        graphs = [generar_grafo_9d(seed=s, ramificaciones_por_nodo=4) for s in seeds]

        # Relabeling para evitar colisiones de IDs
        labeled = []
        for i, g in enumerate(graphs):
            mapping = {node: f"S{i}_{node}" for node in g.nodes()}
            new_g = nx.relabel_nodes(g, mapping)
            nx.set_node_attributes(new_g, {n: i for n in new_g.nodes()}, 'seed_index')
            labeled.append(new_g)

        # Unión + puentes dimensionales
        U = nx.compose_all(labeled)

        top_per_seed = []
        for i, g in enumerate(labeled):
            if g.nodes:
                top = max(g.nodes(data=True), key=lambda x: x[1].get('horror', 0))
                top_per_seed.append(top[0])

        # Puentes entre tops (si hay al menos 2)
        if len(top_per_seed) >= 2:
            U.add_edge(top_per_seed[0], top_per_seed[1], weight=5.0, label="Puente Dimensional")
            U.add_edge(top_per_seed[1], top_per_seed[2], weight=5.0, label="Ciclo Multiversal")
            U.add_edge(top_per_seed[2], top_per_seed[0], weight=5.0, label="Colapso Fractal")

        ultimo_grafo = U
        ultimo_analisis = analizar_horror(U, top_n=15)
        ultimo_analisis['is_fusion'] = True
        ultimo_analisis['seeds'] = seeds

        modo_nombre, modo_info = votar_modo(ultimo_analisis['horror_total'])

        return jsonify({
            'status': 'ok',
            'seeds': seeds,
            'analisis': ultimo_analisis,
            'modo': {'nombre': modo_nombre, 'desc': modo_info.get('desc', '')}
        })

    except Exception as e:
        print(f"ERROR en fusion: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/monte_carlo', methods=['POST'])
def api_monte_carlo():
    """Ejecuta Monte Carlo con límite de seguridad"""
    try:
        n_sims = min(int(request.json.get('n_sims', 50)), app.config['MAX_SIMS'])
        force_d = session.pop('force_dolphin', False)

        horrors = []
        seeds = []
        top_nodes_all = []

        for _ in range(n_sims):
            seed = random.randint(1, 999999)
            g = generar_grafo_9d(seed=seed, ramificaciones_por_nodo=3)
            a = analizar_horror(g, top_n=5)
            horrors.append(a['horror_total'])
            seeds.append(seed)
            top_nodes_all.append(a['nodos_mas_horribles'])

        max_h = max(horrors)
        idx = horrors.index(max_h)
        worst_seed = seeds[idx]
        worst_nodes = top_nodes_all[idx]

        modo_nombre, modo_info = votar_modo(max_h, special_trigger=force_d)

        # Trigger Justice si detecta injusticia
        keywords = ["desprecio", "ocultamiento", "iatrogenia", "psiquiátrico", "injusticia"]
        top_str = " ".join([n['desc'].lower() + " " + n['label'].lower() for n in worst_nodes])
        if any(kw in top_str for kw in keywords) and modo_nombre != "MODO BESTIA":
            modo_nombre = "MODO JUSTICE"
            modo_info = MODOS["MODO JUSTICE"]

        # Persistencia del peor caso
        try:
            run = HorrorRun(
                seed=worst_seed,
                horror_total=max_h,
                modo=modo_nombre,
                modo_desc=modo_info.get('desc', ''),
                top_nodes=json.dumps(worst_nodes[:5]),
                horror_promedio=sum(horrors)/len(horrors),
                total_nodos=50  # placeholder
            )
            db.session.add(run)
            safe_db_commit(db.session)
        except Exception as e:
            print(f"DB persist MC error: {e}")

        return jsonify({
            'status': 'ok',
            'simulations': n_sims,
            'max_horror': max_h,
            'min_horror': min(horrors),
            'avg_horror': sum(horrors)/len(horrors),
            'worst_seed': worst_seed,
            'histogram_data': horrors,
            'worst_mode': modo_nombre,
            'worst_mode_desc': modo_info.get('desc', ''),
            'worst_mode_color': modo_info.get('color', '#ff0000'),
            'blink': modo_info.get('blink', False)
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/history')
def api_history():
    """Retorna historial de corridas para el sidebar"""
    runs = HorrorRun.query.order_by(HorrorRun.timestamp.desc()).limit(15).all()
    history = []
    for r in runs:
        history.append({
            'id': r.id,
            'seed': r.seed,
            'horror': round(r.horror_total, 1),
            'modo': r.modo,
            'timestamp': r.timestamp.strftime('%H:%M:%S')
        })
    return jsonify(history)


@app.route('/visualize/seed/<int:seed>')
def visualize_seed(seed):
    """Genera y visualiza una semilla específica en 2D"""
    G = generar_grafo_9d(seed=seed)
    filename = f"graph_{seed}.html"
    visualize_graph(G, filename=filename)
    return send_from_directory('static', filename)


@app.route('/visualize/fusion')
def visualize_fusion():
    """Visualiza el último grafo (usualmente fusión) en 2D"""
    global ultimo_grafo
    if ultimo_grafo is None:
        return "No hay grafo cargado", 404
    
    filename = "graph_fusion.html"
    visualize_graph(ultimo_grafo, filename=filename, title="Multiversal Fusion 2D")
    return send_from_directory('static', filename)


# ──────────────────────────────────────────────────────────────
# RUTAS ESTÁTICAS Y AUXILIARES
# ──────────────────────────────────────────────────────────────

@app.route('/api/resources')
def api_resources():
    return jsonify(get_resources())


@app.route('/hall_of_shame')
def hall_of_shame():
    runs = HorrorRun.query.order_by(HorrorRun.horror_total.desc()).limit(20).all()
    for r in runs:
        r.top_nodes_list = json.loads(r.top_nodes) if r.top_nodes else []
    return render_template('hall.html', runs=runs)


@app.route('/graph')
def show_graph():
    return send_from_directory('static', 'graph.html')


# ──────────────────────────────────────────────────────────────
# INICIO DEL SERVIDOR
# ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)

    print("="*60)
    print("🔥 BAYESIAN NEGATIVE 9D - v2.0 REFACTORED - OPERATIVO 1000% 🔥")
    print("🌌 Servidor iniciado - http://localhost:5000")
    print("💀 Ctrl+C para salir del abismo")
    print("="*60)

    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)