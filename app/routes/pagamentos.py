from flask import Blueprint, request, jsonify
from app.models.pagamento import Pagamento
from app.validators.pagamento_validator import PagamentoValidator
from app.init import db
from datetime import datetime

pagamentos_bp = Blueprint('pagamentos', __name__)

@pagamentos_bp.route('/pagamentos', methods=['POST'])
def criar_pagamento():
    data = request.get_json()

    # Validar dados
    valido, mensagem = PagamentoValidator.validar_criar_pagamento(data)
    if not valido:
        return jsonify({"erro": mensagem}), 400

    # Converter data_pagamento para o formato de data
    data_pagamento = datetime.strptime(data['data_pagamento'], '%d/%m/%Y').date()

    # Criar pagamento
    novo_pagamento = Pagamento(
        id_consulta=data['id_consulta'],
        valor=data['valor'],
        data_pagamento=data_pagamento,
        id_meio_pagamento=data['id_meio_pagamento']
    )
    db.session.add(novo_pagamento)
    db.session.commit()
    return jsonify({"mensagem": "Pagamento criado com sucesso!", "id_pagamento": novo_pagamento.id_pagamento}), 201