from flask import render_template, jsonify, request, redirect
from app.models.animal import Animal
from app import connect_database, disconnect_database, create_app, db

# Simulação de dados vindos do banco de dados
pacientes = [
    {'id': 1, 'nome': 'Marley', 'tutor': 'Ana Luiza Campos', 'especie': 'Cachorro', 'raca': 'Labrador', 'nascimento':
        '02-05-2018', 'sexo': 'M', 'peso': 10, 'cor': 'Preto'},
    {'id': 2, 'nome': 'Catherine', 'tutor':  'Célio Eduardo Júnior', 'especie': 'Gato', 'raca': 'SRD', 'nascimento':
        '15-08-2019', 'sexo': 'F', 'peso': 5, 'cor': 'Branco'},
    {'id': 3, 'nome': 'Thor', 'tutor': 'João Pedro Souza', 'especie': 'Cachorro', 'raca': 'Pitbull', 'nascimento':
        '10-10-2017', 'sexo': 'M', 'peso': 15, 'cor': 'Marrom'},
    {'id': 4, 'nome': 'Mel', 'tutor': 'Fernanda Oliveira', 'especie': 'Cachorro', 'raca': 'Poodle', 'nascimento':
        '25-12-2016', 'sexo': 'F', 'peso': 7.200, 'cor': 'Branco'},
    {'id': 5, 'nome': 'Rex', 'tutor': 'Carlos Eduardo Santos', 'especie': 'Cachorro', 'raca': 'SRD', 'nascimento':
        '30-07-2019', 'sexo': 'M', 'peso': 8, 'cor': 'Preto'}
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

app = create_app()
cursor, conn = connect_database()


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
        # Inserir no banco de dados aqui
        try:
            novo_animal = Animal(**data)
            db.session.add(novo_animal)
            db.session.commit()
            return jsonify({"mensagem": "Paciente cadastrado com sucesso!", "id_animal": novo_animal.id_animal}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": f"Erro ao cadastrar paciente: {str(e)}"}), 500

    return render_template('tela_cadastros/cadastro_pacientes.html')


@app.route('/api/pacientes')
def get_pacientes():
    """q_pacientes = Animal.query.all()
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
    } for p in q_pacientes]"""

    pacientes_lista = pacientes
    # colocar o cpf do tutor em vez do nome do tutor

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


@app.route('/sair')
def sair():
    # Fazer todos os processos de sair, tirar o usuário logado (?), desconectar o banco, etc
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
