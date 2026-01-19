#!/usr/bin/env python3
"""
🔥 WEB INTERFACE - BAYESIAN NEGATIVE 9D 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Servidor Flask con estética terminal dark satánica.
Visualización interactiva del grafo de horror.
"""

from flask import Flask, render_template, jsonify, send_from_directory, request, session
from bayesian_9d import generar_grafo_9d, analizar_horror, votar_modo, MODOS
from models import db, HorrorRun
import random
from pyvis.network import Network
import os
import json
import datetime

app = Flask(__name__)
app.secret_key = 'secret_key_satanico_666' # Necesario flashear mensajes y session
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///horror_runs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Crear DB si no existe (una vez)
with app.app_context():
    # ⚠️ RESET DB SOLO SI NO EXISTE TABLA PARA EVITAR CRASH POR ESQUEMA NUEVO
    # OJO: Si agregaste columnas, mejor borrar manualmente o aquí:
    db_path = 'instance/horror_runs.db' if os.path.exists('instance') else 'horror_runs.db'
    # db.create_all() lo hace automático, pero si cambiamos modelo, el alter table falla en sqlite
    # Para this run, asumimos que el usuario permite reset
    try:
        db.create_all() 
    except:
        pass # Si falla, es porque ya existe.

# Almacenar último grafo generado
ultimo_grafo = None
ultimo_analisis = None

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/force_dolphin', methods=['POST'])
def force_dolphin():
    # Fuerza Dolphin en la próxima visualización o simulación
    session['force_dolphin'] = True
    return jsonify({"message": "🐬 Modo Dolphin forzado. El milagro improbable está en marcha..."})

@app.route('/api/generate', methods=['POST'])
def generate_graph():
    """Genera un nuevo grafo de horror y lo guarda en DB. Soporta Replay via seed."""
    global ultimo_grafo, ultimo_analisis
    
    # Check if seed provided in JSON body
    data = request.get_json(silent=True) or {}
    req_seed = data.get('seed')
    
    # 🔮 MODO INFLUENCE: El pasado persigue el futuro
    # Obtener último modo para influir en parámetros
    last_run = HorrorRun.query.order_by(HorrorRun.timestamp.desc()).first()
    
    ramificaciones = 7 # Default standard brutal
    cross_prob = 0.4
    
    if last_run:
        if last_run.modo == "MODO BESTIA":
             ramificaciones = 9 # Caos total
             print("🔥 Influencia BESTIA: Ramificaciones aumentadas a 9")
        elif last_run.modo == "MODO JUSTICE":
             ramificaciones = 6 
             # Bonus: Justicia optimiza, menos nodos basura, más conectados
             print("⚖️ Influencia JUSTICE: Ramificaciones optimizadas")
        elif last_run.modo == "DOLPHIN":
             ramificaciones = 3 # Calma total
             print("🐬 Influencia DOLPHIN: El abismo duerme (ramif=3)")

    if req_seed is not None:
        seed = int(req_seed)
        print(f"🔄 Replaying seed: {seed}")
    else:
        seed = random.randint(1, 999999)
    
    # Check if custom dimension provided
    custom_dim = data.get('custom_dim')
    
    force_d = session.pop('force_dolphin', False)
    
    ultimo_grafo = generar_grafo_9d(seed=seed, ramificaciones_por_nodo=ramificaciones, custom_dim=custom_dim)
    ultimo_analisis = analizar_horror(ultimo_grafo, top_n=10)
    
    # Check manual force or natural vote
    modo_nombre, modo_info = votar_modo(ultimo_analisis['horror_total'], special_trigger=force_d)
    
    # Guardar en DB
    try:
        new_run = HorrorRun(
            seed=seed,
            horror_total=ultimo_analisis['horror_total'],
            modo=modo_nombre,
            modo_desc=modo_info['desc'],
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
            'emoji': modo_info.get('emoji', ''),
            'desc': modo_info['desc']
        }
    })

@app.route('/api/visualize')
def visualize_graph():
    """Genera visualización HTML del grafo"""
    global ultimo_grafo, ultimo_analisis
    
    if ultimo_grafo is None:
        return jsonify({'error': 'No hay grafo generado'}), 400
    
    if ultimo_analisis is None:
        ultimo_analisis = analizar_horror(ultimo_grafo, top_n=10)
        
    # Check session forced dolphin (visualize does not consume it, only generate does usually, but lets check)
    force_d = session.get('force_dolphin', False) 
    
    modo_nombre, modo_info = votar_modo(ultimo_analisis['horror_total'], special_trigger=force_d)
    
    # Extract configs
    bg_color = "#000000"
    font_color = "#00ff41" # Default Matrix Green
    
    # Dynamic values from metadata
    physics = modo_info.get('physics', {})
    gravity = physics.get('gravity', -15000)
    spring_len = physics.get('spring_length', 120)
    spring_const = physics.get('spring_strength', 0.001)
    damping = physics.get('damping', 0.09)
    
    mod_color = modo_info.get('color', '#00ff41')
    shape = modo_info.get('node_shape', 'dot')
    edge_col = modo_info.get('edge_color', 'rgba(255, 0, 51, 0.4)')
    
    if modo_nombre == "MODO BESTIA":
        bg_color = "#1a0500" # Naranja muy oscuro
        font_color = "#ff4500"
    elif modo_nombre == "MODO JUSTICE":
        bg_color = "#1a1a00" # Dorado oscuro
        font_color = "#ffd700"
    elif modo_nombre == "CHILL":
        bg_color = "#000a1a"
        font_color = "#00aaff"
    elif modo_nombre == "DOLPHIN":
        bg_color = "#001a1a"
        font_color = "#00ffcc"
    elif modo_nombre == "MAPUCHE_COSMICO":
        bg_color = "#0a000a"
        font_color = "#aa00ff"
        
    # Crear red pyvis
    net = Network(
        height='100vh', 
        width='100%', 
        bgcolor=bg_color, 
        font_color=font_color, 
        directed=True
    )
    
    # Configuración física dinámica
    net.set_options(f"""
    {{
      "physics": {{
        "enabled": true,
        "barnesHut": {{
          "gravitationalConstant": {gravity},
          "centralGravity": 0.01,
          "springLength": {spring_len},
          "springConstant": {spring_const},
          "damping": {damping},
          "avoidOverlap": 0.1
        }},
        "minVelocity": 0.75
      }},
      "nodes": {{
        "shape": "{shape}",
        "font": {{
          "color": "{font_color}",
          "size": 16,
          "face": "monospace"
        }},
        "borderWidth": 2,
        "shadow": true
      }},
      "edges": {{
        "color": {{
          "color": "{edge_col}",
          "highlight": "#ffffff"
        }},
        "smooth": {{
            "type": "continuous"
        }},
        "arrows": {{
          "to": {{
            "enabled": true,
            "scaleFactor": 0.5
          }}
        }}
      }}
    }}
    """)
    
    # Calcular max horror para scaling
    all_horrors = [data.get('horror', 0) for _, data in ultimo_grafo.nodes(data=True)]
    max_h = max(all_horrors) if all_horrors else 1

    # Añadir nodos
    for node, data in ultimo_grafo.nodes(data=True):
        horror = data.get('horror', 0)
        
        # Scaling brutal
        intensity = int(255 * (horror / max_h))
        intensity = max(0, min(255, intensity))
        
        # Default dynamic color base (Red scale usually)
        # But if mode has specific primary color, we might want to scale that
        # For simplify: use red scale unless it's Dolphin/Chill
        
        color = f'#{intensity:02x}0000' # Default horror red
        
        if modo_nombre == "MODO BESTIA":
             color = f'#{intensity:02x}4500' # Orange scale
        elif modo_nombre == "MODO JUSTICE":
             color = f'#{intensity:02x}D700' # Gold scale
        elif modo_nombre == "DOLPHIN":
             color = f'#00{intensity:02x}cc' # Cyan scale
        elif modo_nombre == "CHILL":
             color = f'#00{intensity:02x}ff' # Blue scale
        
        # HYBRID OVERRIDE
        if 'HYBRID' in str(data.get('dim', '')):
             color = "#880088" # Purple fixed
             if modo_nombre == "MODO BESTIA": color = "#ff00ff"
        
        # 🔥 CERO ABSOLUTO OVERRIDE (SOL AMARILLO) 🔥
        if node == "CERO_ABSOLUTO" or node == "Cero Absoluto":
             color = "#FFD700"  # Gold/Sun Yellow
             size = 60 # Más grande que el resto
        else:
            size = 15 + (horror / max_h) * 60
        
        label = data.get('label', node)
        title = f"{label}<br>HORROR: {horror:.1f}<br>{data.get('desc', '')}"
        
        net.add_node(
            node,
            label=label,
            title=title,
            color=color,
            size=size,
            borderWidth=2
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
    
    # Check force dolphin
    force_d = session.pop('force_dolphin', False)
    
    results = []
    seeds = [] # Para almacenar todos los seeds
    top_nodes_all = [] # Para chequear keywords
    
    for _ in range(limit):
        current_seed = random.randint(1, 999999)
        # Dolphin influence should affect simulation parameters, but here use default for MC
        # To make it fair, maybe random params? Keep simple for now.
        g = generar_grafo_9d(seed=current_seed, ramificaciones_por_nodo=3)
        analytics = analizar_horror(g, top_n=5)
        
        horror = analytics['horror_total']
        results.append(horror)
        seeds.append(current_seed)
        top_nodes_all.append(analytics['nodos_mas_horribles'])
            
    # Identificar peor caso
    max_h = max(results)
    index_worst = results.index(max_h)
    best_worst_seed = seeds[index_worst]
    worst_nodes = top_nodes_all[index_worst]
    
    # Votar modo del peor caso
    modo_nombre, modo_info = votar_modo(max_h, special_trigger=force_d)
    
    # ⚔️ TEMPORAL TRIGGER JUSTICE ⚔️
    # Si detecta injusticia en los nodos más horribles, activa JUSTICE override
    keywords = ["desprecio", "ocultamiento", "iatrogenia", "psiquiátrico", "injusticia", "traición"]
    top_desc_str = " ".join([n['desc'].lower() for n in worst_nodes] + [n['label'].lower() for n in worst_nodes])
    
    if any(kw in top_desc_str for kw in keywords) and modo_nombre != "MODO BESTIA":
         modo_nombre = "MODO JUSTICE"
         modo_info = MODOS["MODO JUSTICE"]
         modo_info['desc'] += " [ACTIVADO POR DETECCIÓN DE INJUSTICIA]"

    # 💾 Persistir el PEOR caso
    try:
        new_run = HorrorRun(
            seed=best_worst_seed,
            horror_total=max_h,
            modo=modo_nombre,
            modo_desc=modo_info['desc'],
            top_nodes=json.dumps(worst_nodes),
            horror_promedio=max_h / 20, # Approx
            total_nodos=50 # dummy
        )
        db.session.add(new_run)
        db.session.commit()
    except Exception as e:
        print(f"Error DB persist MC: {e}")

    return jsonify({
        'simulations': limit,
        'max_horror': max_h,
        'min_horror': min(results),
        'avg_horror': sum(results) / len(results),
        'worst_seed': best_worst_seed,
        'histogram_data': results,
        'worst_mode': modo_nombre,
        'worst_mode_desc': modo_info['desc'],
        'worst_mode_emoji': modo_info.get('emoji', ''),
        'worst_mode_color': modo_info.get('color', '#00ff41'),
        'blink': modo_info.get('blink', False)
    })

@app.route('/visualize/seed/<int:seed>')
def visualize_seed_route(seed):
    """Visualiza directamente un seed específico sin pasar por generate"""
    grafo = generar_grafo_9d(seed=seed, ramificaciones_por_nodo=7)
    analisis = analizar_horror(grafo, top_n=10)
    modo_nombre, modo_info = votar_modo(analisis['horror_total'])
    
    # Dynamic values from metadata
    physics = modo_info.get('physics', {})
    gravity = physics.get('gravity', -15000)
    spring_len = physics.get('spring_length', 120)
    spring_const = physics.get('spring_strength', 0.001)
    damping = physics.get('damping', 0.09)
    
    mod_color = modo_info.get('color', '#00ff41')
    shape = modo_info.get('node_shape', 'dot')
    edge_col = modo_info.get('edge_color', 'rgba(255, 0, 51, 0.4)')
    
    bg_color = "#000000"
    font_color = "#00ff41"

    if modo_nombre == "MODO BESTIA":
        bg_color = "#1a0500" 
        font_color = "#ff4500"
    elif modo_nombre == "MODO JUSTICE":
        bg_color = "#1a1a00" 
        font_color = "#ffd700"
    elif modo_nombre == "CHILL":
        bg_color = "#000a1a"
        font_color = "#00aaff"
    elif modo_nombre == "DOLPHIN":
        bg_color = "#001a1a"
        font_color = "#00ffcc"
    elif modo_nombre == "MAPUCHE_COSMICO":
        bg_color = "#0a000a"
        font_color = "#aa00ff"

    # Crear red pyvis
    net = Network(
        height='100vh', 
        width='100%', 
        bgcolor=bg_color, 
        font_color=font_color,
        directed=True
    )
    
    # Configuración física dinámica
    net.set_options(f"""
    {{
      "physics": {{
        "enabled": true,
        "barnesHut": {{
          "gravitationalConstant": {gravity},
          "centralGravity": 0.01,
          "springLength": {spring_len},
          "springConstant": {spring_const},
          "damping": {damping},
          "avoidOverlap": 0.1
        }},
        "minVelocity": 0.75
      }},
      "nodes": {{
        "shape": "{shape}",
        "font": {{ "color": "{font_color}", "size": 16, "face": "monospace" }},
        "borderWidth": 2, "shadow": true
      }},
      "edges": {{
        "color": {{ "color": "{edge_col}", "highlight": "#ffffff" }},
        "smooth": {{ "type": "continuous" }},
        "arrows": {{ "to": {{ "enabled": true, "scaleFactor": 0.5 }} }}
      }}
    }}
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
        
        color = f'#{intensity:02x}0000' # Default horror red
        
        if modo_nombre == "MODO BESTIA":
             color = f'#{intensity:02x}4500' 
        elif modo_nombre == "MODO JUSTICE":
             color = f'#{intensity:02x}D700' 
        elif modo_nombre == "DOLPHIN":
             color = f'#00{intensity:02x}cc' 
        elif modo_nombre == "CHILL":
             color = f'#00{intensity:02x}ff' 

        # HYBRID OVERRIDE
        if 'HYBRID' in str(data.get('dim', '')):
             color = "#880088" 
             if modo_nombre == "MODO BESTIA": color = "#ff00ff"
        
        # 🔥 CERO ABSOLUTO OVERRIDE (SOL AMARILLO) 🔥
        if node == "CERO_ABSOLUTO" or node == "Cero Absoluto":
             color = "#FFD700"
             size = 60
        else:
            size = 15 + (horror / max_h) * 60
            
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
