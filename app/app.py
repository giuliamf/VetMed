from flask import render_template, jsonify, request, redirect, session
from app import create_app
from app.database import buscar_dados_usuario_por_email, buscar_usuario_por_id, execute_sql
from app.utils.criptografia_senhas import criptografar_senha, verificar_senha
from app.simulação_bd import usuarios, especialidades, agendamento, listastatus
from datetime import datetime

app = create_app()


@app.route('/', methods=['GET', 'POST'])
def login():
    if 'usuario' in session:
        return redirect('/inicio')
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            senha = request.form.get('senha')

            usuario = buscar_dados_usuario_por_email(email.lower())  # [id, email, senha]
            # Verificar se o usuário existe no banco de dados
            # Se sim, verificar se a senha está correta
            # Se sim, redirecionar para a página inicial

            if usuario and verificar_senha(senha, usuario[2]):
                session['usuario'] = usuario[0]  # Salva o id do usuário na sessão
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
    usuario = {"nome": "Usuário"}  # Valor padrão caso o usuário não seja encontrado
    if usuario_id:
        user_data = buscar_usuario_por_id(usuario_id)
        if user_data:
            usuario = {
                "id": user_data[0],
                "nome": user_data[1],
                "email": user_data[2],
            }

    return {'usuario': usuario}


@app.route('/inicio')
def inicio():
    if 'usuario' in session:
        return render_template('inicio.html')
    return redirect('/')


# Tela de cadastros e suas funcionalidades
@app.route('/cadastros')
def cadastro():
    return render_template('cadastros.html')


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


# Tela de agenda e suas funcionalidades
@app.route('/agenda')
def agenda():
    lista_agendamento = formatar_data(agendamento)
    return render_template('agenda.html', agendamento=lista_agendamento)


@app.route('/cadastro_agendamento', methods=['GET', 'POST'])
def cadastro_agendamento():
    if request.method == 'POST':
        data = {
            'hora': request.form.get('hora'),
            'data': request.form.get('data'),
            'paciente': request.form.get('paciente'),
            'tutor': request.form.get('tutor'),
            'status': 1  # status de agendado
        }
        # Inserir no banco de dados aqui
        return jsonify({"mensagem": "Agendamento realizado com sucesso!"}), 201

    return render_template('tela_cadastros/cadastro_agendamentos.html')


@app.route('/editar_agendamento', methods=['GET', 'POST'])
def editar_agendamento():
    # quando post for chamado, as unicas informações que podem ser alteradas são hora e status
    if request.method == 'POST':
        hora = request.form.get('hora')
        status = request.form.get('status')

        # Atualizar no banco de dados aqui
        return jsonify({"mensagem": "Agendamento atualizado com sucesso!"}), 200

    return render_template('tela_cadastros/editar_agendamento.html', status=listastatus)


@app.route('/api/status')
def get_status():
    return jsonify(listastatus)


@app.route('/api/agendamentos')
def get_agendamentos():
    lista_agendamentos = formatar_data(agendamento)
    return jsonify(lista_agendamentos)


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
    session.clear()  # Limpa a sessão
    return redirect('/')


# back-end
# MODIFICAR AQUI QUANDO DEFINIR A FUNCAO QUE VAI PEGAR A LISTA DE AGENDAMENTOS DO BD (ou colocar em outro lugar)
def formatar_data(lista_agenda):
    for a in lista_agenda:
        if type(a['data']) != datetime:  # Se a data já estiver no formato datetime, não precisa converter
            try:
                a['data'] = datetime.strptime(a['data'], '%d/%m/%Y')  # Converte a data para o formato datetime
            except ValueError:
                continue
        a['data'] = a['data'].strftime('%Y-%m-%d')  # Converte a data para o formato 'AAAA-MM-DD'
    return lista_agenda


if __name__ == '__main__':
    app.run(debug=True)
