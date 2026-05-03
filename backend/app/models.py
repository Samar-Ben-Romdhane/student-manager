from . import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'students'
    id        = db.Column(db.Integer, primary_key=True)
    nom       = db.Column(db.String(100), nullable=False)
    prenom    = db.Column(db.String(100), nullable=False)
    email     = db.Column(db.String(150), unique=True, nullable=False)
    filiere   = db.Column(db.String(100), nullable=False)
    niveau    = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 'nom': self.nom, 'prenom': self.prenom,
            'email': self.email, 'filiere': self.filiere,
            'niveau': self.niveau, 'created_at': self.created_at.isoformat()
        }
