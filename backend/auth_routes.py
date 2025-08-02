from flask import Blueprint, request, jsonify
from backend.models import db, User
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

# ============================================================
# User Registration Route
# ============================================================

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    """
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON"}), 400

    username = data.get('username')
    password = data.get('password')
    full_name = data.get('full_name')
    qualification = data.get('qualification')
    dob = data.get('dob')

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 409

    user = User(
        username=username,
        full_name=full_name,
        qualification=qualification,
        is_admin=False
    )

    if dob:
        try:
            user.dob = datetime.strptime(dob, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"msg": "Invalid DOB format. Use YYYY-MM-DD."}), 400

    user.password = password
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


# ============================================================
# User Login Route
# ============================================================

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Log in a user or admin.
    """
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return jsonify({"msg": "Invalid username or password"}), 401

    additional_claims = {
        "is_admin": user.is_admin,
        "user_id": user.id
    }
    access_token = create_access_token(identity=user.username, additional_claims=additional_claims)

    return jsonify(access_token=access_token, is_admin=bool(user.is_admin)), 200



