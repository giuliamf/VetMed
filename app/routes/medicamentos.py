from flask import Blueprint, request, jsonify
from app.models.medicamento import Medicamento
from app.validators.medicamento_validator import MedicamentoValidator
from app.init import db

medicamentos_bp = Blueprint('medicamentos', __name__)

@medicamentos_bp.route('/medicamentos', methods=['POST'])
def criar_medicamento():
    data = request.get_json()

    # Validar dados
    valido, mensagem = MedicamentoValidator.validar_criar_medicamento(data)
    if not valido:
        return jsonify({"erro": mensagem}), 400

    # Criar medicamento
    novo_medicamento = Medicamento(
        nome=data['nome'],
        descricao=data['descricao'],
        quantidade=data['quantidade'],
        tipo=data['tipo'],
        uso=data['uso']
    )
    db.session.add(novo_medicamento)
    db.session.commit()
    return jsonify({"mensagem": "Medicamento criado com sucesso!", "id_medicamento": novo_medicamento.id_medicamento}), 201