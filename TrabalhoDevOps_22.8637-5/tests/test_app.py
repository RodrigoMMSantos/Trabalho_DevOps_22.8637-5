import pytest
from app import app
import mysql.connector

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_aluno(client):
    conn = mysql.connector.connect(
        user='usuario_escola',
        password='senha_forte',
        host='localhost',
        database='escola'
    )
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alunos")
    conn.commit()
    cursor.close()
    conn.close()

    response = client.post('/add', data={'nome': 'Aluno Teste', 'ra': '12345'}, follow_redirects=True)
    assert b'Aluno cadastrado com sucesso!' in response.data

    conn = mysql.connector.connect(
        user='usuario_escola',
        password='senha_forte',
        host='localhost',
        database='escola'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alunos WHERE ra = '12345'")
    aluno = cursor.fetchone()
    cursor.close()
    conn.close()

    assert aluno is not None
    assert aluno['nome'] == 'Aluno Teste'
    assert aluno['ra'] == '12345'
