from flask import Blueprint, request, jsonify, render_template
from psycopg2.errors import UniqueViolation
from app.database import execute_sql

from app.utils.formatar_cpf import formatar_cpf

tutores_bp = Blueprint('tutores', __name__)


# Rota para retornar a lista de tutores
@tutores_bp.route('/api/tutores', methods=['GET'])
def get_tutores():
    """ Retorna a lista de tutores do banco de dados """
    query = "SELECT id_tutor, cpf, nome, data_nascimento, telefone, endereco FROM Tutor"
    tutores = execute_sql(query, fetch_all=True)

    tutores_lista = [
        {
            "id": t[0],
            "cpf": t[1],
            "nome": t[2],
            "nascimento": str(t[3]),
            "telefone": t[4],
            "endereco": t[5]
        }
        for t in tutores
    ]

    return jsonify(tutores_lista)


# Rota para cadastrar um tutor
@tutores_bp.route('/cadastro_tutor', methods=['POST'])
def cadastro_tutor():
    """ Cadastro de novo tutor """
    if not request.json:
        return jsonify({"erro": "Nenhum dado JSON foi recebido"}), 400

    data = request.json

    # Verificar se todos os campos estão presentes
    if not all(key in data for key in ["nome", "cpf", "nascimento", "telefone", "endereco"]):
        return jsonify({"erro": "Campos obrigatórios ausentes!"}), 400

    if not all(data.values()):
        return jsonify({"erro": "Preencha todos os campos!"}), 400

    data['cpf'] = formatar_cpf(data['cpf'])
    try:
        query = """
            INSERT INTO Tutor (cpf, nome, data_nascimento, telefone, endereco)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            data['cpf'],
            data['nome'],
            data['nascimento'],
            data['telefone'],
            data['endereco']
        )
        execute_sql(query, params)

    except UniqueViolation as e:
        return jsonify({"erro": "CPF já cadastrado!"}), 400
    except Exception as e:
        return jsonify({"erro": f"Erro ao cadastrar tutor: {str(e)}"}), 500

    return jsonify({"mensagem": "Tutor cadastrado com sucesso!"}), 201


# Rota para editar um tutor
@tutores_bp.route('/api/tutores/<int:id_tutor>', methods=['PUT'])
def atualizar_tutor(id_tutor):
    """ Atualiza os dados de um tutor """
    dados = request.json

    query = """
        UPDATE Tutor SET nome = %s, data_nascimento = %s, telefone = %s, endereco = %s
        WHERE id_tutor = %s
    """
    execute_sql(query, (dados["nome"], dados["nascimento"], dados["telefone"], dados["endereco"], id_tutor))

    return jsonify({"mensagem": "Tutor atualizado com sucesso!"}), 200


# Rotas para renderizar páginas HTML
@tutores_bp.route('/tutores')
def tutores_page():
    """ Renderiza a página de tutores """
    return render_template('tela_cadastros/tutores.html')


@tutores_bp.route('/cadastro_tutor_page')
def cadastro_tutor_page():
    return render_template('tela_cadastros/cadastro_tutores.html')
