from flask import Blueprint, request, jsonify, render_template
from app.database import execute_sql

from app.utils.funcoes_com_cpf import formatar_cpf, nome_tutor_id, cpf_igual, cpf_existe
from app.utils.buscas_bd import buscar_id_tutor_por_cpf, buscar_cpf_tutor_por_id, buscar_id_tutor_por_id_animal

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
    id_tutor = buscar_id_tutor_por_cpf(cpf_tutor)
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
    print(f"Buscando paciente com ID: {id_animal}")

    if request.method == 'GET':
        # Buscar paciente pelo ID no banco de dados
        query = "SELECT * FROM Animal WHERE id_animal = %s"
        resultado = execute_sql(query, (id_animal,), fetch_one=True)

        if not resultado:
            print(f"Paciente com ID {id_animal} não encontrado.")
            return jsonify({"erro": "Paciente não encontrado"}), 404

        # Pegar o cpf do tutor a partir do id
        cpf_tutor = formatar_cpf(buscar_cpf_tutor_por_id(resultado[1]))

        paciente = {
            "id_animal": resultado[0],
            "id_tutor": resultado[1],
            "nome": resultado[2],
            "especie": resultado[3],
            "raca": resultado[4],
            "nascimento": resultado[5],
            "sexo": resultado[6],
            "peso": resultado[7],
            "cor": resultado[8],
            "tutor": cpf_tutor
        }
        return jsonify(paciente), 200

    """ Atualiza os dados de um paciente, garantindo que o tutor informado já esteja cadastrado. """
    if request.method == 'PUT':
        dados = request.json

        cpf = dados["tutor"]
        cpf_formatado = formatar_cpf(cpf)

        # Pegar o id "original" do tutor a partir do id do animal
        id_tutor_original = buscar_id_tutor_por_id_animal(id_animal)

        # Verificar se o usuário tentou mudar o cpf
        if not cpf_igual(cpf_formatado, id_tutor_original):
            # Verificar se o novo cpf já está cadastrado
            cpf_invalido = cpf_existe(cpf_formatado)
            if cpf_invalido:    # Se o cpf já existe, retornar erro
                return cpf_invalido

        # Achar o id do tutor através do cpf
        id_tutor = buscar_id_tutor_por_cpf(cpf_formatado)

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
            return jsonify({"erro": f"Erro ao atualizar paciente 1: {str(e)}"}), 500


@animais_bp.route('/api/pacientes/<int:id_animal>', methods=['DELETE'])
def excluir_paciente(id_animal):
    """ Rota para excluir um paciente """
    try:
        query = "DELETE FROM Animal WHERE id_animal = %s"
        execute_sql(query, (id_animal,))
        return jsonify({"mensagem": "Paciente excluído com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao excluir paciente: {str(e)}"}), 500


# Rotas para renderizar páginas HTML
@animais_bp.route('/pacientes')
def pacientes_page():
    return render_template('tela_cadastros/pacientes.html')


@animais_bp.route('/cadastro_paciente_page')
def cadastro_paciente_page():
    return render_template('tela_cadastros/cadastro_pacientes.html')
