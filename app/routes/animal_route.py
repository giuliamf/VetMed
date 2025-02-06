from flask import Blueprint, request, jsonify
from app.models.animal import Animal
from app.validators.animal_validator import AnimalValidator
from app import db

animais_bp = Blueprint('animais', __name__)


@animais_bp.route('/animais', methods=['POST'])
def criar_animal():
    """
    Rota para criar um novo animal no banco de dados.
    """
    data = request.get_json()

    # Validar dados
    valido, mensagem = AnimalValidator.validar_criar_animal(data)
    if not valido:
        return jsonify({"erro": mensagem}), 400

    # Criar animal
    novo_animal = Animal(
        id_tutor=data['id_tutor'],
        nome=data['nome'],
        especie=data['especie'],
        raca=data.get('raca'),
        ano_nascimento=data.get('ano_nascimento'),
        sexo=data.get('sexo'),
        peso=data.get('peso'),
        cor=data['cor']
    )

    db.session.add(novo_animal)
    db.session.commit()

    return jsonify({"mensagem": "Animal criado com sucesso!", "id_animal": novo_animal.id_animal}), 201


@animais_bp.route('/animais/<int:id_animal>', methods=['GET'])
def obter_animal(id_animal):
    animal = Animal.query.get_or_404(id_animal)
    return jsonify({
        "id_animal": animal.id_animal,
        "id_tutor": animal.id_tutor,
        "nome": animal.nome,
        "especie": animal.especie,
        "raca": animal.raca,
        "ano_nascimento": animal.ano_nascimento,
        "sexo": animal.sexo,
        "peso": animal.peso,
        "cor": animal.cor
    })

@animais_bp.route('/animais/<int:id_animal>', methods=['PUT'])
def atualizar_animal(id_animal):
    animal = Animal.query.get_or_404(id_animal)
    data = request.get_json()
    
    if 'nome' in data:
        animal.nome = data['nome']
    if 'especie' in data:
        animal.especie = data['especie']
    if 'raca' in data:
        animal.raca = data['raca']
    if 'ano_nascimento' in data:
        animal.ano_nascimento = data['ano_nascimento']
    if 'sexo' in data:
        animal.sexo = data['sexo']
    if 'peso' in data:
        animal.peso = data['peso']
    if 'cor' in data:
        animal.cor = data['cor']
    
    db.session.commit()
    return jsonify({"mensagem": "Animal atualizado com sucesso!"}), 200

@animais_bp.route('/animais/<int:id_animal>', methods=['DELETE'])
def excluir_animal(id_animal):
    animal = Animal.query.get_or_404(id_animal)
    db.session.delete(animal)
    db.session.commit()
    return jsonify({"mensagem": "Animal excluído com sucesso!"}), 200
