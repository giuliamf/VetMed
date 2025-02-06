from flask import Blueprint, request, jsonify
from app.models.tratamento import Tratamento
from app.validators.tratamento_validator import TratamentoValidator
from app.init import db
from datetime import datetime

tratamentos_bp = Blueprint('tratamentos', __name__)

@tratamentos_bp.route('/tratamentos', methods=['POST'])
def criar_tratamento():
    data = request.get_json()

    # Validar dados
    valido, mensagem = TratamentoValidator.validar_criar_tratamento(data)
    if not valido:
        return jsonify({"erro": mensagem}), 400

    # Converter data_inicio para o formato de data completo (adicionando o ano atual)
    data_inicio = datetime.strptime(data['data_inicio'], '%d/%m').date().replace(year=datetime.now().year)

    # Criar tratamento
    novo_tratamento = Tratamento(
        id_consulta=data['id_consulta'],
        tipo_tratamento=data['tipo_tratamento'],
        descricao=data['descricao'],
        duracao_estimada=data['duracao_estimada'],
        data_inicio=data_inicio
    )
    db.session.add(novo_tratamento)
    db.session.commit()
    return jsonify({"mensagem": "Tratamento criado com sucesso!", "id_tratamento": novo_tratamento.id_tratamento}), 201