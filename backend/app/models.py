from . import db
from datetime import datetime

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

    # Profil complet
    date_naissance              = db.Column(db.Date, nullable=True)
    telephone                   = db.Column(db.String(20), nullable=True)
    adresse                     = db.Column(db.String(255), nullable=True)
    contact_urgence_nom         = db.Column(db.String(150), nullable=True)
    contact_urgence_telephone   = db.Column(db.String(20), nullable=True)
    photo                       = db.Column(db.Text, nullable=True)  # base64 data URL

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, include_photo=True):
        d = {
            'id': self.id,
            'matricule': self.matricule,
            'nom': self.nom,
            'prenom': self.prenom,
            'email': self.email,
            'filiere': self.filiere,
            'niveau': self.niveau,
            'statut': self.statut,
            'date_naissance': self.date_naissance.isoformat() if self.date_naissance else None,
            'telephone': self.telephone,
            'adresse': self.adresse,
            'contact_urgence_nom': self.contact_urgence_nom,
            'contact_urgence_telephone': self.contact_urgence_telephone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_photo:
            d['photo'] = self.photo
        return d
