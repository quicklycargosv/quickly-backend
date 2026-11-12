from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Habilita la comunicación con tu frontend en Netlify

# Simulación de base de datos en memoria (o puedes adaptarla a tus necesidades)
proyectos_db = [
    {
        "referencia": "PAN-2026-001",
        "importador": "Comercializadora Ejemplo S.A. de C.V.",
        "estado": "REGISTRADO"
    },
    {
        "referencia": "PAN-2026-002",
        "importador": "Distribuidora Global S.A.",
        "estado": "CREADO"
    }
]

@app.route('/api/proyectos', methods=['POST'])
def crear_proyecto():
    try:
        referencia = request.form.get('referencia')
        importador = request.form.get('importador')
        
        # Aquí puedes capturar los archivos si deseas procesarlos con pdfplumber/pandas:
        # factura = request.files.get('factura')
        
        nuevo_proyecto = {
            "referencia": referencia,
            "importador": importador,
            "estado": "CREADO"
        }
        
        proyectos_db.append(nuevo_proyecto)
        return jsonify({"mensaje": "Proyecto creado con éxito", "proyecto": nuevo_proyecto}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/proyectos', methods=['GET'])
def listar_proyectos():
    return jsonify(proyectos_db), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
