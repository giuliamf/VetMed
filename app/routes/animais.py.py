from flask import Blueprint, request, jsonify
from app.models.animal import Animal
from app import db

animais_bp = Blueprint('animais', __name__)

@animais_bp.route('/animais', methods=['POST'])
def criar_animal():
    data = request.get_json()
    novo_animal = Animal(
        id_tutor=data['id_tutor'],
        nome=data['nome'],
        especie=data['especie'],
        raca=data.get('raca'),
        ano_nascimento=data.get('ano_nascimento'),
        sexo=data.get('sexo'),
        peso=data.get('peso'),
        cor=data.get('cor')
    )
    db.session.add(novo_animal)
    db.session.commit()
    return jsonify({"mensagem": "Animal criado com sucesso!", "id_animal": novo_animal.id_animal}), 201

@animais_bp.route('/animais/<int:id_animal>', methods=['PUT'])
def atualizar_animal(id_animal):
    animal = Animal.query.get_or_404(id_animal)
    data = request.get_json()
    
    # Atualiza apenas os campos fornecidos
    if 'nome' in data:
        animal.nome = data['nome']
    if 'ano_nascimento' in data:
        animal.ano_nascimento = data['ano_nascimento']
    # Repita para outros campos...
    
    db.session.commit()
    return jsonify({"mensagem": "Animal atualizado com sucesso!"}), 200

@animais_bp.route('/animais/<int:id_animal>', methods=['DELETE'])
def excluir_animal(id_animal):
    animal = Animal.query.get_or_404(id_animal)
    db.session.delete(animal)
    db.session.commit()
    return jsonify({"mensagem": "Animal excluído com sucesso!"}), 200
