from flask import Blueprint, request, jsonify
from app.models.veterinario import Veterinario
from app.validators.veterinario_validator import VeterinarioValidator
from app.utils.crmv_generator import gerar_crmv
from app import db

veterinarios_bp = Blueprint('veterinarios', __name__)

@veterinarios_bp.route('/veterinarios', methods=['POST'])
def criar_veterinario():
    data = request.get_json()

    # Gerar CRMV automaticamente
    data['crmv'] = gerar_crmv()

    # Validar dados
    valido, mensagem = VeterinarioValidator.validar_criar_veterinario(data)
    if not valido:
        return jsonify({"erro": mensagem}), 400

    # Criar veterinário
    novo_veterinario = Veterinario(
        id_veterinario=data['id_veterinario'],
        nome=data['nome'],
        telefone=data['telefone'],
        endereco=data['endereco'],
        email=data['email'],
        crmv=data['crmv']
    )
    db.session.add(novo_veterinario)
    db.session.commit()
    return jsonify({"mensagem": "Veterinário criado com sucesso!", "crmv": novo_veterinario.crmv}), 201