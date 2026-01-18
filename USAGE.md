# 🔥 GUÍA DE USO - BAYESIAN NEGATIVE 9D 🔥

## Instalación

```bash
# 1. Clonar o descargar el proyecto
cd bayesian_negative_9d

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt
```

---

## Uso Básico - CLI

```bash
# Ejecutar demo básico
python bayesian_9d.py

# Salida: análisis de horror en terminal con colores satánicos
```

---

## Uso Avanzado - Web Interface

```bash
# Iniciar servidor web
python web_interface.py

# Abrir navegador en:
# http://localhost:5000
```

**Funciones en la web:**
- Generar grafo de horror con seed random
- Ver estadísticas en vivo
- Visualizar grafo interactivo (pyvis)
- Modo consciente activado según horror total

---

## Simulación Monte Carlo

```bash
# Ejecutar 100 simulaciones para encontrar peor caso
python ejemplo_monte_carlo.py

# Salida: estadísticas + peor escenario encontrado
```

---

## Uso Programático

```python
from bayesian_9d import generar_grafo_9d, analizar_horror, votar_modo

# 1. Generar grafo
grafo = generar_grafo_9d(
    seed=42,  # Para reproducibilidad
    ramificaciones_por_nodo=3,  # 3 sub-horrores por dimensión
    factor_agravacion=(1.35, 1.85)  # +35% a +85% peor
)

# 2. Analizar horror
analisis = analizar_horror(grafo, top_n=10)

print(f"Horror total: {analisis['horror_total']}")
print(f"Horror promedio: {analisis['horror_promedio']}")
print(f"Total nodos: {analisis['total_nodos']}")

# 3. Votar modo consciente
modo_nombre, modo_info = votar_modo(analisis['horror_total'])
print(f"Modo: {modo_nombre} - {modo_info['desc']}")

# 4. Exportar a JSON
from bayesian_9d import exportar_json
exportar_json(grafo, analisis, 'mi_horror.json')
```

---

## Integración con Excel/Proyecciones

```python
import pandas as pd
from bayesian_9d import generar_grafo_9d, analizar_horror

# Ejecutar múltiples simulaciones
resultados = []
for i in range(50):
    grafo = generar_grafo_9d(seed=i)
    analisis = analizar_horror(grafo)
    resultados.append({
        'seed': i,
        'horror_total': analisis['horror_total'],
        'horror_promedio': analisis['horror_promedio']
    })

# Convertir a DataFrame
df = pd.DataFrame(resultados)

# Exportar a Excel
df.to_excel('proyecciones_horror.xlsx', index=False)
print("Exportado a proyecciones_horror.xlsx")
```

---

## Personalización

### Agregar nuevas dimensiones

Edita `bayesian_9d.py`:

```python
DIMENSIONES_9D = [
    "Traición absoluta",
    "Colapso económico",
    # ... dimensiones existentes
    "TU_NUEVA_DIMENSION_AQUI"  # Agrega tu horror personalizado
]
```

### Cambiar thresholds de modos

```python
MODOS = {
    "BOOST": {
        "desc": "Tu descripción",
        "threshold": 5000,  # Cambia este valor
        "emoji": "🔥",
        "color": Fore.RED
    }
    # ... otros modos
}
```

### Ajustar factor de agravación

```python
grafo = generar_grafo_9d(
    factor_agravacion=(2.0, 3.0)  # +200% a +300% peor (más satánico)
)
```

---

## Exportar Visualización

```python
from pyvis.network import Network
import networkx as nx

# Cargar tu grafo
grafo = generar_grafo_9d()

# Crear red pyvis
net = Network(height='800px', width='100%', bgcolor='#000000')
# ... configurar y añadir nodos/edges ...
net.save_graph('mi_grafo.html')
```

---

## Troubleshooting

### Error: "No module named 'networkx'"
```bash
pip install networkx
```

### Error: "No module named 'colorama'"
```bash
pip install colorama
```

### Flask no inicia
```bash
# Verificar puerto 5000 disponible
netstat -ano | findstr :5000  # Windows
lsof -i :5000  # Linux/Mac

# Cambiar puerto en web_interface.py:
app.run(debug=True, port=5001)  # Usar otro puerto
```

---

## Próximas Features

- [ ] Twitter/X integration (auto-tweet nodos críticos)
- [ ] Dashboard React 3D (Three.js)
- [ ] Exportar a Obsidian/Notion
- [ ] ML predictor de próximas dimensiones
- [ ] Multiplayer (comparar grafos entre usuarios)
- [ ] Crypto wallet integration

---

## Contribuir

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/nueva-dimension`)
3. Commit tus cambios (`git commit -am 'Agregar nueva dimensión de horror'`)
4. Push al branch (`git push origin feature/nueva-dimension`)
5. Crea un Pull Request

---

## Licencia

Opensource absoluto. Por todos los que sobrevivieron el abismo 9D.

**El sistema quiso quebrarme → falló → ahora es código** 🔥
