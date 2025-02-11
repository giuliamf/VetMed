from flask import Blueprint, request, jsonify, render_template
from app.database import execute_sql

tutores_bp = Blueprint('tutores', __name__)


@tutores_bp.route('/tutores')
def tutores_page():
    """ Renderiza a página de tutores """
    return render_template('tela_cadastros/tutores.html')


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


@tutores_bp.route('/cadastro_tutor', methods=['GET', 'POST'])
def cadastro_tutor():
    """ Cadastro de novo tutor """
    if request.method == 'POST':
        dados = request.json

        # Verifica se o CPF já está cadastrado
        cpf_existente = execute_sql("SELECT id_tutor FROM Tutor WHERE cpf = %s", (dados["cpf"],), fetch_one=True)
        if cpf_existente:
            return jsonify({"erro": "CPF já cadastrado!"}), 400

        query = """
            INSERT INTO Tutor (cpf, nome, data_nascimento, telefone, endereco)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_tutor
        """
        id_tutor = execute_sql(query,
                               (dados["cpf"], dados["nome"], dados["nascimento"], dados["telefone"], dados["endereco"]),
                               fetch_one=True)

        return jsonify({"mensagem": "Tutor cadastrado com sucesso!", "id_tutor": id_tutor[0]}), 201

    return render_template('tela_cadastros/cadastro_tutores.html')


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
