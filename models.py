from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class HorrorRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seed = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    horror_total = db.Column(db.Float, nullable=False)
    modo = db.Column(db.String(50))
    top_nodes = db.Column(db.Text)          # JSON string con top 5 nodos
    graph_json = db.Column(db.Text)         # Opcional: export graph to json
    
    # Metadatos extra
    horror_promedio = db.Column(db.Float)
    total_nodos = db.Column(db.Integer)

    def __repr__(self):
        return f"<HorrorRun {self.seed} - {self.horror_total}>"

    def to_dict(self):
        return {
            'id': self.id,
            'seed': self.seed,
            'timestamp': self.timestamp.isoformat(),
            'horror_total': self.horror_total,
            'modo': self.modo,
            'top_nodes': json.loads(self.top_nodes) if self.top_nodes else [],
            'horror_promedio': self.horror_promedio,
            'total_nodos': self.total_nodos
        }
