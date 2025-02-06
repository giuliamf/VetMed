from flask import Blueprint, request, jsonify
from app.models.consulta import Consulta
from app.validators.horario_validator import HorarioValidator
from app.init import db

consultas_bp = Blueprint('consultas', __name__)

@consultas_bp.route('/consultas', methods=['POST'])
def criar_consulta():
    data = request.get_json()

    # Validar horário
    valido, mensagem = HorarioValidator.validar_horario(data['horario'])
    if not valido:
        return jsonify({"erro": mensagem}), 400

    # Verificar conflito de horário
    valido, mensagem = HorarioValidator.verificar_conflito_horario(
        data['id_veterinario'],
        data['data'],
        data['horario']
    )
    if not valido:
        return jsonify({"erro": mensagem}), 400

    # Criar consulta
    nova_consulta = Consulta(
        id_animal=data['id_animal'],
        id_veterinario=data['id_veterinario'],
        data=data['data'],
        horario=data['horario'],
        id_tipo=data['id_tipo']
    )
    db.session.add(nova_consulta)
    db.session.commit()
    return jsonify({"mensagem": "Consulta criada com sucesso!", "id_consulta": nova_consulta.id_consulta}), 201