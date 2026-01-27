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

from flask import Flask, render_template, jsonify, send_from_directory, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hmac
import json
import os
import glob
import random
import time

# Importar desde core_engine modularizado
from src.core.core_engine import (
    generar_grafo_9d, analizar_horror, print_banner,
    DIMENSIONES_9D, MODOS, normalize_to_9d, optimizacion_recursiva_agi # PR-10
)
from src.llm.llm_narrator import narrator
from src.connectors.data_connectors import ingestion_manager
from src.quantum.connectors import QuantumNexus
from src.quantum.kernel import QuantumKernel
from src.core.multiverse import MultiverseEngine
from src.core.orchestrator import orchestrator # PR-76

app = Flask(__name__, 
            template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../templates')),
            static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../static')))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///horror_runs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CLEANUP_TOKEN'] = os.environ.get('CLEANUP_TOKEN')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(32))
db = SQLAlchemy(app)

# PR-15: Quantum Integration
q_nexus = QuantumNexus()
q_kernel = QuantumKernel(nexus=q_nexus)
mv_engine = MultiverseEngine() # PR-17: Timeline Branching

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
        
        # PR-15: Quantum Entropy Seed
        if random.random() < 0.1: # 10% chance to use real quantum seed
            seed = q_kernel.generate_quantum_seed(seed)
            print(f"(Quantum Seed: {seed}) ", end='')

        G = generar_grafo_9d(seed=seed, max_nodes=12000, ramificaciones_por_nodo=8)
        
        # PR-10: Recursive Improvement
        if seed % 3 == 0: # Simbolically trigger every few seeds
            G = optimizacion_recursiva_agi(G, iterations=2)
            
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

@app.route('/api/ingest_real')
def api_ingest_real():
    """Generates a universe using the BayesianOrchestrator (Resonance Cycle)."""
    seed = int(time.time())
    freq = float(request.args.get('freq', 440.0)) # PR-79
    
    # Run the full resonance cycle (Bio + Memory + Quantum + Ethics)
    result = orchestrator.run_resonance_cycle(seed, cosmic_freq=freq)
    
    if result.get("status") == "QUARANTINED":
        return jsonify(result), 403

    G = result["graph"]
    analisis = result["analysis"]
    
    # PR-17: Timeline Branching
    chps = mv_engine.detect_chp(G, threshold=80000.0)
    branches = []
    for node in chps[:3]: # Limit to 3 branches max
        branch_seed = mv_engine.spawn_parallel_timeline(seed, node)
        branches.append({"at_node": node, "new_seed": branch_seed})

    filename = f"web/data_seed_{seed}.json"
    export_to_threejs(G, analisis, filename)
    save_run_to_db(seed, analisis)
    
    return jsonify({
        "status": "success",
        "seed": seed,
        "horror_total": analisis['horror_total'],
        "branches_detected": branches,
        "resonance_data": {
            "bio_entropy": result["biological_context"]["global_bio_entropy"],
            "ethical_risk": result["ethical_risk"]["risk_level"]
        }
    })

@app.route('/api/upload_data', methods=['POST'])
def api_upload_data():
    """Endpoint for manual JSON/CSV ingestion."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        data = json.load(file)
        # For simplicity, we assume the JSON has { "initial_weights": { "1": 2.0, ... } }
        weights = {int(k): float(v) for k, v in data.get("initial_weights", {}).items()}
        seed = int(time.time())
        
        G = generar_grafo_9d(seed=seed, initial_horror_weights=weights)
        analisis = analizar_horror(G)
        
        filename = f"web/data_seed_{seed}.json"
        export_to_threejs(G, analisis, filename)
        save_run_to_db(seed, analisis)
        
        return jsonify({"success": True, "seed": seed})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

@app.route('/api/multiverse/branches')
def api_multiverse_branches():
    """Returns branches for a given seed."""
    seed = request.args.get('seed', type=int)
    if not seed or seed not in mv_engine.timelines:
        return jsonify({"branches": []})
    return jsonify(mv_engine.timelines[seed])

@app.route('/api/narrative_stream')
def narrative_stream():
    """SSE endpoint for LLM narrative"""
    seed = request.args.get('seed', -10, type=int)
    horror = request.args.get('horror', 0, type=float)
    nodes = request.args.get('nodes', 0, type=int)
    mode = request.args.get('mode', 'UNKNOWN')
    persona = request.args.get('persona', 'AUTO') # PR-79

    def generate():
        for chunk in narrator.generate_narrative({
            'seed': seed,
            'horror_total': horror,
            'total_nodos': nodes,
            'modo': mode,
            'force_persona': persona if persona != 'AUTO' else None
        }):
            yield f"data: {json.dumps({'text': chunk})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

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
# 🤖 PHASE 20: AI CHAT ENDPOINT (Multi-Provider + Tools)
# ═══════════════════════════════════════════════════════════════

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """AI Chat endpoint with context, RAG, Quantum, MCP, and LangChain support."""
    data = request.get_json()
    
    message = data.get('message', '')
    provider = data.get('provider', 'deepseek')
    api_key = data.get('apiKey') # Frontend sends apiKey
    tools = data.get('tools', {})
    context = data.get('context', {})
    history = data.get('history', [])
    attachments = data.get('attachments', [])
    
    tools_used = []
    augmented_context = ""
    
    try:
        # 1. RAG/Memory retrieval
        if tools.get('rag'):
            tools_used.append('RAG')
            from src.llm.rag_engine import biological_rag
            rag_context = biological_rag.retrieve_context(context.get('horror', 0))
            augmented_context += f"\n[RAG CONTEXT]: {rag_context[:500]}"
        
        # 2. Quantum state query
        if tools.get('quantum'):
            tools_used.append('QUANTUM')
            quantum_state = q_kernel.get_quantum_context(context.get('seed', -10))
            augmented_context += f"\n[QUANTUM STATE]: Entanglement={quantum_state.get('entanglement', 0):.3f}, Decoherence={quantum_state.get('decoherence', 0):.3f}"
        
        # 3. Database query
        if tools.get('db'):
            tools_used.append('DATABASE')
            # Query recent runs
            recent_runs = HorrorRun.query.order_by(HorrorRun.timestamp.desc()).limit(3).all()
            db_context = ", ".join([f"Seed {r.seed}: Horror {r.horror_total:.0f}" for r in recent_runs])
            augmented_context += f"\n[DB CONTEXT]: {db_context}"
        
        # 4. MCP Agent (simulation for now)
        if tools.get('mcp'):
            tools_used.append('MCP')
            augmented_context += f"\n[MCP AGENT]: Mode=AUTO, Context awareness active"
        
        # 5. Attachment context
        if attachments:
            tools_used.append('VISION')
            for att in attachments:
                att_type = att.get('type', 'unknown').upper()
                augmented_context += f"\n[ATTACHMENT]: {att_type} at Seed={att.get('context', {}).get('seed', '?')}, Horror={att.get('context', {}).get('horror', '?')}"
        
        # Build system prompt
        system_prompt = f"""You are COSMIC AI, an assistant integrated into a 11D Bayesian horror simulation.
Current Universe Context:
- Seed: {context.get('seed', -10)}
- Horror Level: {context.get('horror', 0)}
- Nodes: {context.get('nodes', 0)}
- Mode: {context.get('mode', 'UNKNOWN')}
- Bio State: {context.get('bio_state', 'UNKNOWN')}

{augmented_context}

You have access to: {', '.join(tools_used) if tools_used else 'Basic LLM only'}

Respond in Spanish. Be concise but helpful. If the user provided a screenshot, describe what you understand about the visualization state."""
        
        # Build conversation
        messages = []
        for h in history[-5:]:
            messages.append({"role": h['role'], "content": h['content']})
        messages.append({"role": "user", "content": message})
        
        # Generate response via narrator's provider
        response_text = ""
        for chunk in narrator.generate_narrative({
            'seed': context.get('seed', -10),
            'horror_total': context.get('horror', 0),
            'chat_mode': True,
            'chat_message': message,
            'chat_system': system_prompt,
            'force_persona': None,  # Use raw LLM
            'api_key': api_key
        }):
            response_text += chunk
        
        return jsonify({
            "response": response_text or "Respuesta generada basada en el contexto cósmico.",
            "tools_used": tools_used,
            "provider": provider
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "response": f"Error procesando la consulta: {str(e)}. Los servicios de IA pueden requerir configuración adicional.",
            "tools_used": tools_used
        }), 200  # Return 200 so frontend can display the error gracefully

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
