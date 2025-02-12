from flask import Blueprint, request, jsonify, render_template
from app.database import execute_sql

usuarios_bp = Blueprint('usuarios', __name__)


@usuarios_bp.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    """ Retorna a lista de usuários do banco de dados """
    try:
        query = "SELECT * FROM Usuario ORDER BY id_usuario ASC"
        usuarios = execute_sql(query, fetch_all=True)

        usuarios_lista = [
            {
                "id": u[0],
                "email": u[1],
                "nome": u[2],
                "senha": u[3],
                "cargo": u[4]
            }
            for u in usuarios
        ]

        for usuario in usuarios_lista:
            if usuario['cargo'] == 'vet':
                query = "SELECT * FROM Veterinario WHERE email = %s"
                vet = execute_sql(query, (usuario['email'],), fetch_one=True)
                usuario['especialidade'] = vet[1]

        return jsonify(usuarios_lista), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar usuários: {str(e)}"}), 500


# Rotas para renderizar páginas HTML
@usuarios_bp.route('/usuarios')
def usuarios_page():
    """ Renderiza a página de usuários """
    return render_template('tela_cadastros/usuarios.html')


@usuarios_bp.route('/cadastro_usuario_page')
def cadastro_usuario_page():
    return render_template('tela_cadastros/cadastro_usuarios.html')