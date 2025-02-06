from flask import Flask, render_template, jsonify, request
# from app import db
from models.animal import Animal
from routes.animal_route import animais_bp

app = Flask(__name__)
#app.config.from_object('app.config.Config') # configurações do bd

#db.init_app(app)    # inicializa o bd

app.register_blueprint(animais_bp, url_prefix='/api')

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
        data = {
            'id_tutor': request.form.get('tutor'),  # pegar o cpf (?) do tutor e achar o id
            'nome': request.form.get('nome'),
            'ano_nascimento': request.form.get('nascimento'),
            'sexo': request.form.get('sexo'),
            'especie': request.form.get('especie'),
            'raca': request.form.get('raca'),
            'peso': request.form.get('peso'),
            'cor': request.form.get('cor')
        }

        novo_animal = Animal(**data)

        # Inserir no banco de dados aqui
        # db.session.add(novo_animal)
        # db.session.commit()

        return jsonify({'mensagem': 'Paciente cadastrado com sucesso!', 'id_animal': novo_animal.id_animal}), 201

    return render_template('tela_cadastros/cadastro_pacientes.html')


@app.route('/api/pacientes')
def get_pacientes():
    q_pacientes = Animal.query.all()
    pacientes_lista = [{
        "id_animal": p.id_animal,
        "id_tutor": p.id_tutor,
        "nome": p.nome,
        "especie": p.especie,
        "raca": p.raca,
        "ano_nascimento": p.ano_nascimento,
        "sexo": p.sexo,  # Retorna 'M' ou 'F'
        "peso": p.peso,
        "cor": p.cor
    } for p in q_pacientes]

    return jsonify(pacientes_lista)


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
