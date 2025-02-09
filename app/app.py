from flask import render_template, jsonify, request, redirect, session
from app.models.animal import Animal
from app import connect_database, disconnect_database, create_app, db
from app.criptografia_senhas import criptografar_senha, verificar_senha

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
    {'id': 1, 'nome': 'Giulia Moura Ferreira', 'email': 'giulia@gmail.com', 'cargo': 'vet', 'especialidade': 1, 'senha':
        'e4c2eed8a6df0147265631e9ff25b70fd0e4b3a246896695b089584bf3ce8b90'},
    {'id': 2, 'nome': 'Célio Eduardo Júnior', 'email': 'celio@gmail.com', 'cargo': 'sec', 'senha':
        '60fe67ed8156498b9a17f3d983bcf3961d7aa8c36e33bf2edf2ccf1706d33fef'},
    {'id': 3, 'nome': 'Ana Luiza Campos', 'email': 'analuiza@gmail.com', 'cargo': 'vet', 'especialidade': 2,
     'senha': '0a3fa8009c0f56804c7bee62f18836d7bf84743d7ba2b2d0fb151e03b71a6b81'},
]

especialidades = [
    {'id': 1, 'nome': 'Clínica Geral'},
    {'id': 2, 'nome': 'Ortopedia'},
    {'id': 3, 'nome': 'Dermatologia'},
    {'id': 4, 'nome': 'Oftalmologia'},
    {'id': 5, 'nome': 'Cardiologia'},
    {'id': 6, 'nome': 'Cirurgia'}
]

app = create_app()
cursor, conn = connect_database()


@app.route('/', methods=['GET', 'POST'])
def login():
    if session:
        return redirect('/inicio')
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            senha = request.form.get('senha')

            # Verificar se o usuário existe no banco de dados
            # Se sim, verificar se a senha está correta
            # Se sim, redirecionar para a página inicial
            usuario = next((u for u in usuarios if u['email'] == email.lower()), None)

            if usuario and verificar_senha(senha, usuario['senha']):
                session['usuario'] = usuario['id']  # Salva o id do usuário na sessão
                return redirect('/inicio')
            elif not usuario:
                return jsonify({"erro": "Usuário não encontrado!"}), 404
            else:
                return jsonify({"erro": "Senha incorreta!"}), 401

    return render_template('login.html')


@app.context_processor
def inject_user():
    # Caso o usuário entre nessa página, com certeza ele estará logado.
    usuario_id = session.get('usuario')
    usuario = next((u for u in usuarios if u['id'] == usuario_id), {"nome": "Usuário"})
    return {'usuario': usuario}


@app.route('/inicio')
def inicio():
    if 'usuario' in session:
        return render_template('inicio.html')
    return redirect('/')


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
            'nascimento': request.form.get('nascimento'),
            'telefone': request.form.get('telefone'),
            'endereco': {
                'bairro': request.form.get('bairro'),
                'cidade': request.form.get('cidade'),
                'estado': request.form.get('estado')
            }
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


@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        senha = request.form.get('senha')
        senha_criptografada = criptografar_senha(senha)

        data = {
            'nome': request.form.get('nome'),
            'email': request.form.get('email'),
            'senha': senha_criptografada,
            'cargo': request.form.get('cargo'),
        }
        if data['cargo'] == 'vet':
            data['especialidade'] = request.form.get('especialidade')

        # Inserir no banco de dados aqui
        return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201

    return render_template('tela_cadastros/cadastro_usuarios.html', especialidades=especialidades)


@app.route('/api/usuarios')
def get_usuarios():
    usuarios_lista = usuarios
    return jsonify(usuarios_lista)


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
    session.clear()     # Limpa a sessão
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
