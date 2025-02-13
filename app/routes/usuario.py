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

            if 'especialidade' not in data or not data['especialidade']:
                return jsonify({"erro": "Especialidade é obrigatória para veterinários!"}), 400

            if 'turno' not in data or not data['turno']:
                return jsonify({"erro": "Turno é obrigatório para veterinários!"}), 400

            query_vet = """
                INSERT INTO Veterinario (id_veterinario, id_especialidade)
                VALUES (%s, %s)
            """
            params_vet = (
                id_usuario[0],
                data['especialidade']
            )
            execute_sql(query_vet, params_vet)

            query_turno = """
                    INSERT INTO Carga_Horaria (id_veterinario, turno)
                    VALUES (%s, %s)
                """

            params_turno = (id_usuario[0], data['turno'])
            execute_sql(query_turno, params_turno)

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

            data['senha'] = criptografar_senha(data['senha'])

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

                query_turno = """
                    INSERT INTO Carga_Horaria (id_veterinario, turno)
                    VALUES (%s, %s)
                    ON CONFLICT (id_veterinario)
                    DO UPDATE SET turno = EXCLUDED.turno;
                """

                params_turno = (usuario_id, data['turno'])
                execute_sql(query_turno, params_turno)

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


@usuarios_bp.route('/api/usuarios/<int:usuario_id>/foto', methods=['GET', 'PUT'])
def atualizar_foto_usuario(usuario_id):
    if request.method == 'GET':
        try:
            query = "SELECT foto FROM Usuario_Foto WHERE id_usuario = %s"
            resultado = execute_sql(query, (usuario_id,), fetch_one=True)

            if not resultado or not resultado[0]:
                return jsonify({"erro": "Foto não encontrada"}), 404

            # Retorna a foto como resposta binária
            return resultado[0], 200, {'Content-Type': 'image/jpeg'}
        except Exception as e:
            return jsonify({"erro": f"Erro ao buscar foto: {str(e)}"}), 500

    """ Atualiza a foto do usuário """

    if request.method == 'PUT':
        if 'foto' not in request.files:
            return jsonify({"erro": "Nenhuma foto foi enviada"}), 400

        foto = request.files['foto'].read()  # Lê a foto como bytes

        try:
            query = """
                INSERT INTO Usuario_Foto (id_usuario, foto)
                VALUES (%s, %s)
                ON CONFLICT (id_usuario) 
                DO UPDATE SET foto = EXCLUDED.foto;
            """
            execute_sql(query, (usuario_id, foto))

            return jsonify({"mensagem": "Foto atualizada com sucesso!"}), 200
        except Exception as e:
            return jsonify({"erro": f"Erro ao atualizar foto: {str(e)}"}), 500


@usuarios_bp.route("/api/usuarios/<int:usuario_id>", methods=["DELETE"])
def excluir_usuario(usuario_id):
    try:
        # Verifica se o usuário existe
        usuario_existe = execute_sql("SELECT 1 FROM Usuario WHERE id_usuario = %s", (usuario_id,), fetch_one=True)
        if not usuario_existe:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        # Remove o usuário e a foto (ON DELETE CASCADE já deve remover em Usuario_Foto)
        execute_sql("DELETE FROM Usuario WHERE id_usuario = %s", (usuario_id,))

        return jsonify({"mensagem": "Usuário excluído com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao excluir usuário: {str(e)}"}), 500


@usuarios_bp.route('/api/turnos', methods=['GET'])
def get_turnos():
    """ Retorna os turnos disponíveis para cadastro de veterinários """
    try:
        turnos = [{"id": "manha", "nome": "Manhã"}, {"id": "tarde", "nome": "Tarde"}]
        return jsonify(turnos), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar turnos: {str(e)}"}), 500


# Rotas para renderizar páginas HTML
@usuarios_bp.route('/usuarios')
def usuarios_page():
    """ Renderiza a página de usuários """
    return render_template('tela_cadastros/usuarios.html')


@usuarios_bp.route('/cadastro_usuario_page')
def cadastro_usuario_page():
    return render_template('tela_cadastros/cadastro_usuarios.html')


@usuarios_bp.route('/popup_foto')
def popup_foto():
    """ Renderiza a popup de alteração de foto """
    return render_template('tela_cadastros/popup_foto.html')
