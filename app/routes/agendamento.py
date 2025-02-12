from flask import Blueprint, jsonify, request, render_template
from app.database import execute_sql

from app.utils.funcoes_com_cpf import formatar_cpf
from app.utils.buscas_bd import buscar_id_tutor_por_cpf

agendamentos_bp = Blueprint('agendamento', __name__)


@agendamentos_bp.route('/api/agendamentos')
def get_agendamentos():
    """ Retorna a lista de agendamentos do banco de dados """
    try:
        query = """
                SELECT a.id_agendamento, p.nome AS animal, t.nome AS tutor, s.nome AS status, 
                       a.data, a.horario
                FROM Agendamento a
                JOIN Animal p ON a.id_animal = p.id_animal
                JOIN Tutor t ON p.id_tutor = t.id_tutor
                JOIN Status_Agendamento s ON a.id_status = s.id_status
                ORDER BY a.data ASC, a.horario ASC
            """

        agendamentos = execute_sql(query, fetch_all=True)
        print(agendamentos)

        agendamentos_lista = [
            {
                "id_agendamento": a[0],
                "paciente": a[1],
                "tutor": a[2],
                "id_status": a[3],
                "status": a[4],
                "data": str(a[5]),
                "horario": a[6]
            }
            for a in agendamentos
        ]

        return jsonify(agendamentos_lista), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar agendamentos: {str(e)}"}), 500


@agendamentos_bp.route('/api/status', methods=['GET'])
def get_status():
    """ Retorna a lista de status para agendamento """
    try:
        query = "SELECT * FROM Status"
        status = execute_sql(query, fetch_all=True)

        status_lista = [
            {
                "id": s[0],
                "nome": s[1]
            }
            for s in status
        ]

        return jsonify(status_lista), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar status: {str(e)}"}), 500


@agendamentos_bp.route('/cadastro_agendamento', methods=['POST'])
def cadastro_agendamento():
    """ Cadastro de novo agendamento """
    if not request.json:
        return jsonify({"erro": "Nenhum dado JSON foi recebido"}), 400

    """
    Aqui, eu recebo do formulário: cpf do tutor (achar o id)
    id do animal
    status é cadastrado como 1 (agendado)
    data é recebida do calendário da página
    horário é recebido do select como uma string hh:mm
    """

    data = request.json

    # Dados recebidos do formulário
    cpf_tutor = data.get("cpf_tutor")
    id_animal = data.get("id_animal")
    data_agendamento = data.get("data")
    horario = data.get("horario")

    if not cpf_tutor or not id_animal or not data_agendamento or not horario:
        return jsonify({"erro": "Campos obrigatórios ausentes!"}), 400

    id_tutor = buscar_id_tutor_por_cpf(formatar_cpf(cpf_tutor))

    if not id_tutor:
        return jsonify({"erro": "Tutor não encontrado!"}), 404

    novo_agendamento = {
        "id_tutor": id_tutor,
        "id_animal": id_animal,
        "data_agendamento": data_agendamento,
        "horario": horario,
    }

    try:
        query = """
            INSERT INTO Agendamento (id_animal, id_status, data, horario)
            VALUES (%s, 1, %s, %s)
        """
        params = (
            novo_agendamento['id_animal'],
            novo_agendamento['data_agendamento'],
            novo_agendamento['horario']
        )
        execute_sql(query, params)
        return jsonify({"mensagem": "Agendamento realizado com sucesso!"}), 201

    except Exception as e:
        return jsonify({"erro": f"Erro ao cadastrar agendamento: {str(e)}"}), 500


@agendamentos_bp.route('/api/agendamentos/<int:id_agendamento>', methods=['GET', 'PUT'])
def editar_agendamento(id_agendamento):
    # Quando a edição for chamada, as únicas informações que podem ser alteradas são hora e status
    if request.method == 'GET':
        id_agendamento = id_agendamento
        query = "SELECT * FROM Agendamento WHERE id_agendamento = %s"
        resultado = execute_sql(query, (id_agendamento,), fetch_one=True)

        if not resultado:
            return jsonify({"erro": "Agendamento não encontrado!"}), 404

        agendamentos = {
            "id_agendamento": resultado[0],
            "id_animal": resultado[1],
            "id_status": resultado[2],
            "data": str(resultado[3]),
            "horario": resultado[4],
        }

        return jsonify(agendamentos), 200

    if request.method == 'PUT':
        data = request.json

        horario = data.get('horario')
        status = data.get('status')

        if not horario or not status:
            return jsonify({"erro": "Campos obrigatórios ausentes!"}), 400

        query = """
            UPDATE Agendamento
            SET horario = %s, id_status = %s
            WHERE id_agendamento = %s
                """
        params = (
            horario,
            status,
            id_agendamento
        )

        try:
            execute_sql(query, params)
            return jsonify({"mensagem": "Agendamento atualizado com sucesso!"}), 200
        except Exception as e:
            return jsonify({"erro": f"Erro ao atualizar agendamento: {str(e)}"}), 500


# Rotas para renderizar as páginas de HTML de agendamento
@agendamentos_bp.route('/agenda')
def agenda():
    return render_template('agenda.html')


@agendamentos_bp.route('/cadastro_agendamento_page')
def cadastro_agendamento_page():
    return render_template('tela_cadastros/cadastro_agendamentos.html')


@agendamentos_bp.route('/editar_agendamento_page')
def editar_agendamento_page():
    return render_template('tela_cadastros/editar_agendamento.html')