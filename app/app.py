from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Simulação de dados vindos do banco de dados
pacientes = [
    {'nome': 'Marley (Ana Luiza Campos)'},
    {'nome': 'Catherine (Célio Eduardo Júnior)'},
    {'nome': 'Thor (João Pedro Souza)'},
    {'nome': 'Mel (Fernanda Oliveira)'},
    {'nome': 'Rex (Carlos Eduardo Santos)'}
]

tutores = [
    {'nome': 'Ana Luiza Campos'},
    {'nome': 'Célio Eduardo Júnior'},
    {'nome': 'João Pedro Souza'},
    {'nome': 'Fernanda Oliveira'},
    {'nome': 'Carlos Eduardo Santos'}
]

usuarios = [
    {'nome': 'Giulia Moura Ferreira'},
    {'nome': 'Célio Eduardo Júnior'},
    {'nome': 'Ana Luiza Campos'},
]


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/inicio')
def inicio():
    return render_template('inicio.html')


# Tela de agenda e suas funcionalidades
@app.route('/agenda')
def agenda():
    return render_template('agenda.html')


# Tela de cadastros e suas funcionalidades
@app.route('/cadastros')
def cadastro():
    return render_template('cadastros.html')


@app.route('/pacientes')
def pacientes_page():
    return render_template('tela_cadastros/pacientes.html', pacientes=pacientes)


@app.route('/cadastro_paciente', methods=['GET', 'POST'])
def cadastro_paciente():
    if request.method == 'POST':
        nome = request.form.get('nome')
        nascimento = request.form.get('nascimento')
        sexo = request.form.get('sexo')
        especie = request.form.get('especie')
        raca = request.form.get('raca')
        peso = request.form.get('peso')
        cor = request.form.get('cor')
        tutor = request.form.get('tutor')

        novo_paciente = {
            'nome': nome,
            'nascimento': nascimento,
            'sexo': sexo,
            'especie': especie,
            'raca': raca,
            'peso': peso,
            'cor': cor,
            'tutor': tutor
        }

        # Inserir no banco de dados aqui
        # db....add(novo_paciente)
        # db.commit()

    return render_template('tela_cadastros/cadastro_pacientes.html')


@app.route('/api/pacientes')
def get_pacientes():
    return jsonify(pacientes)


@app.route('/tutores')
def tutores_page():
    return render_template('tela_cadastros/tutores.html', tutores=tutores)


@app.route('/api/tutores')
def get_tutores():
    return jsonify(tutores)


@app.route('/usuarios')
def usuarios_page():
    return render_template('tela_cadastros/usuarios.html', usuarios=usuarios)


# Tela de consultas e suas funcionalidades
@app.route('/consultas')
def consultas():
    return render_template('consultas.html')


# Tela do financeiro e suas funcionalidades
@app.route('/financeiro')
def financeiro():
    return render_template('financeiro.html')


if __name__ == '__main__':
    app.run(debug=True)
