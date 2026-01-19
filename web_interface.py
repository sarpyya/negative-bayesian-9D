#!/usr/bin/env python3
"""
🔥 WEB INTERFACE - BAYESIAN NEGATIVE 9D 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Servidor Flask con estética terminal dark satánica.
Visualización interactiva del grafo de horror.
"""

from flask import Flask, render_template, jsonify, send_from_directory, request
from bayesian_9d import generar_grafo_9d, analizar_horror, votar_modo
from models import db, HorrorRun
import random
from pyvis.network import Network
import os
import json
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///horror_runs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Crear DB si no existe (una vez)
with app.app_context():
    db.create_all()

# Almacenar último grafo generado
ultimo_grafo = None
ultimo_analisis = None

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_graph():
    """Genera un nuevo grafo de horror y lo guarda en DB. Soporta Replay via seed."""
    global ultimo_grafo, ultimo_analisis
    
    # Check if seed provided in JSON body
    data = request.get_json(silent=True) or {}
    req_seed = data.get('seed')
    
    if req_seed is not None:
        seed = int(req_seed)
        print(f"🔄 Replaying seed: {seed}")
    else:
        seed = random.randint(1, 999999)
    
    ultimo_grafo = generar_grafo_9d(seed=seed, ramificaciones_por_nodo=3)
    ultimo_analisis = analizar_horror(ultimo_grafo, top_n=10)
    modo_nombre, modo_info = votar_modo(ultimo_analisis['horror_total'])
    
    # Guardar en DB
    try:
        new_run = HorrorRun(
            seed=seed,
            horror_total=ultimo_analisis['horror_total'],
            modo=modo_nombre,
            top_nodes=json.dumps(ultimo_analisis['nodos_mas_horribles'][:5]),
            horror_promedio=ultimo_analisis['horror_promedio'],
            total_nodos=ultimo_analisis['total_nodos']
        )
        db.session.add(new_run)
        db.session.commit()
    except Exception as e:
        print(f"Error saving to DB: {e}")
    
    return jsonify({
        'seed': seed,
        'analisis': ultimo_analisis,
        'modo': {
            'nombre': modo_nombre,
            'emoji': modo_info['emoji'],
            'desc': modo_info['desc']
        }
    })

@app.route('/api/visualize')
def visualize_graph():
    """Genera visualización HTML del grafo"""
    global ultimo_grafo
    
    if ultimo_grafo is None:
        return jsonify({'error': 'No hay grafo generado'}), 400
    
    # Crear red pyvis con estilo dark
    net = Network(
        height='800px',
        width='100%',
        bgcolor='#000000',
        font_color='#00ff41',
        directed=True
    )
    
    # Configuración física del grafo (BRUTAL MODE)
    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -12000,
          "centralGravity": 0.05,
          "springLength": 150,
          "springConstant": 0.04,
          "damping": 0.09,
          "avoidOverlap": 0.1
        },
        "minVelocity": 0.75
      },
      "nodes": {
        "font": {
          "color": "#00ff41",
          "size": 16,
          "face": "monospace"
        },
        "borderWidth": 2,
        "shadow": true
      },
      "edges": {
        "color": {
          "color": "rgba(255, 0, 51, 0.4)",
          "highlight": "#ffff00"
        },
        "smooth": {
            "type": "continuous"
        },
        "arrows": {
          "to": {
            "enabled": true,
            "scaleFactor": 0.5
          }
        }
      }
    }
    """)
    
    # Calcular max horror para scaling
    all_horrors = [data.get('horror', 0) for _, data in ultimo_grafo.nodes(data=True)]
    max_h = max(all_horrors) if all_horrors else 1

    # Añadir nodos con colores basados en horror
    for node, data in ultimo_grafo.nodes(data=True):
        horror = data.get('horror', 0)
        
        # Scaling brutal
        intensity = int(255 * (horror / max_h))
        # Ensure intensity is within 0-255
        intensity = max(0, min(255, intensity))
        
        # Color rojo dinámico basado en intensidad
        color = f'#{intensity:02x}0000'
        # Size dinámico
        size = 15 + (horror / max_h) * 50
        
        label = data.get('label', node)
        title = f"{label}<br>HORROR: {horror:.1f}<br>{data.get('desc', '')}"
        
        net.add_node(
            node,
            label=label,
            title=title,
            color=color,
            size=size,
            borderWidth=2,
            borderWidthSelected=4
        )
    
    # Añadir edges
    for u, v, data in ultimo_grafo.edges(data=True):
        weight = data.get('weight', 1.0)
        label = data.get('label', '')
        # Edges transversales más tenues
        if label == "transversal":
             net.add_edge(u, v, label="", width=1, color="rgba(100,100,100,0.3)", dashes=True)
        else:
             net.add_edge(u, v, label="", width=weight, title=f"Factor: {weight:.2f}")
    
    # Guardar HTML
    output_file = os.path.join('static', 'graph.html')
    net.save_graph(output_file)
    
    return jsonify({'status': 'ok', 'file': 'graph.html'})

@app.route('/graph')
def show_graph():
    """Muestra el grafo generado"""
    return send_from_directory('static', 'graph.html')

@app.route('/hall_of_shame')
def hall_of_shame():
    """Muestra el ranking de las peores simulaciones"""
    runs = HorrorRun.query.order_by(HorrorRun.horror_total.desc()).limit(20).all()
    # Parse top_nodes json for template
    for run in runs:
        if run.top_nodes:
            run.top_nodes_list = json.loads(run.top_nodes)
        else:
            run.top_nodes_list = []
            
    return render_template('hall.html', runs=runs)

@app.route('/api/hall')
def api_hall_of_shame():
    """API para obtener el Top N del Hall of Shame"""
    limit = int(request.args.get('limit', 10))
    runs = HorrorRun.query.order_by(HorrorRun.horror_total.desc()).limit(limit).all()
    return jsonify([run.to_dict() for run in runs])

@app.route('/api/monte_carlo', methods=['POST'])
def run_monte_carlo_endpoint():
    """Ejecuta simulación Monte Carlo"""
    n_sims = int(request.json.get('n_sims', 50))
    limit = min(n_sims, 500) # Límite de seguridad
    
    results = []
    best_worst_horror = -1
    best_worst_seed = -1
    
    for _ in range(limit):
        current_seed = random.randint(1, 999999)
        g = generar_grafo_9d(seed=current_seed, ramificaciones_por_nodo=3)
        analytics = analizar_horror(g, top_n=1)
        
        horror = analytics['horror_total']
        results.append(horror)
        
        if horror > best_worst_horror:
            best_worst_horror = horror
            best_worst_seed = current_seed
            
            # Guardamos el PEOR histórico si supera cierto umbral, o siempre?
            # Por ahora guardemos solo el winner de la ronda en DB
    
    # Guardar el ganador de Monte Carlo en DB
    winner_graph = generar_grafo_9d(seed=best_worst_seed)
    winner_analysis = analizar_horror(winner_graph, top_n=5)
    winner_modo, _ = votar_modo(winner_analysis['horror_total'])
    
    try:
        new_run = HorrorRun(
            seed=best_worst_seed,
            horror_total=winner_analysis['horror_total'],
            modo=winner_modo,
            top_nodes=json.dumps(winner_analysis['nodos_mas_horribles'][:5]),
            horror_promedio=winner_analysis['horror_promedio'],
            total_nodos=winner_analysis['total_nodos']
        )
        db.session.add(new_run)
        db.session.commit()
    except Exception as e:
        print(f"Error saving Monte Carlo run: {e}")
            
    return jsonify({
        'simulations': limit,
        'max_horror': max(results),
        'min_horror': min(results),
        'avg_horror': sum(results) / len(results),
        'worst_seed': best_worst_seed,
        'histogram_data': results # Para el frontend
    })

@app.route('/visualize/seed/<int:seed>')
def visualize_seed_route(seed):
    """Visualiza directamente un seed específico sin pasar por generate"""
    grafo = generar_grafo_9d(seed=seed, ramificaciones_por_nodo=3)
    
    # Crear red pyvis
    net = Network(
        height='100vh', 
        width='100%', 
        bgcolor='#000000', 
        font_color='#00ff41',
        directed=True
    )
    
    # Misma configuración física del grafo (BRUTAL)
    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -12000,
          "centralGravity": 0.05,
          "springLength": 150,
          "springConstant": 0.04,
          "damping": 0.09,
          "avoidOverlap": 0.1
        },
        "minVelocity": 0.75
      },
      "nodes": {
        "font": { "color": "#00ff41", "size": 16, "face": "monospace" },
        "borderWidth": 2, "shadow": true
      },
      "edges": {
        "color": { "color": "rgba(255, 0, 51, 0.4)", "highlight": "#ffff00" },
        "smooth": { "type": "continuous" },
        "arrows": { "to": { "enabled": true, "scaleFactor": 0.5 } }
      }
    }
    """)
    
    # Calcular max horror para scaling
    all_horrors = [data.get('horror', 0) for _, data in grafo.nodes(data=True)]
    max_h = max(all_horrors) if all_horrors else 1

    # Añadir nodos
    for node, data in grafo.nodes(data=True):
        horror = data.get('horror', 0)
        # Scaling brutal
        intensity = int(255 * (horror / max_h))
        intensity = max(0, min(255, intensity))
        
        color = f'#{intensity:02x}0000'
        size = 15 + (horror / max_h) * 50
            
        label = data.get('label', node)
        title = f"{label}<br>HORROR: {horror:.1f}<br>{data.get('desc', '')}"
        
        net.add_node(node, label=label, title=title, color=color, size=size, borderWidth=2)
    
    # Añadir edges
    for u, v, data in grafo.edges(data=True):
        weight = data.get('weight', 1.0)
        label = data.get('label', '')
        if label == "transversal":
             net.add_edge(u, v, width=1, color="rgba(100,100,100,0.3)", dashes=True)
        else:
             net.add_edge(u, v, width=weight, title=f"Factor: {weight:.2f}")
        
    # Guardar en temp
    filename = f"graph_{seed}.html"
    path = os.path.join('static', filename)
    net.save_graph(path)
    
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Crear directorio static si no existe
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    print("🔥 Iniciando servidor Bayesian Negative 9D + Persistence + Monte Carlo...")
    print("📡 Abre http://localhost:5000 en tu navegador")
    print("💀 Ctrl+C para salir\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
