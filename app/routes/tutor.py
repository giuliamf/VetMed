from flask import Blueprint, request, jsonify, render_template
from app.database import execute_sql

from app.utils.funcoes_com_cpf import cpf_existe, cpf_igual, formatar_cpf

tutores_bp = Blueprint('tutores', __name__)


# Rota para retornar a lista de tutores
@tutores_bp.route('/api/tutores', methods=['GET'])
def get_tutores():
    """ Retorna a lista de tutores do banco de dados """
    try:
        query = "SELECT * FROM Tutor ORDER BY id_tutor ASC"
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

        return jsonify(tutores_lista), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar tutores: {str(e)}"}), 500


# Rota para cadastrar um tutor
@tutores_bp.route('/cadastro_tutor', methods=['POST'])
def cadastro_tutor():
    """ Cadastro de novo tutor """
    if not request.json:
        return jsonify({"erro": "Nenhum dado JSON foi recebido"}), 400

    data = request.json
    cpf = formatar_cpf(data.get("cpf"))

    # Verifica se o CPF já existe no banco
    cpf_invalido = cpf_existe(cpf)
    if cpf_invalido:        # Se cpf não for None, significa que ele foi encontrado
        return jsonify({"erro": "CPF já cadastrado!"}), 400

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
        return jsonify({"mensagem": "Tutor cadastrado com sucesso!"}), 201

    except Exception as e:
        return jsonify({"erro": f"Erro ao cadastrar tutor: {str(e)}"}), 500


# Rota para editar um tutor
@tutores_bp.route('/api/tutores/<int:id_tutor>', methods=['GET', 'PUT'])
def editar_tutor(id_tutor):
    if request.method == 'GET':
        # Buscar tutor pelo ID no banco de dados
        query = "SELECT * FROM Tutor WHERE id_tutor = %s"
        resultado = execute_sql(query, (id_tutor,), fetch_one=True)

        if not resultado:
            return jsonify({"erro": "Tutor não encontrado"}), 404

        cpf_formatado = formatar_cpf(resultado[1])
        tutor = {
            "cpf": cpf_formatado,
            "nome": resultado[2],
            "nascimento": resultado[3],
            "telefone": resultado[4],
            "endereco": resultado[5]
        }

        return jsonify(tutor), 200

    """ Atualiza os dados de um tutor """
    if request.method == 'PUT':
        # Código de atualização já existente
        dados = request.json
        cpf_formatado = formatar_cpf(dados['cpf'])

        # Verifica se o CPF foi alterado e se foi, se ele já existe no banco, se existir, retorna um erro
        if not cpf_igual(cpf_formatado, id_tutor):
            cpf_invalido = cpf_existe(cpf_formatado)
            if cpf_invalido:
                return cpf_invalido

        query = """
                    UPDATE Tutor SET cpf = %s, nome = %s, data_nascimento = %s, telefone = %s, endereco = %s
                    WHERE id_tutor = %s
                """

        params = (
            cpf_formatado,
            dados["nome"],
            dados["nascimento"],
            dados["telefone"],
            dados["endereco"],
            id_tutor
        )
        try:
            execute_sql(query, params)
            return jsonify({"mensagem": "Tutor atualizado com sucesso!"}), 200
        except Exception as e:
            return jsonify({"erro": f"Erro ao atualizar tutor: {str(e)}"}), 500


@tutores_bp.route('/api/tutores/<int:id_tutor>', methods=['DELETE'])
def excluir_tutor(id_tutor):
    """ Rota para excluir um tutor """
    try:
        query = "DELETE FROM Tutor WHERE id_tutor = %s"
        execute_sql(query, (id_tutor,))
        return jsonify({"mensagem": "Tutor excluído com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao excluir tutor: {str(e)}"}), 500


# Rotas para renderizar páginas HTML
@tutores_bp.route('/tutores')
def tutores_page():
    """ Renderiza a página de tutores """
    return render_template('tela_cadastros/tutores.html')


@tutores_bp.route('/cadastro_tutor_page')
def cadastro_tutor_page():
    return render_template('tela_cadastros/cadastro_tutores.html')
