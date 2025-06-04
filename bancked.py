from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simula la "base de datos" en memoria
inventario = []

@app.route('/inventario', methods=['GET'])
def obtener_inventario():
    return jsonify(inventario)

@app.route('/inventario', methods=['POST'])
def agregar_medicamento():
    data = request.get_json()
    # Verifica si ya existe el medicamento para ese residente
    for item in inventario:
        if item["residente"] == data["residente"] and item["medicamento"] == data["medicamento"]:
            item["cantidad"] += int(data["cantidad"])
            item["minimo"] = int(data["minimo"])
            return jsonify({"msg": "Actualizado", "item": item})
    # Si no existe, lo agrega nuevo
    data["cantidad"] = int(data["cantidad"])
    data["minimo"] = int(data["minimo"])
    inventario.append(data)
    return jsonify({"msg": "Agregado", "item": data})

@app.route('/inventario/consumo', methods=['POST'])
def registrar_consumo():
    data = request.get_json()
    for item in inventario:
        if item["residente"] == data["residente"] and item["medicamento"] == data["medicamento"]:
            item["cantidad"] = max(0, item["cantidad"] - int(data["consumo"]))
            return jsonify({"msg": "Consumo registrado", "item": item})
    return jsonify({"msg": "Medicamento no encontrado"}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
