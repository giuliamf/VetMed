from flask import Flask, request, jsonify, Blueprint
from app.models.agendamento import Agendamento
from app.validators.agendamento_validator import AgendamentoValidator
from app import db
from datetime import datetime

agendamento_bp = Blueprint('agendamentos', __name__)

@app.route('/agendamento', methods=['POST'])
def criar_agendamento_route():
    try:
        # Obter os dados do corpo da requisição
        dados = request.json

        # Validar os dados antes de criar o agendamento
        valido, mensagem = AgendamentoValidator.validar_criar_agendamento(dados)
        if not valido:
            return jsonify({"erro": mensagem}), 400  # Bad Request

        # Criar o agendamento no banco de dados
        id_agendamento = Agendamento.criar_agendamento(dados)

        # Retornar a resposta com o ID do agendamento criado
        return jsonify({"id_agendamento": id_agendamento}), 201  # Created

    except ValueError as e:
        # Capturar erros de validação ou conversão de dados
        return jsonify({"erro": str(e)}), 400  # Bad Request

    except Exception as e:
        # Capturar outros erros inesperados (ex: erros no banco de dados)
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500  # Internal Server Error

@app.route('/agendamento/<int:id_agendamento>', methods=['GET'])
def buscar_agendamento_route(id_agendamento):
    agendamento = Agendamento.buscar_agendamento_por_id(id_agendamento)
    if agendamento:
        return jsonify({
            "id_agendamento": agendamento.id_agendamento,
            "id_animal": agendamento.id_animal,
            "data": agendamento.data.strftime('%d/%m/%Y'),
            "hora": agendamento.hora.strftime('%H:%M'),
            "id_status": agendamento.id_status
        })
    return jsonify({"mensagem": "Agendamento não encontrado"}), 404

@app.route('/agendamento/<int:id_agendamento>', methods=['PUT'])
def atualizar_agendamento_route(id_agendamento):
    try:
        # Obter os dados do corpo da requisição
        dados = request.json

        # Validar os dados antes de atualizar o agendamento
        valido, mensagem = AgendamentoValidator.validar_atualizar_agendamento(dados)
        if not valido:
            return jsonify({"erro": mensagem}), 400  # Bad Request

        # Atualizar o agendamento no banco de dados
        Agendamento.atualizar_agendamento(id_agendamento, **dados)

        # Retornar a resposta de sucesso
        return jsonify({"mensagem": "Agendamento atualizado com sucesso"}), 200  # OK

    except ValueError as e:
        # Capturar erros de validação ou conversão de dados
        return jsonify({"erro": str(e)}), 400  # Bad Request

    except Exception as e:
        # Capturar outros erros inesperados (ex: erros no banco de dados)
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500  # Internal Server Error

@app.route('/agendamento/<int:id_agendamento>', methods=['DELETE'])
def deletar_agendamento_route(id_agendamento):
    try:
        Agendamento.deletar_agendamento(id_agendamento)
        return jsonify({"mensagem": "Agendamento deletado com sucesso"}), 200  # OK
    except Exception as e:
        # Capturar outros erros inesperados (ex: erros no banco de dados)
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500  # Internal Server Error

if __name__ == '__main__':
    app.run(debug=True)