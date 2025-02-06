from flask import Blueprint, request, jsonify
from app.models.receita_medicamento import ReceitaMedicamento
from app.validators.receita_medicamento_validator import ReceitaMedicamentoValidator
from app.init import db

receita_medicamento_bp = Blueprint('receita_medicamento', __name__)

@receita_medicamento_bp.route('/receita_medicamento', methods=['POST'])
def criar_receita_medicamento():
    data = request.get_json()

    # Validar dados
    valido, mensagem = ReceitaMedicamentoValidator.validar_criar_receita_medicamento(data)
    if not valido:
        return jsonify({"erro": mensagem}), 400

    # Criar registro na tabela Receita_Medicamento
    novo_receita_medicamento = ReceitaMedicamento(
        id_receita=data['id_receita'],
        id_medicamento=data['id_medicamento'],
        quantidade=data['quantidade'],
        tipo_quantidade=data['tipo_quantidade'],
        frequencia=data['frequencia'],
        duracao=data['duracao']
    )
    db.session.add(novo_receita_medicamento)
    db.session.commit()
    return jsonify({"mensagem": "Registro criado com sucesso!"}), 201