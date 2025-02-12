from flask import Blueprint, request, jsonify, render_template
from app.database import execute_sql

from app.utils.funcoes_com_cpf import formatar_cpf, nome_tutor_id
from app.utils.buscas_bd import id_tutor_cpf


animais_bp = Blueprint('pacientes', __name__)


@animais_bp.route('/api/pacientes', methods=['GET'])
def get_pacientes():
    """ Retorna a lista de pacientes do banco de dados """
    try:
        query = "SELECT * FROM Animal ORDER BY id_animal ASC"
        pacientes = execute_sql(query, fetch_all=True)

        pacientes_lista = [
            {
                "id_animal": p[0],
                "id_tutor": p[1],
                "nome": p[2],
                "especie": p[3],
                "raca": p[4],
                "nascimento": str(p[5]),
                "sexo": p[6],
                "peso": float(p[7]),
                "cor": p[8]
            }
            for p in pacientes
        ]

        # incluir o nome do tutor na lista
        for paciente in pacientes_lista:
            paciente["nome_tutor"] = nome_tutor_id(paciente["id_tutor"])

        return jsonify(pacientes_lista), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar pacientes: {str(e)}"}), 500


@animais_bp.route('/cadastro_paciente', methods=['POST'])
def criar_paciente():
    """ Cria um novo paciente verificando o tutor pelo CPF. """
    if not request.json:
        return jsonify({"erro": "Nenhum dado JSON foi recebido"}), 400

    data = request.json
    cpf_tutor = formatar_cpf(data.get("tutor"))

    # Achar o id do tutor pelo cpf
    id_tutor = id_tutor_cpf(cpf_tutor)
    if not id_tutor:
        return jsonify({"erro": "Tutor não encontrado! Cadastre o tutor antes"}), 404

    if not all(key in data for key in ["nome", "especie", "raca", "nascimento", "sexo", "peso", "cor"]):
        return jsonify({"erro": "Campos obrigatórios ausentes!"}), 400

    if not all(data.values()):
        return jsonify({"erro": "Preencha todos os campos!"}), 400

    try:
        query_paciente = """
            INSERT INTO Animal (id_tutor, nome, especie, raca, nascimento, sexo, peso, cor)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            id_tutor,
            data.get("nome"),
            data.get("especie"),
            data.get("raca"),
            data.get("nascimento"),
            data.get("sexo"),
            data.get("peso"),
            data.get("cor")
        )
        execute_sql(query_paciente, params)
        return jsonify({"mensagem": "Paciente cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"erro": f"Erro ao cadastrar paciente: {str(e)}"}), 500


@animais_bp.route('/api/pacientes/<int:id_animal>', methods=['GET', 'PUT'])
def editar_paciente(id_animal):

    if request.method == 'GET':
        # Buscar paciente pelo ID no banco de dados
        query = "SELECT * FROM Animal WHERE id_animal = %s"
        resultado = execute_sql(query, (id_animal,), fetch_one=True)

        if not resultado:
            return jsonify({"erro": "Paciente não encontrado"}), 404

        paciente = {
            "id_animal": resultado[0],
            "id_tutor": resultado[1],
            "nome": resultado[2],
            "especie": resultado[3],
            "raca:": resultado[4],
            "nascimento": str(resultado[5]),
            "sexo": resultado[6],
            "peso": float(resultado[7]),
            "cor": resultado[8]
        }
        return jsonify(paciente), 200

    """ Atualiza os dados de um paciente, garantindo que o tutor informado já esteja cadastrado. """
    if request.method == 'PUT':
        dados = request.json

        cpf = dados["tutor"]
        cpf_formatado = formatar_cpf(cpf)

        # Achar o id do tutor através do cpf
        id_tutor = id_tutor_cpf(cpf_formatado)

        if not id_tutor:    # Se não encontrar o tutor, retornar erro
            return jsonify({"erro": "Tutor não encontrado! Cadastre o tutor antes"}), 404

        query = """
                    UPDATE Animal SET id_tutor = %s, nome = %s, especie = %s, raca = %s, nascimento = %s, sexo = %s, peso = %s, cor = %s
                    WHERE id_animal = %s
                """
        params = (
            id_tutor,
            dados["nome"],
            dados["especie"],
            dados["raca"],
            dados["nascimento"],
            dados["sexo"],
            dados["peso"],
            dados["cor"],
            id_animal
        )

        try:
            execute_sql(query, params)
            return jsonify({"mensagem": "Paciente atualizado com sucesso!"}), 200
        except Exception as e:
            return jsonify({"erro": f"Erro ao atualizar paciente: {str(e)}"}), 500


# Rotas para renderizar páginas HTML
@animais_bp.route('/pacientes')
def pacientes_page():
    return render_template('tela_cadastros/pacientes.html')


@animais_bp.route('/cadastro_paciente_page')
def cadastro_paciente_page():
    return render_template('tela_cadastros/cadastro_pacientes.html')
