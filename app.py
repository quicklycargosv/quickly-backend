import os
import pandas as pd
import pdfplumber
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/procesar', methods=['POST'])
def procesar_documento():
    if 'factura' not in files:
        return jsonify({"error": "No se encontró el archivo de factura"}), 400
    
    # Aquí procesaremos el PDF, aplicaremos el prorrateo de peso y generaremos el Excel
    # ...
    return jsonify({"mensaje": "Procesamiento exitoso"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
