from flask import Blueprint, request, jsonify, render_template
from app.database import execute_sql

from app.utils.criptografia_senhas import criptografar_senha

usuarios_bp = Blueprint('usuarios', __name__)


@usuarios_bp.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    """ Retorna a lista de usuários do banco de dados """
    try:
        query = """
            SELECT u.id_usuario, u.email, u.nome, u.senha, u.cargo, v.id_especialidade
            FROM Usuario u
            LEFT JOIN Veterinario v ON u.id_usuario = v.id_veterinario
            WHERE u.cargo != 'adm'
            ORDER BY u.id_usuario ASC
        """
        # Pegar todos os usuários, inclusive veterinários e suas especialidades
        usuarios = execute_sql(query, fetch_all=True)

        usuarios_lista = [
            {
                "id": u[0],
                "email": u[1],
                "nome": u[2],
                "senha": u[3],
                "cargo": u[4],
                "especialidade": u[5] if u[4] == 'vet' else None     # Se não for veterinário, especialidade é None
            }
            for u in usuarios
        ]

        return jsonify(usuarios_lista), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar usuários: {str(e)}"}), 500


@usuarios_bp.route('/cadastro_usuario', methods=['POST'])
def cadastro_usuario():
    """ Cadastro de novo usuário """
    if not request.json:
        return jsonify({"erro": "Nenhum dado JSON foi recebido"}), 400

    data = request.json

    if not all(key in data for key in ["nome", "email", "senha", "cargo"]):
        return jsonify({"erro": "Campos obrigatórios ausentes!"}), 400

    if not all(data.values()):
        return jsonify({"erro": "Preencha todos os campos!"}), 400

    # criptografar a senha recebida
    data['senha'] = criptografar_senha(data['senha'])

    try:
        query = """
            INSERT INTO Usuario (email, nome, senha, cargo)
            VALUES (%s, %s, %s, %s)
        """
        params = (
            data['email'],
            data['nome'],
            data['senha'],
            data['cargo']
        )
        execute_sql(query, params)

        # Se o cargo for 'vet', cadastrar na tabela Veterinario
        if data['cargo'] == 'vet':
            # Obter o id a partir do execute_sql anterior
            id_usuario = execute_sql(
                "SELECT id_usuario FROM Usuario WHERE email = %s", (data['email'],), fetch_one=True)

            query_vet = """
                INSERT INTO Veterinario (id_veterinario, id_especialidade)
                VALUES (%s, %s)
            """
            params_vet = (
                id_usuario[0],
                data['especialidade']
            )
            execute_sql(query_vet, params_vet)

        return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"erro": f"Erro ao cadastrar usuário: {str(e)}"}), 500


@usuarios_bp.route('/api/usuarios/<int:usuario_id>', methods=['GET', 'PUT'])
def editar_usuario(usuario_id):
    """ Rota para editar um usuário """
    if request.method == 'GET':
        # Buscar usuário pelo ID no banco de dados
        query = """
            SELECT u.id_usuario, u.email, u.nome, u.senha, u.cargo, v.id_especialidade
            FROM Usuario u
            LEFT JOIN Veterinario v ON u.id_usuario = v.id_veterinario
            WHERE u.id_usuario = %s
            """
        resultado = execute_sql(query, (usuario_id,), fetch_one=True)

        if not resultado:
            return jsonify({"erro": "Usuário não encontrado!"}), 404

        usuario = {
            "id": resultado[0],
            "email": resultado[1],
            "nome": resultado[2],
            "senha": resultado[3],
            "cargo": resultado[4],
            "especialidade": resultado[5] if resultado[4] == "vet" else None  # Só retorna especialidade se for 'vet'
        }

        return jsonify(usuario), 200

    if request.method == 'PUT':

        if not request.is_json:
            return jsonify({"erro": "Formato inválido! Use 'application/json'"}), 415

        data = request.get_json()
        print("Recebendo dados para atualização:", data)  # Debug no console

        if not all(key in data for key in ["nome", "email", "senha", "cargo"]):
            return jsonify({"erro": "Campos obrigatórios ausentes!"}), 400

        if not all(data.values()):
            return jsonify({"erro": "Preencha todos os campos!"}), 400

        try:
            # Conferir se a senha foi modificada
            query_senha = "SELECT senha FROM Usuario WHERE id_usuario = %s"
            senha_atual = execute_sql(query_senha, (usuario_id,), fetch_one=True)

            if senha_atual and senha_atual[0] != data['senha']:
                # criptografar a nova senha recebida
                data['senha'] = criptografar_senha(data['senha'])

            query = """
                UPDATE Usuario
                SET email = %s, nome = %s, senha = %s, cargo = %s
                WHERE id_usuario = %s
            """
            params = (
                data['email'],
                data['nome'],
                data['senha'],
                data['cargo'],
                usuario_id
            )
            execute_sql(query, params)

            # Se o cargo for 'vet', atualizar na tabela Veterinario
            if data['cargo'] == 'vet' and 'especialidade' in data and data['especialidade']:
                query_vet = """
                    INSERT INTO Veterinario (id_veterinario, id_especialidade)
                    VALUES (%s, %s)
                    ON CONFLICT (id_veterinario) 
                    DO UPDATE SET id_especialidade = EXCLUDED.id_especialidade;
                """
                params_vet = (
                    data['especialidade'],
                    usuario_id
                )
                execute_sql(query_vet, params_vet)

            return jsonify({"mensagem": "Usuário atualizado com sucesso!"}), 200
        except Exception as e:
            return jsonify({"erro": f"Erro ao atualizar usuário: {str(e)}"}), 500


@usuarios_bp.route('/api/especialidades', methods=['GET'])
def get_especialidades():
    """ Retorna a lista de especialidades """
    try:
        query = "SELECT * FROM Especialidade ORDER BY nome ASC"
        especialidades = execute_sql(query, fetch_all=True)

        especialidades_lista = [
            {
                "id": e[0],
                "nome": e[1]
            }
            for e in especialidades
        ]

        return jsonify(especialidades_lista), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar especialidades: {str(e)}"}), 500


# Rotas para renderizar páginas HTML
@usuarios_bp.route('/usuarios')
def usuarios_page():
    """ Renderiza a página de usuários """
    return render_template('tela_cadastros/usuarios.html')


@usuarios_bp.route('/cadastro_usuario_page')
def cadastro_usuario_page():
    return render_template('tela_cadastros/cadastro_usuarios.html')
