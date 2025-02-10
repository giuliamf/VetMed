from flask import Blueprint, request, jsonify
from app.models.animal import Animal
from app.validators.animal_validator import AnimalValidator
<<<<<<< Updated upstream:app/routes/animal_route.py
from app import db
=======
>>>>>>> Stashed changes:app/routes/animais.py

animais_bp = Blueprint('animais', __name__)


@animais_bp.route('/animais', methods=['POST'])
<<<<<<< Updated upstream:app/routes/animal_route.py
def criar_animal():
    """
    Rota para criar um novo animal no banco de dados.
    """
    data = request.get_json()
=======
def criar_animal_route():
    try:
        # Obter os dados do corpo da requisição
        dados = request.json
>>>>>>> Stashed changes:app/routes/animais.py

        # Validar os dados antes de criar o animal
        valido, mensagem = AnimalValidator.validar_criar_animal(dados)
        if not valido:
            return jsonify({"erro": mensagem}), 400  # Bad Request

<<<<<<< Updated upstream:app/routes/animal_route.py
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
=======
        # Criar o animal no banco de dados
        id_animal = Animal.criar_animal(dados)

        # Retornar a resposta com o ID do animal criado
        return jsonify({"id_animal": id_animal}), 201  # Created

    except ValueError as e:
        # Capturar erros de validação ou conversão de dados
        return jsonify({"erro": str(e)}), 400  # Bad Request

    except Exception as e:
        # Capturar outros erros inesperados (ex: erros no banco de dados)
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500  # Internal Server Error
>>>>>>> Stashed changes:app/routes/animais.py


@animais_bp.route('/animais/<int:id_animal>', methods=['GET'])
def obter_animal_route(id_animal):
    animal = Animal.buscar_animal_por_id(id_animal)
    if animal:
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
    return jsonify({"mensagem": "Animal não encontrado"}), 404


@animais_bp.route('/animais/<int:id_animal>', methods=['PUT'])
def atualizar_animal_route(id_animal):
    try:
        # Obter os dados do corpo da requisição
        dados = request.json

        # Validar os dados antes de atualizar o animal
        valido, mensagem = AnimalValidator.validar_atualizar_animal(dados)
        if not valido:
            return jsonify({"erro": mensagem}), 400  # Bad Request

        # Atualizar o animal no banco de dados
        Animal.atualizar_animal(id_animal, **dados)

        # Retornar a resposta de sucesso
        return jsonify({"mensagem": "Animal atualizado com sucesso"}), 200  # OK

    except ValueError as e:
        # Capturar erros de validação ou conversão de dados
        return jsonify({"erro": str(e)}), 400  # Bad Request

    except Exception as e:
        # Capturar outros erros inesperados (ex: erros no banco de dados)
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500  # Internal Server Error


@animais_bp.route('/animais/<int:id_animal>', methods=['DELETE'])
def excluir_animal_route(id_animal):
    try:
        Animal.deletar_animal(id_animal)
        return jsonify({"mensagem": "Animal excluído com sucesso!"}), 200  # OK
    except Exception as e:
        # Capturar outros erros inesperados (ex: erros no banco de dados)
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500  # Internal Server Error