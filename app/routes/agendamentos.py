from flask import Blueprint, request, jsonify
from app.models.agendamento import Agendamento
from app.validators.agendamento_validator import AgendamentoValidator
from app import db
from datetime import datetime

agendamentos_bp = Blueprint('agendamentos', __name__)

@agendamentos_bp.route('/agendamentos', methods=['POST'])
def criar_agendamento():
    data = request.get_json()

    # Validar dados
    valido, mensagem = AgendamentoValidator.validar_criar_agendamento(data)
    if not valido:
        return jsonify({"erro": mensagem}), 400

    # Converter data e hora para os formatos corretos
    data_agendamento = datetime.strptime(data['data'], '%d/%m/%Y').date()
    hora_agendamento = datetime.strptime(data['hora'], '%H:%M').time()

    # Criar agendamento
    novo_agendamento = Agendamento(
        id_tutor=data['id_tutor'],
        id_animal=data['id_animal'],
        data=data_agendamento,
        hora=hora_agendamento,
        id_status=data['id_status']
    )
    db.session.add(novo_agendamento)
    db.session.commit()
    return jsonify({"mensagem": "Agendamento criado com sucesso!", "id_agendamento": novo_agendamento.id_agendamento}), 201