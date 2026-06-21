from flask import Blueprint, jsonify, request
from . import db
from .models import Student
from .auth import token_required, role_required
from sqlalchemy import func
from datetime import datetime

bp = Blueprint('api', __name__, url_prefix='/api')

STATUTS_VALIDES = ['Actif', 'Suspendu', 'Diplômé', 'Abandonné']

def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None

@bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@bp.route('/students', methods=['GET'])
@token_required
@role_required('Admin', 'Professeur')
def list_students(current_user):
    students = Student.query.order_by(Student.created_at.desc()).all()
    return jsonify([s.to_dict(include_photo=False) for s in students]), 200

@bp.route('/students/<int:student_id>', methods=['GET'])
@token_required
def get_student(current_user, student_id):
    if current_user.role == 'Etudiant' and current_user.student_id != student_id:
        return jsonify({'error': 'Accès refusé'}), 403
    student = Student.query.get_or_404(student_id)
    return jsonify(student.to_dict()), 200

@bp.route('/students', methods=['POST'])
@token_required
@role_required('Admin')
def add_student(current_user):
    data = request.get_json()
    required = ['nom', 'prenom', 'email', 'filiere', 'niveau']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'Champ requis manquant: {field}'}), 400

    if Student.query.filter_by(email=data['email'].strip().lower()).first():
        return jsonify({'error': 'Email déjà utilisé'}), 409

    statut = data.get('statut', 'Actif')
    if statut not in STATUTS_VALIDES:
        statut = 'Actif'

    student = Student(
        nom=data['nom'].strip(), prenom=data['prenom'].strip(),
        email=data['email'].strip().lower(), filiere=data['filiere'].strip(),
        niveau=data['niveau'].strip(), statut=statut,
        date_naissance=parse_date(data.get('date_naissance')),
        telephone=data.get('telephone', '').strip() or None,
        adresse=data.get('adresse', '').strip() or None,
        contact_urgence_nom=data.get('contact_urgence_nom', '').strip() or None,
        contact_urgence_telephone=data.get('contact_urgence_telephone', '').strip() or None,
        photo=data.get('photo') or None
    )
    db.session.add(student)
    db.session.commit()

    annee = datetime.utcnow().year
    student.matricule = f"ETU-{annee}-{student.id:04d}"
    db.session.commit()

    return jsonify(student.to_dict()), 201

@bp.route('/students/<int:student_id>', methods=['PUT'])
@token_required
def update_student(current_user, student_id):
    student = Student.query.get_or_404(student_id)
    is_owner = current_user.role == 'Etudiant' and current_user.student_id == student_id

    if current_user.role not in ('Admin', 'Professeur') and not is_owner:
        return jsonify({'error': 'Accès refusé'}), 403

    data = request.get_json()

    if current_user.role in ('Admin', 'Professeur'):
        if 'email' in data and data['email'].strip():
            new_email = data['email'].strip().lower()
            if new_email != student.email and Student.query.filter_by(email=new_email).first():
                return jsonify({'error': 'Email déjà utilisé'}), 409
            student.email = new_email
        if 'nom' in data and data['nom'].strip(): student.nom = data['nom'].strip()
        if 'prenom' in data and data['prenom'].strip(): student.prenom = data['prenom'].strip()
        if 'filiere' in data and data['filiere'].strip(): student.filiere = data['filiere'].strip()
        if 'niveau' in data and data['niveau'].strip(): student.niveau = data['niveau'].strip()
        if 'statut' in data and data['statut'] in STATUTS_VALIDES: student.statut = data['statut']
        if 'date_naissance' in data: student.date_naissance = parse_date(data.get('date_naissance'))

    # Champs modifiables par l'étudiant lui-même
    if 'telephone' in data: student.telephone = data.get('telephone', '').strip() or None
    if 'adresse' in data: student.adresse = data.get('adresse', '').strip() or None
    if 'contact_urgence_nom' in data: student.contact_urgence_nom = data.get('contact_urgence_nom', '').strip() or None
    if 'contact_urgence_telephone' in data: student.contact_urgence_telephone = data.get('contact_urgence_telephone', '').strip() or None
    if 'photo' in data and data['photo']: student.photo = data['photo']

    db.session.commit()
    return jsonify(student.to_dict()), 200

@bp.route('/students/<int:student_id>', methods=['DELETE'])
@token_required
@role_required('Admin')
def delete_student(current_user, student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Étudiant supprimé avec succès'}), 200

@bp.route('/stats', methods=['GET'])
@token_required
@role_required('Admin', 'Professeur')
def stats(current_user):
    total = Student.query.count()
    par_filiere = db.session.query(Student.filiere, func.count(Student.id)).group_by(Student.filiere).all()
    par_niveau  = db.session.query(Student.niveau,  func.count(Student.id)).group_by(Student.niveau).all()
    par_statut  = db.session.query(Student.statut,  func.count(Student.id)).group_by(Student.statut).all()
    return jsonify({
        'total': total,
        'par_filiere': [{'filiere': f, 'count': c} for f, c in par_filiere],
        'par_niveau':  [{'niveau': n,  'count': c} for n, c in par_niveau],
        'par_statut':  [{'statut': s,  'count': c} for s, c in par_statut]
    }), 200
