#!/usr/bin/env python3
"""
🔥 WEB INTERFACE - BAYESIAN NEGATIVE 9D 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Servidor Flask con estética terminal dark satánica.
Visualización interactiva del grafo de horror.
"""

from flask import Flask, render_template, jsonify, send_from_directory
from bayesian_9d import generar_grafo_9d, analizar_horror, votar_modo
import random
import networkx as nx
from pyvis.network import Network
import os

app = Flask(__name__)

# Almacenar último grafo generado
ultimo_grafo = None
ultimo_analisis = None

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_graph():
    """Genera un nuevo grafo de horror"""
    global ultimo_grafo, ultimo_analisis
    
    seed = random.randint(1, 999999)
    ultimo_grafo = generar_grafo_9d(seed=seed, ramificaciones_por_nodo=3)
    ultimo_analisis = analizar_horror(ultimo_grafo, top_n=10)
    modo_nombre, modo_info = votar_modo(ultimo_analisis['horror_total'])
    
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
    
    # Configuración física del grafo
    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -8000,
          "centralGravity": 0.3,
          "springLength": 95,
          "springConstant": 0.04
        }
      },
      "nodes": {
        "font": {
          "color": "#00ff41",
          "size": 14
        },
        "borderWidth": 2
      },
      "edges": {
        "color": {
          "color": "#ff0033",
          "highlight": "#ffff00"
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
    
    # Añadir nodos con colores basados en horror
    for node, data in ultimo_grafo.nodes(data=True):
        horror = data.get('horror', 0)
        
        # Color según nivel de horror
        if horror > 1200:
            color = '#ff0033'  # Rojo oscuro
            size = 30
        elif horror > 800:
            color = '#ff6600'  # Naranja
            size = 20
        else:
            color = '#ffff00'  # Amarillo
            size = 15
        
        label = data.get('label', node)
        title = f"{label}<br>Horror: {horror:.1f}<br>{data.get('desc', '')}"
        
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
        net.add_edge(u, v, label=label, width=weight, title=f"Factor: {weight:.2f}")
    
    # Guardar HTML
    output_file = os.path.join('static', 'graph.html')
    net.save_graph(output_file)
    
    return jsonify({'status': 'ok', 'file': 'graph.html'})

@app.route('/graph')
def show_graph():
    """Muestra el grafo generado"""
    return send_from_directory('static', 'graph.html')

if __name__ == '__main__':
    # Crear directorio static si no existe
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    print("🔥 Iniciando servidor Bayesian Negative 9D...")
    print("📡 Abre http://localhost:5000 en tu navegador")
    print("💀 Ctrl+C para salir\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
