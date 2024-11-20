from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'

db_config = {
    'user': 'usuario_escola',
    'password': 'senha_forte',
    'host': 'localhost',
    'database': 'escola'
}

@app.route('/')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', alunos=alunos)

@app.route('/add', methods=['POST'])
def add_aluno():
    nome = request.form['nome']
    ra = request.form['ra']
    if nome and ra:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO alunos (nome, ra) VALUES (%s, %s)", (nome, ra))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Aluno cadastrado com sucesso!')
    else:
        flash('Todos os campos são obrigatórios.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
