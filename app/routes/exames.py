from flask import Blueprint, request, jsonify
from app.models.exame import Exame
from app.validators.exame_validator import ExameValidator
from app.init import db
from datetime import datetime

exames_bp = Blueprint('exames', __name__)

@exames_bp.route('/exames', methods=['POST'])
def criar_exame():
    data = request.get_json()

    # Validar dados
    valido, mensagem = ExameValidator.validar_criar_exame(data)
    if not valido:
        return jsonify({"erro": mensagem}), 400

    # Converter data_exame para o formato de data
    data_exame = datetime.strptime(data['data_exame'], '%d/%m/%Y').date()

    # Criar exame
    novo_exame = Exame(
        id_consulta=data['id_consulta'],
        id_animal=data['id_animal'],
        id_tipo_exame=data['id_tipo_exame'],
        resultado=data.get('resultado'),
        data_exame=data_exame,
        observacoes=data.get('observacoes')
    )
    db.session.add(novo_exame)
    db.session.commit()
    return jsonify({"mensagem": "Exame criado com sucesso!", "id_exame": novo_exame.id_exame}), 201