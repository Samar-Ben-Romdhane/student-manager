from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
import os

db = SQLAlchemy()
metrics = PrometheusMetrics.for_app_factory()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://student_user:student_pass@db:5432/student_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

    CORS(app)
    db.init_app(app)
    metrics.init_app(app)

    from .routes import bp
    from .auth import auth_bp
    app.register_blueprint(bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()
        _seed_default_admin()

    return app


def _seed_default_admin():
    from .models import User
    if User.query.count() == 0:
        admin = User(nom='Administrateur', email='admin@univ.tn', role='Admin')
        admin.set_password('Admin@2026')  # nosec B105
        db.session.add(admin)
        db.session.commit()
        print('>>> Compte admin créé : admin@univ.tn / Admin@2026')
