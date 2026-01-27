#!/usr/bin/env python3
"""
🔥 BAYESIAN NEGATIVE 9D v6.0 - FLASK APP COMPLETO 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Servidor Flask completo con:
- Generación de grafos 9D
- Export a JSON para Three.js
- Base de datos SQLite (Hall of Shame)
- Rutas para visualización web
"""

from flask import Flask, render_template, jsonify, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hmac
import json
import os
import glob
import random

# Importar desde core_engine consolidado
from core_engine import (
    generar_grafo_9d, analizar_horror, print_banner,
    DIMENSIONES_9D, MODOS
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///horror_runs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CLEANUP_TOKEN'] = os.environ.get('CLEANUP_TOKEN')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(32))
db = SQLAlchemy(app)

# ═══════════════════════════════════════════════════════════════
# 💾 MODELO DE BASE DE DATOS
# ═══════════════════════════════════════════════════════════════

class HorrorRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seed = db.Column(db.Integer, nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    horror_total = db.Column(db.Float, nullable=False)
    modo = db.Column(db.String(50))
    modo_desc = db.Column(db.Text)
    top_nodes = db.Column(db.Text)  # JSON string
    horror_promedio = db.Column(db.Float)
    total_nodos = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'seed': self.seed,
            'timestamp': self.timestamp.isoformat(),
            'horror_total': self.horror_total,
            'modo': f"{self.modo} {self.modo_desc or ''}",
            'top_nodes': json.loads(self.top_nodes) if self.top_nodes else [],
            'horror_promedio': self.horror_promedio,
            'total_nodos': self.total_nodos
        }

with app.app_context():
    db.create_all()

# ═══════════════════════════════════════════════════════════════
# 🔧 FUNCIONES AUXILIARES
# ═══════════════════════════════════════════════════════════════

def save_run_to_db(seed, analisis):
    """Guarda un run en la base de datos"""
    if HorrorRun.query.filter_by(seed=seed).first():
        return
    
    top_nodes_json = json.dumps([
        {"label": n['label'], "horror": n['horror'], "desc": n.get('desc','')[:100]}
        for n in analisis['nodos_mas_horribles'][:10]
    ])
    
    run = HorrorRun(
        seed=seed,
        horror_total=analisis['horror_total'],
        modo=analisis['modo'],
        modo_desc=analisis['modo_info']['desc'],
        top_nodes=top_nodes_json,
        horror_promedio=analisis['horror_promedio'],
        total_nodos=analisis['total_nodos']
    )
    db.session.add(run)
    db.session.commit()

def export_to_threejs(G, analisis, filepath="web/data.json"):
    """Exporta grafo a formato JSON para Three.js"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    nodes = []
    for node_id, data in G.nodes(data=True):
        nodes.append({
            "id": node_id,
            "label": data.get('label', node_id),
            "horror": data.get('horror', 0),
            "dim": data.get('dim', 0),
            "desc": data.get('desc', ''),
            "position": [
                random.uniform(-1000, 1000),
                random.uniform(-500, 500),
                random.uniform(-1000, 1000)
            ]
        })
    
    edges = []
    for u, v, data in G.edges(data=True):
        edges.append({
            "source": u,
            "target": v,
            "weight": data.get('weight', 1.0),
            "label": data.get('label', '')
        })
    
    output = {
        "nodes": nodes,
        "edges": edges,
        "modo": analisis['modo'],
        "horror_total": analisis['horror_total'],
        "timestamp": analisis['timestamp']
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

def save_replay_seed(G, analisis, seed, replay_path="replays/"):
    """Guarda replay para reproducción futura"""
    os.makedirs(replay_path, exist_ok=True)
    filepath = os.path.join(replay_path, f"horror_graph_{seed}.json")
    export_to_threejs(G, analisis, filepath)

# ═══════════════════════════════════════════════════════════════
# 🎮 GENERACIÓN BATCH
# ═══════════════════════════════════════════════════════════════

def main(batch_size: int = 200, start_seed: int = -10):
    """Genera batch de universos y guarda en DB"""
    print_banner()
    print(f"\n🌌 Generando {batch_size} universos desde seed {start_seed}...\n")
    
    for i in range(batch_size):
        seed = start_seed + i
        print(f"[{i+1}/{batch_size}] Seed {seed}... ", end='', flush=True)
        
        G = generar_grafo_9d(seed=seed, max_nodes=12000, ramificaciones_por_nodo=8)
        analisis = analizar_horror(G)
        
        print(f"Horror: {analisis['horror_total']:,.0f} | {analisis['modo_info']['emoji']} {analisis['modo']}")
        
        save_replay_seed(G, analisis, seed)
        export_to_threejs(G, analisis, f"web/data_seed_{seed}.json")
        save_run_to_db(seed, analisis)
    
    print(f"\n✅ Batch completo! {batch_size} universos generados 🚀\n")

# ═══════════════════════════════════════════════════════════════
# 🌐 RUTAS FLASK
# ═══════════════════════════════════════════════════════════════

@app.after_request
def set_security_headers(response):
    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; "
        "script-src 'self' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net 'unsafe-inline'; "
        "style-src 'self' https://fonts.googleapis.com 'unsafe-inline'; "
        "font-src https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "base-uri 'self'; "
        "frame-ancestors 'self'"
    )
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("Permissions-Policy", "camera=(), geolocation=(), microphone=(self)")
    return response

@app.route('/')
def index():
    """Página principal con visualizador 3D"""
    return render_template('index.html')

@app.route('/visualize')
def visualize():
    """Visualizador con seed específico"""
    seed = request.args.get('seed', -10)
    return render_template('index.html', initial_seed=seed)

@app.route('/brain_3d')
def brain_3d():
    """Visualización cerebro bicameral"""
    return render_template('brain_3d.html')

@app.route('/random_seed')
def random_seed():
    """Retorna un seed aleatorio disponible"""
    json_files = glob.glob("web/data_seed_*.json")
    if not json_files:
        return jsonify({"error": "No hay universos generados"}), 404
    
    chosen = random.choice(json_files)
    seed = int(chosen.split("_")[-1].replace(".json", ""))
    return jsonify({
        "file": chosen,
        "seed": seed,
        "url": f"/web/data_seed_{seed}.json"
    })

@app.route('/hall_of_shame')
def hall_of_shame():
    """Hall of Shame - Top 50 peores runs"""
    runs = HorrorRun.query.order_by(HorrorRun.horror_total.desc()).limit(50).all()
    return render_template('hall.html', runs=[r.to_dict() for r in runs])

@app.route('/web/<path:filename>')
def serve_web(filename):
    """Sirve archivos JSON de universos"""
    return send_from_directory('web', filename)

@app.route('/api/stats')
def api_stats():
    """API: Estadísticas generales"""
    total_runs = HorrorRun.query.count()
    worst_run = HorrorRun.query.order_by(HorrorRun.horror_total.desc()).first()
    best_run = HorrorRun.query.order_by(HorrorRun.horror_total.asc()).first()
    
    return jsonify({
        "total_universes": total_runs,
        "worst_horror": worst_run.horror_total if worst_run else 0,
        "worst_seed": worst_run.seed if worst_run else None,
        "best_horror": best_run.horror_total if best_run else 0,
        "best_seed": best_run.seed if best_run else None
    })

@app.route('/api/cleanup', methods=['POST'])
def api_cleanup():
    """API: Limpiar todos los datos generados"""
    import shutil
    
    try:
        cleanup_token = app.config.get('CLEANUP_TOKEN')
        provided_token = request.headers.get('X-Cleanup-Token', '')
        if not cleanup_token:
            return jsonify({
                "status": "error",
                "message": "Cleanup token no configurado. Define CLEANUP_TOKEN en el entorno."
            }), 403
        if not hmac.compare_digest(provided_token, cleanup_token):
            return jsonify({
                "status": "error",
                "message": "Token inválido para cleanup."
            }), 403

        # Borrar base de datos
        HorrorRun.query.delete()
        db.session.commit()
        
        # Borrar archivos JSON
        if os.path.exists('web'):
            shutil.rmtree('web')
        os.makedirs('web', exist_ok=True)
        
        # Borrar replays
        if os.path.exists('replays'):
            shutil.rmtree('replays')
        os.makedirs('replays', exist_ok=True)
        
        return jsonify({
            "status": "success",
            "message": "Todos los datos han sido eliminados"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ═══════════════════════════════════════════════════════════════
# 🚀 MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        # Modo generación: python app.py generate
        batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 200
        start_seed = int(sys.argv[3]) if len(sys.argv) > 3 else -10
        main(batch_size, start_seed)
    else:
        # Modo servidor
        print("\n🌌 COSMIC OS v3.3 - Servidor iniciado")
        print("📍 http://localhost:5000")
        print("🏆 Hall of Shame: http://localhost:5000/hall_of_shame")
        print("\n💡 Para generar batch: python app.py generate [cantidad] [seed_inicial]\n")
        app.run(debug=False, host='0.0.0.0', port=5000)
