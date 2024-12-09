import pytest
from flask import url_for
from app import app, users, events

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_user(client):
    response = client.post('/register', data={
        'username': 'test_user',
        'password': 'test_pass'
    })
    assert response.status_code == 302  # Redirect after successful registration
    assert b'Registration successful' in response.data or b'Username already exists' in response.data

def test_login_user(client):
    # Ensure test user exists
    users.insert_one({'username': 'test_user', 'password': 'test_pass'})
    
    response = client.post('/login', data={
        'username': 'test_user',
        'password': 'test_pass'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Login Required' not in response.data

def test_invalid_login(client):
    response = client.post('/login', data={
        'username': 'invalid_user',
        'password': 'wrong_pass'
    })
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_status_route(client):
    with client.session_transaction() as session:
        session['_user_id'] = 'test_user'
    
    response = client.get('/api/status')
    assert response.status_code == 200
    assert b'logged_in' in response.data

def test_add_event(client):
    with client.session_transaction() as session:
        session['_user_id'] = 'test_user'

    response = client.post('/event/add', data={
        'fname': 'Test Event',
        'fmessage': 'Event description',
        'hours': '10',
        'minutes': '30',
        'date': '12/25/2024'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert events.find_one({'name': 'Test Event'})

def test_edit_event(client):
    with client.session_transaction() as session:
        session['_user_id'] = 'test_user'

    # Insert test event
    event_id = events.insert_one({
        'name': 'Old Event',
        'description': 'Old Description',
        'time': '2024-12-25T10:30:00',
        'user': 'test_user'
    }).inserted_id

    response = client.post(f'/event/{event_id}/edit', data={
        'fname': 'Updated Event',
        'fmessage': 'Updated Description',
        'hours': '11',
        'minutes': '00',
        'date': '12/26/2024'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    updated_event = events.find_one({'_id': event_id})
    assert updated_event['name'] == 'Updated Event'

def test_delete_event(client):
    with client.session_transaction() as session:
        session['_user_id'] = 'test_user'

    # Insert test event
    event_id = events.insert_one({
        'name': 'Delete Event',
        'description': 'To be deleted',
        'time': '2024-12-25T10:30:00',
        'user': 'test_user'
    }).inserted_id

    response = client.get(f'/event/{event_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert not events.find_one({'_id': event_id})