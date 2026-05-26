import os
import time
import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "talleruser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "tallerpass")
DB_NAME = os.getenv("DB_NAME", "taller")


def get_connection():
    for i in range(10):
        try:
            return mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
        except mysql.connector.Error:
            time.sleep(3)

    raise Exception("No se ha podido conectar con la base de datos")


@app.route("/")
def home():
    return jsonify({"mensaje": "API del taller funcionant correctament"})


@app.route("/vehicles", methods=["GET"])
def get_vehicles():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT 
            v.idVehicle,
            v.matricula,
            v.model,
            v.any_vehicle,
            c.nom AS client
        FROM vehicles v
        INNER JOIN clients c ON v.idClient = c.idClient
    """

    cursor.execute(query)
    vehicles = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(vehicles)


@app.route("/appointments", methods=["GET"])
def get_appointments():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT 
            ci.idCita,
            DATE_FORMAT(ci.data_cita, '%Y-%m-%d') AS data_cita,
            ci.servei,
            ci.estat,
            cl.nom,
            cl.telefon,
            cl.correu,
            v.matricula,
            v.model,
            v.any_vehicle
        FROM cites ci
        INNER JOIN clients cl ON ci.idClient = cl.idClient
        INNER JOIN vehicles v ON ci.idVehicle = v.idVehicle
        ORDER BY ci.data_cita ASC
    """

    cursor.execute(query)
    appointments = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(appointments)


@app.route("/appointments", methods=["POST"])
def create_appointment():
    data = request.get_json()

    nom = data.get("nom")
    telefon = data.get("telefon")
    correu = data.get("correu")
    matricula = data.get("matricula")
    model = data.get("model")
    any_vehicle = data.get("any_vehicle")
    data_cita = data.get("data_cita")
    servei = data.get("servei")

    if not all([nom, telefon, correu, matricula, model, any_vehicle, data_cita, servei]):
        return jsonify({"error": "Falten dades al formulari"}), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO clients (nom, telefon, correu) VALUES (%s, %s, %s)",
        (nom, telefon, correu)
    )
    id_client = cursor.lastrowid

    cursor.execute(
        "INSERT INTO vehicles (matricula, model, any_vehicle, idClient) VALUES (%s, %s, %s, %s)",
        (matricula, model, any_vehicle, id_client)
    )
    id_vehicle = cursor.lastrowid

    cursor.execute(
        "INSERT INTO cites (data_cita, servei, estat, idClient, idVehicle) VALUES (%s, %s, %s, %s, %s)",
        (data_cita, servei, "pendent", id_client, id_vehicle)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"mensaje": "Cita creada correctament"}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)