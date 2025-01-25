from flask import Blueprint, request, jsonify
from app.models.tutor import Tutor
from app.validators.tutor_validator import TutorValidator
from app.utils.cpf_generator import gerar_cpf
from app import db


tutores_bp = Blueprint('tutores', __name__)

@tutores_bp.route('/tutores', methods=['POST'])
def criar_tutor():
    data = request.get_json()

    # Validar CPF verificar uso junto ao gerar CPF
    if 'id_tutor' in data:
        valido, mensagem = validar_cpf(data['id_tutor'])
        if not valido:
            return jsonify({"erro": mensagem}), 400
    
    # Gerar CPF automaticamente se não for fornecido validar uso do junto ao Validar CPF
    if 'id_tutor' not in data:
        data['id_tutor'] = gerar_cpf()
        
    
    # Validar dados
    valido, mensagem = TutorValidator.validar_criar_tutor(data)
    if not valido:
        return jsonify({"erro": mensagem}), 400

    # Criar tutor
    novo_tutor = Tutor(
        id_tutor=data['id_tutor'],
        nome=data['nome'],
        data_nascimento=data['data_nascimento'],
        telefone=data['telefone'],
        endereço=data['endereço'],
        email=data['email']
    )
    db.session.add(novo_tutor)
    db.session.commit()
    return jsonify({"mensagem": "Tutor criado com sucesso!", "id_tutor": novo_tutor.id_tutor}), 201

@tutores_bp.route('/tutores/<int:id_tutor>', methods=['GET'])
def obter_tutor(id_tutor):
    tutor = Tutor.query.get_or_404(id_tutor)
    return jsonify({
        "id_tutor": tutor.id_tutor,
        "nome": tutor.nome,
        "data_nascimento": tutor.data_nascimento,
        "telefone": tutor.telefone,
        "endereço": tutor.endereço,
        "email": tutor.email
    })

@tutores_bp.route('/tutores/<int:id_tutor>', methods=['PUT'])
def atualizar_tutor(id_tutor):
    tutor = Tutor.query.get_or_404(id_tutor)
    data = request.get_json()
    
    if 'nome' in data:
        tutor.nome = data['nome']
    if 'data_nascimento' in data:
        tutor.data_nascimento = data['data_nascimento']
    if 'telefone' in data:
        tutor.telefone = data['telefone']
    if 'endereço' in data:
        tutor.endereço = data['endereço']
    if 'email' in data:
        tutor.email = data['email']
    
    db.session.commit()
    return jsonify({"mensagem": "Tutor atualizado com sucesso!"}), 200

@tutores_bp.route('/tutores/<int:id_tutor>', methods=['DELETE'])
def excluir_tutor(id_tutor):
    tutor = Tutor.query.get_or_404(id_tutor)
    db.session.delete(tutor)
    db.session.commit()
    return jsonify({"mensagem": "Tutor excluído com sucesso!"}), 200