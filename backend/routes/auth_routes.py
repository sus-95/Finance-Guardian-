from flask import Blueprint, request, jsonify
from backend.models.user_model import create_user, find_user_by_email
from backend.utils.password_hash import hash_password, verify_password
from backend.utils.jwt_handler import generate_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if find_user_by_email(email):
        return jsonify({"error": "User already exists"}), 409

    hashed_password = hash_password(password)

    user_data = {
        "name": name,
        "email": email,
        "password": hashed_password
    }

    create_user(user_data)

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = find_user_by_email(email)

    if not user or not verify_password(user["password"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = generate_token(user["_id"])

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }
    }), 200
