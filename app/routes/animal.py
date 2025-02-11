from flask import Blueprint, request, jsonify
from app.models.animal import Animal

animais_bp = Blueprint('animais', __name__)


@animais_bp.route('/api/pacientes', methods=['GET'])
def listar_pacientes():
    """ Retorna a lista de pacientes com o nome do tutor. """
    try:
        pacientes = Animal.buscar_todos_animais()
        return jsonify(pacientes), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar pacientes: {str(e)}"}), 500


@animais_bp.route('/api/pacientes', methods=['POST'])
def criar_paciente():
    """ Cria um novo paciente verificando o tutor pelo CPF. """
    try:
        dados = request.json
        id_animal = Animal.criar_animal(dados)

        if id_animal:
            return jsonify({"status": "success", "id_animal": id_animal}), 201
        return jsonify({"erro": "Erro ao criar paciente"}), 400

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500


@animais_bp.route('/api/pacientes/<int:id_animal>', methods=['GET'])
def obter_paciente(id_animal):
    """ Retorna os detalhes de um paciente pelo ID. """
    paciente = Animal.buscar_animal_por_id(id_animal)
    if paciente:
        return jsonify(paciente), 200
    return jsonify({"erro": "Paciente não encontrado"}), 404


@animais_bp.route('/api/pacientes/<int:id_animal>', methods=['PUT'])
def atualizar_paciente(id_animal):
    """ Atualiza os dados de um paciente, garantindo que o tutor informado já esteja cadastrado. """
    try:
        dados = request.json
        Animal.atualizar_animal(id_animal, dados)

        return jsonify({"mensagem": "Paciente atualizado com sucesso"}), 200  # OK

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400  # Bad Request

    except Exception as e:
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500  # Internal Server Error
