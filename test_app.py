import app
from chalice import Response
from chalice.test import Client

local_url = 'http://127.0.0.1:8000/'
chalice_url = 'https://19cx2ehing.execute-api.us-east-1.amazonaws.com/api/'

# NOTE: to execute tests, please download northwind.db into /tmp

def test_query():
    result = app.query("SELECT * FROM Categories;", '/mnt/lambda/efs-sqlite/northwind.db', 'SOME_TOKEN')
    assert type(result) == list

def test_jsonify():
    result = app.jsonify(b'some_bytes')
    assert type(result) == str

def test_get_file():
    file_name = app.get_file('/mnt/lambda/efs-sqlite/northwind.db')
    assert file_name == '/tmp/northwind.db'

def test_post_do_query():
    import requests
    payload = {'statement': 'SELECT * FROM Categories;', 'file': '/mnt/lambda/efs-sqlite/northwind.db', 
                             'token': 'SOME_TOKEN'}
    response = requests.post('http://127.0.0.1:8000/query', json=payload)
    assert response.status_code == 200

def test_index():
    import requests
    response = requests.get('http://127.0.0.1:8000/')
    assert response.status_code == 200
    assert b'axios' in response.content
    assert b'statement' in response.content
    assert b'file' in response.content
    assert b'token' in response.content
    assert b'result' in response.content
    assert b'submit' in response.content
    assert b'url' in response.content
    assert b'handsontable' in response.content