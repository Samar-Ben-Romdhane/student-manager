from flask import Blueprint, jsonify, request
from . import db
from .models import Student
from sqlalchemy import func

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@bp.route('/students', methods=['GET'])
def list_students():
    students = Student.query.order_by(Student.created_at.desc()).all()
    return jsonify([s.to_dict() for s in students]), 200

@bp.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    for field in ['nom', 'prenom', 'email', 'filiere', 'niveau']:
        if not data.get(field):
            return jsonify({'error': f'Champ requis: {field}'}), 400
    if Student.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email déjà utilisé'}), 409
    student = Student(nom=data['nom'], prenom=data['prenom'],
                      email=data['email'].lower(), filiere=data['filiere'],
                      niveau=data['niveau'])
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201

@bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Étudiant supprimé'}), 200

@bp.route('/stats', methods=['GET'])
def stats():
    total = Student.query.count()
    par_filiere = db.session.query(Student.filiere, func.count(Student.id)).group_by(Student.filiere).all()
    par_niveau  = db.session.query(Student.niveau,  func.count(Student.id)).group_by(Student.niveau).all()
    return jsonify({
        'total': total,
        'par_filiere': [{'filiere': f, 'count': c} for f, c in par_filiere],
        'par_niveau':  [{'niveau': n,  'count': c} for n, c in par_niveau]
    }), 200
