import pytest
from flask import url_for
from app import app, users, events, db
from datetime import datetime
from flask_login import current_user, login_user
from unittest.mock import MagicMock
from bson import ObjectId
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

@pytest.fixture
def client(monkeypatch):
    app.config['TESTING'] = True
    mock_users = MagicMock()
    mock_events = MagicMock()
    monkeypatch.setattr(db, 'users', mock_users)
    monkeypatch.setattr(db, 'events', mock_events)
    with app.test_client() as client:
        mock_users.reset_mock()
        mock_events.reset_mock()
        yield client
        mock_users.reset_mock()
        mock_events.reset_mock()

@pytest.fixture
def mock_user():
    mock_user = MagicMock()
    mock_user.is_authenticated = True
    mock_user.get_id.return_value = "testuser"
    mock_user.username = "testuser"
    
    def mock_user_loader(user_id):
        return mock_user if user_id == "testuser" else None
    
    users.user_loader = mock_user_loader  
    return mock_user

def test_register_get(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_register_post(client, monkeypatch):
    mock_insert = MagicMock()
    monkeypatch.setattr(users, 'insert_one', mock_insert)
    response = client.post('/register', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful. You can now log in.' in response.data
    mock_insert.assert_called_once_with({'username': 'testuser', 'password': 'password'})

def test_register_existing_user(client, monkeypatch):
    mock_find_one = MagicMock(return_value={'username': 'existinguser'})
    monkeypatch.setattr(users, 'find_one', mock_find_one)
    response = client.post('/register', data={'username': 'existinguser', 'password': 'password'}, follow_redirects=True)
    assert b'Username already exists' in response.data
    mock_find_one.assert_called_once_with({'username': 'existinguser'})

def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_login_post_success(client, monkeypatch):
    mock_find_one = MagicMock(side_effect=[
        {'username': 'testuser', 'password': 'password'},
        {'username': 'testuser', 'password': 'password'}
    ])
    monkeypatch.setattr(users, 'find_one', mock_find_one)
    response = client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
    assert b'Login Required' not in response.data
    mock_find_one.assert_any_call({'username': 'testuser'})
    mock_find_one.assert_any_call({'username': 'testuser', 'password': 'password'})
    assert mock_find_one.call_count == 2

def test_login_post_failure(client, monkeypatch):
    mock_find_one = MagicMock(return_value=None)
    monkeypatch.setattr(users, 'find_one', mock_find_one)
    response = client.post('/login', data={'username': 'wronguser', 'password': 'wrongpassword'}, follow_redirects=True)
    assert b'Invalid username or password' in response.data
    mock_find_one.assert_called_once_with({'username': 'wronguser', 'password': 'wrongpassword'})

def test_status(client):
    response = client.get('/api/status')
    assert response.status_code == 200
    assert b'logged_in' in response.data

def test_delete_event(client, monkeypatch):
    mock_find_one = MagicMock(return_value={'_id': ObjectId('507f191e810c19729de860ea'), 'name': 'Test Event'})
    mock_delete = MagicMock()
    monkeypatch.setattr(events, 'find_one', mock_find_one)
    monkeypatch.setattr(events, 'delete_one', mock_delete)
    event_id = '507f191e810c19729de860ea'
    response = client.get(f'/event/{event_id}/delete', follow_redirects=True)
    mock_delete.assert_called_once_with({"_id": ObjectId(event_id)})