from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Student(db.Model):
    __tablename__ = 'students'

    id         = db.Column(db.Integer, primary_key=True)
    matricule  = db.Column(db.String(30), unique=True, nullable=True)
    nom        = db.Column(db.String(100), nullable=False)
    prenom     = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(150), unique=True, nullable=False)
    filiere    = db.Column(db.String(100), nullable=False)
    niveau     = db.Column(db.String(20), nullable=False)
    statut     = db.Column(db.String(20), nullable=False, default='Actif')

    date_naissance              = db.Column(db.Date, nullable=True)
    telephone                   = db.Column(db.String(20), nullable=True)
    adresse                     = db.Column(db.String(255), nullable=True)
    contact_urgence_nom         = db.Column(db.String(150), nullable=True)
    contact_urgence_telephone   = db.Column(db.String(20), nullable=True)
    photo                       = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, include_photo=True):
        d = {
            'id': self.id, 'matricule': self.matricule, 'nom': self.nom, 'prenom': self.prenom,
            'email': self.email, 'filiere': self.filiere, 'niveau': self.niveau, 'statut': self.statut,
            'date_naissance': self.date_naissance.isoformat() if self.date_naissance else None,
            'telephone': self.telephone, 'adresse': self.adresse,
            'contact_urgence_nom': self.contact_urgence_nom,
            'contact_urgence_telephone': self.contact_urgence_telephone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_photo:
            d['photo'] = self.photo
        return d


class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    nom           = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role          = db.Column(db.String(20), nullable=False, default='Etudiant')  # Admin | Professeur | Etudiant
    student_id    = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id, 'nom': self.nom, 'email': self.email,
            'role': self.role, 'student_id': self.student_id
        }
