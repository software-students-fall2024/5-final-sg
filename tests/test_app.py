import pytest
from flask import url_for
from app import app, users, events, db
from datetime import datetime
import os
from unittest.mock import patch
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_db'  # Use a separate test database

    # Set up a test client
    with app.test_client() as client:
        # Reset the database before each test
        db.users.delete_many({})  # Clear users collection
        yield client  
        db.users.delete_many({})
        db.events.delete_many({})  

def test_register_get(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data


def test_register_post(client):
    response = client.post('/register', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful. You can now log in.' in response.data
    assert users.find_one({'username': 'testuser'})


def test_register_existing_user(client):
    users.insert_one({'username': 'existinguser', 'password': 'password'})
    response = client.post('/register', data={'username': 'existinguser', 'password': 'password'}, follow_redirects=True)
    assert b'Username already exists' in response.data


def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_login_post_success(client):
    users.insert_one({'username': 'testuser', 'password': 'password'})
    response = client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
    assert b'Login Required' not in response.data


def test_login_post_failure(client):
    response = client.post('/login', data={'username': 'wronguser', 'password': 'wrongpassword'}, follow_redirects=True)
    assert b'Invalid username or password' in response.data


def test_status(client):
    response = client.get('/api/status')
    assert response.status_code == 200
    assert b'logged_in' in response.data


def test_add_event(client):
    users.insert_one({'username': 'testuser', 'password': 'password'})
    client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)

    response = client.post('/event/add', data={
        'fname': 'Test Event',
        'fmessage': 'Event Description',
        'hours': '12',
        'minutes': '30',
        'date': '12/31/2024'
    }, follow_redirects=True)
    assert events.find_one({'name': 'Test Event', 'user': 'testuser'})


def test_delete_event(client):
    users.insert_one({'username': 'testuser', 'password': 'password'})
    client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)

    event_time = datetime(2024, 12, 11, 12, 30)
    event_id = events.insert_one({
        'name': 'Test Event',
        'description': 'Event Description',
        'time': event_time.strftime('%Y-%m-%d %H:%M:%S'),
        'user': 'testuser'
    }).inserted_id

    response = client.get(f'/event/{event_id}/delete', follow_redirects=True)

    assert events.find_one({'_id': event_id}) is None


def test_edit_event(client):
    users.insert_one({'username': 'testuser', 'password': 'password'})
    client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)

    event_time = datetime(2024, 12, 31, 12, 30)
    event_id = events.insert_one({
        'name': 'Old Event',
        'description': 'Old Description',
        'time': event_time.strftime('%Y-%m-%d %H:%M:%S'),
        'user': 'testuser'
    }).inserted_id

    response = client.post(f'/event/{event_id}/edit', data={
        'fname': 'Updated Event',
        'fmessage': 'Updated Description',
        'hours': '14',
        'minutes': '00',
        'date': '01/01/2025'
    }, follow_redirects=True)

    updated_event = events.find_one({'_id': event_id})
    assert updated_event['name'] == 'Updated Event'
    assert updated_event['description'] == 'Updated Description'
