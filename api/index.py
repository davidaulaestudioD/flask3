from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MONGO_URI = "mongodb+srv://davidad:a4B36EDB@clase.6z984.mongodb.net/?retryWrites=true&w=majority&appName=CLASE"
client = MongoClient(MONGO_URI)
db = client["expressback"] 
users_collection = db["listas"] 


@app.route('/api')
def home():
    return 'Hello, World!'

@app.route('/api/about')
def about():
    return 'About'

#Parte MONGODB
@app.route('/api/users/mongo', methods=["GET"])
def ver_users_mongo():
    users = list(users_collection.find({}, {"_id": 0, "id": 1, "nombre": 1, "telefono": 1}))

    return jsonify(users)

@app.route('/api/users/mongo/primero', methods=["GET"])
def ver_primer_user_mongo():
    user = users_collection.find_one({}, {"_id": 0, "id": 1, "nombre": 1, "telefono": 1})
    
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "No se encontraron usuarios"}), 404


@app.route('/api/users/mongo/add', methods=["POST"])
def agregar_usuario_mongo():
    data = request.json  
    
    if not all(key in data for key in ["id", "nombre","apellido", "telefono"]):
        return jsonify({"error": "Faltan datos. Se requiere id, nombre, apellido y telefono"}), 400
    
    result = users_collection.insert_one({
        "id": data["id"],
        "nombre": data["nombre"],
        "apellido": data["apellido"],
        "telefono": data["telefono"]
    })

    return jsonify({"message": "Usuario agregado correctamente", "inserted_id": str(result.inserted_id)}), 201


@app.route('/api/users/mongo/<int:user_id>', methods=["GET"])
def buscar_usuario_por_id(user_id):
    user = users_collection.find_one({"id": user_id}, {"_id": 0, "id": 1, "nombre": 1, "apellido": 1, "telefono": 1})
    
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404




"""
#Parte LOCAL

#Listar todos los usuarios
@app.route('/api/users', methods=["GET"])
def ver_users():
    return jsonify(users)

#Añadir usuario
@app.route('/api/users', methods=["POST"])
def añadir_user():
    new_user = request.get_json()
    users.append(new_user)
    return jsonify(new_user), 201

#Listar el primer usuario
@app.route('/api/users/user1')
def primer_user():
    return jsonify(users[0])

#Listar un ID
@app.route('/api/users/<int:id>', methods=["GET"])
def buscar_user(id):
    # Buscar el usuario por id
    user = next((u for u in users if u["id"] == id), None)
    return jsonify(user)

"""

handle=app