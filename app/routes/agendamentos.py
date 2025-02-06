from flask import Flask, request, jsonify, Blueprint
from app.models.agendamento import Agendamento
from app.validators.agendamento_validator import AgendamentoValidator
from app.init import db
from datetime import datetime

agendamentos_bp = Blueprint('agendamentos', __name__)

app = Flask(__name__)

from flask import request, jsonify
from datetime import datetime

@app.route('/agendamentos', methods=['POST'])
def criar_agendamento_route():
    try:
        # Obter os dados do corpo da requisição
        dados = request.json

        # Validar os dados antes de criar o agendamento
        valido, mensagem = AgendamentoValidator.validar_criar_agendamento(dados)
        if not valido:
            return jsonify({"erro": mensagem}), 400  # Bad Request

        # Converter a data e hora para os tipos corretos
        data_agendamento = datetime.strptime(dados['data'], '%d/%m/%Y').date()
        hora_agendamento = datetime.strptime(dados['hora'], '%H:%M').time()

        # Criar o agendamento no banco de dados
        id_agendamento = criar_agendamento(
            dados['id_tutor'],
            dados['id_animal'],
            data_agendamento,
            hora_agendamento,
            dados['id_status']
        )

        # Retornar a resposta com o ID do agendamento criado
        return jsonify({"id_agendamento": id_agendamento}), 201  # Created

    except ValueError as e:
        # Capturar erros de validação ou conversão de dados
        return jsonify({"erro": str(e)}), 400  # Bad Request

    except Exception as e:
        # Capturar outros erros inesperados (ex: erros no banco de dados)
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500  # Internal Server Error

@app.route('/agendamentos/<int:id_agendamento>', methods=['GET'])
def buscar_agendamento_route(id_agendamento):
    agendamento = buscar_agendamento_por_id(id_agendamento)
    if agendamento:
        return jsonify({
            "id_agendamento": agendamento.id_agendamento,
            "id_tutor": agendamento.id_tutor,
            "id_animal": agendamento.id_animal,
            "data": agendamento.data,
            "hora": agendamento.hora,
            "id_status": agendamento.id_status
        })
    return jsonify({"mensagem": "Agendamento não encontrado"}), 404

from flask import request, jsonify
from datetime import datetime

from flask import request, jsonify
from datetime import datetime

@app.route('/agendamentos/<int:id_agendamento>', methods=['PUT'])
def atualizar_agendamento_route(id_agendamento):
    try:
        # Obter os dados do corpo da requisição
        dados = request.json

        # Validar os dados antes de atualizar o agendamento
        valido, mensagem = AgendamentoValidator.validar_atualizar_agendamento(dados)
        if not valido:
            return jsonify({"erro": mensagem}), 400  # Bad Request

        # Converter a data e hora para os tipos corretos, se presentes
        if 'data' in dados:
            dados['data'] = datetime.strptime(dados['data'], '%d/%m/%Y').date()
        if 'hora' in dados:
            dados['hora'] = datetime.strptime(dados['hora'], '%H:%M').time()

        # Atualizar o agendamento no banco de dados
        atualizar_agendamento(id_agendamento, **dados)

        # Retornar a resposta de sucesso
        return jsonify({"mensagem": "Agendamento atualizado com sucesso"}), 200  # OK

    except ValueError as e:
        # Capturar erros de validação ou conversão de dados
        return jsonify({"erro": str(e)}), 400  # Bad Request

    except Exception as e:
        # Capturar outros erros inesperados (ex: erros no banco de dados)
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500  # Internal Server Error

@app.route('/agendamentos/<int:id_agendamento>', methods=['DELETE'])
def deletar_agendamento_route(id_agendamento):
    deletar_agendamento(id_agendamento)
    return jsonify({"mensagem": "Agendamento deletado com sucesso"}), 200

if __name__ == '__main__':
    app.run(debug=True)