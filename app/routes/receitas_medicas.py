from flask import Blueprint, request, jsonify
from app.models.receita_medica import ReceitaMedica
from app.validators.receita_medica_validator import ReceitaMedicaValidator
from app.init import db
from datetime import datetime

receitas_medicas_bp = Blueprint('receitas_medicas', __name__)

@receitas_medicas_bp.route('/receitas_medicas', methods=['POST'])
def criar_receita_medica():
    data = request.get_json()

    # Validar dados
    valido, mensagem = ReceitaMedicaValidator.validar_criar_receita_medica(data)
    if not valido:
        return jsonify({"erro": mensagem}), 400

    # Converter data para o formato de data
    data_receita = datetime.strptime(data['data'], '%d/%m/%Y').date()

    # Criar receita médica
    nova_receita_medica = ReceitaMedica(
        id_consulta=data['id_consulta'],
        id_tratamento=data['id_tratamento'],
        id_veterinario=data['id_veterinario'],
        data=data_receita,
        observacoes=data.get('observacoes')
    )
    db.session.add(nova_receita_medica)
    db.session.commit()
    return jsonify({"mensagem": "Receita médica criada com sucesso!", "id_receita": nova_receita_medica.id_receita}), 201