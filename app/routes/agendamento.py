from flask import Blueprint, jsonify, request, render_template
from app.database import execute_sql

from app.utils.funcoes_com_cpf import formatar_cpf
from app.utils.buscas_bd import buscar_animais_por_cpf_tutor, buscar_vet_por_especialidade_turno, buscar_turno_por_horario

agendamentos_bp = Blueprint('agendamento', __name__)


@agendamentos_bp.route('/api/agendamentos', methods=['GET'])
def get_agendamentos():
    """ Retorna a lista de agendamentos do banco de dados filtrando por data """
    try:
        data_selecionada = request.args.get('data')

        if not data_selecionada:
            return jsonify({"erro": "Data não fornecida"}), 400

        query = """
            SELECT a.id_agendamento, p.nome AS paciente, t.nome AS tutor, s.nome AS status, 
                   u.nome AS veterinario, a.data, a.horario
            FROM Agendamento a
            JOIN Usuario u ON a.id_veterinario = u.id_usuario
            JOIN Animal p ON a.id_animal = p.id_animal
            JOIN Tutor t ON p.id_tutor = t.id_tutor
            JOIN Status_Agendamento s ON a.id_status = s.id_status
            JOIN Veterinario v ON a.id_veterinario = v.id_veterinario
            WHERE a.data = %s
            ORDER BY a.horario ASC
        """

        # Executando a consulta
        agendamentos = execute_sql(query, (data_selecionada,), fetch_all=True)

        if not agendamentos:
            return jsonify([]), 200  # Retorna uma lista vazia se não houver agendamentos

        agendamentos_lista = [
            {
                "id_agendamento": a[0],
                "paciente": a[1],
                "tutor": a[2],
                "status": a[3],
                "veterinario": a[4],  # Nome do veterinário
                "data": str(a[5]),
                "horario": a[6]
            }
            for a in agendamentos
        ]

        return jsonify(agendamentos_lista), 200
    except Exception as e:
        print(f"Erro ao buscar agendamentos: {e}")  # Log do erro no console do servidor
        return jsonify({"erro": f"Erro ao buscar agendamentos: {str(e)}"}), 500


@agendamentos_bp.route('/api/status', methods=['GET'])
def get_status():
    """ Retorna a lista de status para agendamento """
    try:
        query = "SELECT * FROM Status_Agendamento"
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
    """ Cadastro de novo agendamento utilizando a procedure """
    if not request.json:
        return jsonify({"erro": "Nenhum dado JSON foi recebido"}), 400

    data = request.json

    id_animal = data.get("id_animal")
    id_veterinario = data.get("id_veterinario")
    data_agendamento = data.get("data")
    horario = data.get("horario")
    id_especialidade = data.get("id_especialidade")

    if not all([id_animal, id_veterinario, data_agendamento, horario, id_especialidade]):
        print("Campos obrigatórios ausentes:", data)
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    try:
        # Buscar o turno com base no horário
        turno = buscar_turno_por_horario(horario)

        if not turno:
            return jsonify({"erro": "Turno não encontrado para este horário."}), 400

        # Chamar a procedure com o turno obtido
        execute_sql(
            "CALL realizar_agendamento(%s, %s, %s, %s, %s, %s)",
            (id_animal, id_veterinario, data_agendamento, horario, turno, id_especialidade)
        )

        return jsonify({"mensagem": "Agendamento realizado com sucesso!"}), 201

    except Exception as e:
        return jsonify({"erro": f"Erro ao cadastrar agendamento: {str(e)}"}), 500


@agendamentos_bp.route('/api/agendamentos/<int:id_agendamento>', methods=['GET', 'PUT'])
def editar_agendamento(id_agendamento):
    if request.method == 'GET':
        query = """
            SELECT a.id_agendamento, s.id_status, s.nome AS status
            FROM Agendamento a
            JOIN Status_Agendamento s ON a.id_status = s.id_status
            WHERE a.id_agendamento = %s
        """
        resultado = execute_sql(query, (id_agendamento,), fetch_one=True)

        if not resultado:
            return jsonify({"erro": "Agendamento não encontrado!"}), 404

        agendamento = {
            "id_agendamento": resultado[0],
            "id_status": resultado[1],
            "status": resultado[2]
        }

        return jsonify(agendamento), 200

    if request.method == 'PUT':
        data = request.json
        status = data.get('status')

        if not status:
            return jsonify({"erro": "O campo status é obrigatório!"}), 400

        query = """
            UPDATE Agendamento
            SET id_status = %s
            WHERE id_agendamento = %s
        """
        params = (status, id_agendamento)

        try:
            execute_sql(query, params)
            return jsonify({"mensagem": "Status atualizado com sucesso!"}), 200
        except Exception as e:
            return jsonify({"erro": f"Erro ao atualizar status: {str(e)}"}), 500


@agendamentos_bp.route('/api/pacientes_por_tutor', methods=['GET'])
def get_pacientes_por_tutor():
    """ Retorna os pacientes (animais) de um tutor pelo CPF """
    cpf_tutor = request.args.get("cpf")
    cpf_formatado = formatar_cpf(cpf_tutor)

    if not cpf_formatado:
        return jsonify({"erro": "CPF do tutor é obrigatório!"}), 400

    try:
        animais = buscar_animais_por_cpf_tutor(cpf_formatado)
        if not animais:
            return jsonify({"erro": "Tutor não encontrado!"}), 404

        pacientes_lista = [{"id": a[0], "nome": a[2]} for a in animais]
        print(pacientes_lista)

        return jsonify(pacientes_lista), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar pacientes: {str(e)}"}), 500


@agendamentos_bp.route('/api/veterinarios_disponiveis', methods=['GET'])
def get_veterinarios_disponiveis():
    """ Retorna a lista de veterinários filtrados por especialidade e, opcionalmente, por turno """
    especialidade_id = request.args.get("especialidade_id")

    if not especialidade_id:
        return jsonify({"erro": "Especialidade é obrigatória!"}), 400

    try:
        veterinarios = buscar_vet_por_especialidade_turno(especialidade_id)

        print(f"Veterinários encontrados para especialidade {especialidade_id}: {veterinarios}")

        if not veterinarios:
            print("Nenhum veterinário encontrado para os filtros.")
            return jsonify([]), 200  # Retorna uma lista vazia se não houver veterinários

        return jsonify(veterinarios), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar veterinários disponíveis: {str(e)}"}), 500


@agendamentos_bp.route('/api/horarios', methods=['GET'])
def get_horarios():
    """ Retorna todos os horários disponíveis e, se um turno for selecionado, filtra os horários desse turno. """
    try:
        query = "SELECT horario FROM Horario_Funcionamento ORDER BY horario ASC"
        horarios = execute_sql(query, fetch_all=True)

        if horarios:
            horarios_lista = [h[0] for h in horarios]
        else:
            horarios_lista = []

        print("Retornando horários:", horarios_lista)  # Depuração
        print(horarios)

        return jsonify(horarios_lista), 200
    except Exception as e:
        print(f"Erro ao buscar horários: {e}")  # Log do erro no console do servidor
        return jsonify({"erro": f"Erro ao buscar horários: {str(e)}"}), 500


@agendamentos_bp.route('/api/especialidades', methods=['GET'])
def get_especialidades():
    """ Retorna a lista de especialidades """
    try:
        query = "SELECT id_especialidade, nome FROM Especialidade ORDER BY nome ASC"
        especialidades = execute_sql(query, fetch_all=True)

        print("Especialidades recebidas do banco: ", especialidades)  # Depuração

        if not especialidades:
            return jsonify([]), 200  # Retorna lista vazia caso não haja especialidades

        lista_especialidade = [{"id": e[0], "nome": e[1]} for e in especialidades]

        print("Lista final de especialidades:", lista_especialidade)  # Depuração

        return jsonify(lista_especialidade), 200
    except Exception as e:
        print(f"Erro ao buscar especialidades: {e}")  # Log do erro no servidor
        return jsonify({"erro": f"Erro ao buscar especialidades: {str(e)}"}), 500


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
