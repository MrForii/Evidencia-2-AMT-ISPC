from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configura tu conexión a la base de datos
db_config = {
    "host": "b4fewpnrw63fxilykl7z-mysql.services.clever-cloud.com",
    "user": "uk0za9yhjsjmmpuy",
    "password": "eARyZjZuCQETChusm6wW",
    "database": "b4fewpnrw63fxilykl7z",
    "port": 3306
}


@app.route("/data", methods=["POST"])
def insert_data():
    if request.is_json:
        data = request.get_json()
        data_to_send = data.get("value")

        if data_to_send is None:
            return jsonify({"status": "error", "message": "data is required"}), 400

        # Aquí va tu lógica para insertar en la base de datos
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sensor_data (value) VALUES (%s)", (data_to_send,)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"status": "success"}), 201
        except mysql.connector.Error as err:
            return jsonify({"status": "error", "message": str(err)}), 500
    else:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

@app.route("/data", methods=["GET"])
def get_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Para obtener resultados como diccionarios
        cursor.execute("SELECT * FROM sensor_data")  # Consulta para obtener todos los datos
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        print(results)
        return jsonify(results), 200  # Devuelve los resultados como JSON
        
    except mysql.connector.Error as err:
        return jsonify({"status": "error", "message": str(err)}), 500

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))