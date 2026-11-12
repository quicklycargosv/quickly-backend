import os
import io
import pandas as pd
import pdfplumber
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "online", "mensaje": "Backend de Quickly operando correctamente"})

@app.route('/procesar', methods=['POST'])
def procesar_documento():
    if 'factura' not in request.files:
        return jsonify({"error": "No se encontró el archivo de factura en la petición"}), 400
    
    file = request.files['factura']
    
    try:
        # Extraer texto y tablas usando pdfplumber
        datos_extraidos = []
        with pdfplumber.open(file) as pdf:
            for pagina in pdf.pages:
                tables = pagina.extract_tables()
                for table in tables:
                    for row in table:
                        datos_extraidos.append(row)
        
        # Si no encontró tablas estructuradas, creamos un reporte básico de contingencia
        if not datos_extraidos:
            datos_extraidos = [["Descripcion", "Cantidad", "Valor"], ["Factura procesada sin tablas directas", 1, 0.0]]

        df = pd.DataFrame(datos_extraidos)
        
        # Generar archivo Excel en memoria
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Aduana_Quickly')
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='reporte_aduanas_quickly.xlsx'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
