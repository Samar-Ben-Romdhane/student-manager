import os
import pytest

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['SECRET_KEY'] = 'test-secret-key'

from app import create_app


@pytest.fixture
def app():
    flask_app = create_app()
    flask_app.config['TESTING'] = True
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin_token(client):
    res = client.post('/api/auth/login', json={
        'email': 'admin@univ.tn',
        'password': 'Admin@2026'
    })
    return res.get_json()['access_token']


def test_health(client):
    res = client.get('/api/health')
    assert res.status_code == 200
    assert res.get_json()['status'] == 'ok'


def test_login_success(client):
    res = client.post('/api/auth/login', json={
        'email': 'admin@univ.tn',
        'password': 'Admin@2026'
    })
    assert res.status_code == 200
    data = res.get_json()
    assert 'access_token' in data
    assert data['user']['role'] == 'Admin'


def test_login_invalid_credentials(client):
    res = client.post('/api/auth/login', json={
        'email': 'admin@univ.tn',
        'password': 'wrong-password'
    })
    assert res.status_code == 401


def test_students_requires_auth(client):
    res = client.get('/api/students')
    assert res.status_code == 401


def test_add_and_list_student(client, admin_token):
    headers = {'Authorization': f'Bearer {admin_token}'}
    res = client.post('/api/students', json={
        'nom': 'Ben Ali', 'prenom': 'Yassine', 'email': 'yassine@univ.tn',
        'filiere': 'Informatique', 'niveau': 'L3'
    }, headers=headers)
    assert res.status_code == 201
    data = res.get_json()
    assert data['matricule'].startswith('ETU-')

    res = client.get('/api/students', headers=headers)
    assert res.status_code == 200
    assert len(res.get_json()) == 1


def test_delete_requires_admin(client, admin_token):
    headers = {'Authorization': f'Bearer {admin_token}'}
    res = client.post('/api/students', json={
        'nom': 'Test', 'prenom': 'User', 'email': 'test.user@univ.tn',
        'filiere': 'Business', 'niveau': 'L1'
    }, headers=headers)
    student_id = res.get_json()['id']

    res = client.delete(f'/api/students/{student_id}', headers=headers)
    assert res.status_code == 200


def test_stats(client, admin_token):
    headers = {'Authorization': f'Bearer {admin_token}'}
    res = client.get('/api/stats', headers=headers)
    assert res.status_code == 200
    assert 'total' in res.get_json()
