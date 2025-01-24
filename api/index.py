from flask import Flask, jsonify,request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
]

@app.route('/api')
def home():
    return 'Hello, World!'

@app.route('/api/about')
def about():
    return 'About'

@app.route('/api/usuarios', methods=["GET"])
def get_users():
    return jsonify(users)

@app.route('/api/usuarios', methods=["POST"])
def add_user():
    new_user = request.get_json()
    users.append(new_user)
    return jsonify (new_user),201

