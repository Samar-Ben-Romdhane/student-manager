from flask import Blueprint, jsonify, request, current_app
from functools import wraps
import jwt
from datetime import datetime, timedelta
from . import db
from .models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def generate_token(user):
    payload = {
        'user_id': user.id,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(hours=8)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.split(' ')[1] if auth_header.startswith('Bearer ') else None
        if not token:
            return jsonify({'error': 'Token manquant'}), 401
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(payload['user_id'])
            if not current_user:
                raise ValueError('Utilisateur introuvable')
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Session expirée, reconnectez-vous'}), 401
        except Exception:
            return jsonify({'error': 'Token invalide'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if current_user.role not in roles:
                return jsonify({'error': 'Accès refusé pour votre rôle'}), 403
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    if not email or not password:
        return jsonify({'error': 'Email et mot de passe requis'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Identifiants invalides'}), 401

    token = generate_token(user)
    return jsonify({'access_token': token, 'user': user.to_dict()}), 200


@auth_bp.route('/me', methods=['GET'])
@token_required
def me(current_user):
    data = current_user.to_dict()
    if current_user.student_id:
        from .models import Student
        student = Student.query.get(current_user.student_id)
        if student:
            data['student'] = student.to_dict()
    return jsonify(data), 200


@auth_bp.route('/users', methods=['GET'])
@token_required
@role_required('Admin')
def list_users(current_user):
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([u.to_dict() for u in users]), 200


@auth_bp.route('/register', methods=['POST'])
@token_required
@role_required('Admin')
def register(current_user):
    data = request.get_json() or {}
    required = ['nom', 'email', 'password', 'role']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'Champ requis: {field}'}), 400

    if data['role'] not in ('Admin', 'Professeur', 'Etudiant'):
        return jsonify({'error': 'Rôle invalide'}), 400

    email = data['email'].strip().lower()
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email déjà utilisé'}), 409

    user = User(
        nom=data['nom'].strip(),
        email=email,
        role=data['role'],
        student_id=data.get('student_id') or None
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201
