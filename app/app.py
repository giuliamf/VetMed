from flask import render_template, jsonify, request, redirect, send_from_directory
from app.models.animal import Animal
from app import connect_database, disconnect_database, create_app, db

# Simulação de dados vindos do banco de dados
pacientes = [
    {'id': 1, 'nome': 'Marley', 'tutor': 1, 'especie': 'Cachorro', 'raca':
        'Labrador', 'nascimento': '02-05-2018', 'sexo': 'M', 'peso': 10, 'cor': 'Preto'},
    {'id': 2, 'nome': 'Catherine', 'tutor':  3, 'especie': 'Gato', 'raca':
        'SRD', 'nascimento': '15-08-2019', 'sexo': 'F', 'peso': 5, 'cor': 'Branco'},
    {'id': 3, 'nome': 'Thor', 'tutor': 2, 'especie': 'Cachorro', 'raca': 'Pitbull',
     'nascimento': '10-10-2017', 'sexo': 'M', 'peso': 15, 'cor': 'Marrom'},
    {'id': 4, 'nome': 'Mel', 'tutor': 4, 'especie': 'Cachorro', 'raca': 'Poodle',
     'nascimento': '25-12-2016', 'sexo': 'F', 'peso': 7.200, 'cor': 'Branco'},
    {'id': 5, 'nome': 'Rex', 'tutor': 5, 'especie': 'Cachorro', 'raca': 'SRD',
     'nascimento': '30-07-2019', 'sexo': 'M', 'peso': 8, 'cor': 'Preto'}
]

tutores = [
    {'id': 1, 'nome': 'Ana Luiza Campos', 'cpf': '123.456.789-00', 'nascimento': '02-05-1995', 'telefone':
        '(61) 99999-9999', 'endereco': {'bairro': 'Asa Sul', 'cidade': 'Brasília', 'estado': 'DF'}},
    {'id': 2, 'nome': 'João Pedro Souza', 'cpf': '456.789.123-00', 'nascimento': '10-10-1996', 'telefone':
        '(61) 77777-7777', 'endereco': {'bairro': 'Taguatinga', 'cidade': 'Brasília', 'estado': 'DF'}},
    {'id': 3, 'nome': 'Célio Eduardo Júnior', 'cpf': '987.654.321-00', 'nascimento': '15-08-1994', 'telefone':
        '(61) 88888-8888', 'endereco': {'bairro': 'Samambaia', 'cidade': 'Brasília', 'estado': 'DF'}},
    {'id': 4, 'nome': 'Fernanda Oliveira', 'cpf': '789.123.456-00', 'nascimento': '25-12-1997', 'telefone':
        '(61) 66666-6666', 'endereco': {'bairro': 'Ceilândia', 'cidade': 'Brasília', 'estado': 'DF'}},
    {'id': 5, 'nome': 'Carlos Eduardo Santos', 'cpf': '321.654.987-00', 'nascimento': '30-07-1998', 'telefone':
        '(61) 55555-4444', 'endereco': {'bairro': 'Asa Norte', 'cidade': 'Brasília', 'estado': 'DF'}}
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
    # colocar o id em vez do nome do tutor

    return jsonify(pacientes_lista)


@app.route('/tutores')
def tutores_page():
    return render_template('tela_cadastros/tutores.html', tutores=tutores)


@app.route('/cadastro_tutor', methods=['GET', 'POST'])
def cadastro_tutor():
    if request.method == 'POST':
        data = {
            'nome': request.form.get('nome'),
            'cpf': request.form.get('cpf'),
            'email': request.form.get('email'),
            'telefone': request.form.get('telefone'),
            'endereco': request.form.get('endereco')
        }
        # Inserir no banco de dados aqui
        return jsonify({"mensagem": "Tutor cadastrado com sucesso!"}), 201

    return render_template('tela_cadastros/cadastro_tutores.html')


@app.route('/api/tutores')
def get_tutores():
    tutores_lista = tutores
    return jsonify(tutores_lista)


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
