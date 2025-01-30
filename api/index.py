from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from flask_cors import CORS

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configurar CORS
CORS(app, resources={r"/api/*": {"origins": "https://vercel-flask-front.vercel.app"}})  # Permitir solo tu dominio frontend

# Cargar las variables del archivo .env
#dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
#load_dotenv(dotenv_path)
load_dotenv()
# Obtener la URI de MongoDB desde las variables de entorno
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI no está definida en el archivo .env")

# Verificar la conexión con pymongo
try:
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')  # Esto verifica la conexión
    print("Conexión a MongoDB exitosa con pymongo")
except Exception as e:
    print(f"Error de conexión a MongoDB: {e}")

# Configurar la URI de MongoDB
app.config["MONGO_URI"] = MONGO_URI

# Inicializar PyMongo
mongo = PyMongo(app)

db = mongo.cx["vercel"]  # Conectar explícitamente a la base de datos "vercel"
usuarios_collection = db["usuarios"] 

# Ruta de prueba
@app.route('/api')
def home():
    return 'Hello, World!'

@app.route('/api/about')
def about():
    return 'About'

# Obtener todos los usuarios
@app.route('/api/usuarios', methods=["GET"])
def get_users():
    users = usuarios_collection.find()  # Usar la colección "usuarios"
    user_list = []
    for user in users:
        user["_id"] = str(user["_id"]) 
        user_list.append(user)
    return jsonify(user_list)

# Crear un nuevo usuario
@app.route('/api/crearusuario', methods=["POST"])
def add_user():
    new_user = request.get_json()  # Obtener los datos del cuerpo de la solicitud
    user_id = usuarios_collection.insert_one(new_user).inserted_id  # Insertar el nuevo usuario
    new_user["_id"] = str(user_id)  # Convertir el ObjectId a string
    return jsonify(new_user), 201  # Retornar el usuario con su nuevo ID

# Obtener un usuario por su ID
@app.route('/api/usuarios/<string:user_id>', methods=["GET"])
def get_user_by_id(user_id):
    user = usuarios_collection.find_one({"_id": ObjectId(user_id)})  # Usar la colección "usuarios"
    if user:
        user["_id"] = str(user["_id"])  # Convertir ObjectId a string
        return jsonify(user)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
