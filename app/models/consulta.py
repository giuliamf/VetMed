from app import db

class Consulta:
    def __init__(self, id_consulta, id_agendamento, id_veterinario, data, horario, id_tipo):
        self.id_consulta = id_consulta
        self.id_agendamento = id_agendamento
        self.id_veterinario = id_veterinario
        self.data = data
        self.horario = horario
        self.id_tipo = id_tipo
        self.valor_total = None

    def __repr__(self):
        return f"<Consulta {self.id_consulta}>"
    
    @staticmethod
    def criar_consulta(data):
        """
        Cria uma nova consulta no banco de dados.
        Recebe um dicionário `data` com os campos da consulta.
        """
        # Validar os dados
        valido, mensagem = ConsultaValidator.validar_consulta(data)
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        id_agendamento = data['id_agendamento']
        id_veterinario = data['id_veterinario']
        data_consulta = datetime.strptime(data['data'], '%d/%m/%Y').date()
        horario = datetime.strptime(data['horario'], '%H:%M').time()
        id_tipo = data['id_tipo']

        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO consulta (id_agendamento, id_veterinario, data, horario, id_tipo)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_consulta
        """
        cursor.execute(query, (id_agendamento, id_veterinario, data_consulta, horario, id_tipo))
        id_consulta = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return id_consulta

    @staticmethod
    def atualizar_consulta(id_consulta, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para a consulta com o id_consulta especificado.
        """
        # Validar os dados
        valido, mensagem = ConsultaValidator.validar_atualizar_consulta(kwargs)
        if not valido:
            raise ValueError(mensagem)

        # Converter 'data' e 'horario' para os tipos corretos, se presentes
        if 'data' in kwargs:
            kwargs['data'] = datetime.strptime(kwargs['data'], '%d/%m/%Y').date()
        if 'horario' in kwargs:
            kwargs['horario'] = datetime.strptime(kwargs['horario'], '%H:%M').time()

        # Construir a query dinamicamente
        conn = get_db_connection()
        cursor = conn.cursor()
        campos = []
        valores = []
        for campo, valor in kwargs.items():
            campos.append(sql.Identifier(campo))
            valores.append(valor)
        valores.append(id_consulta)  # Adicionar o id_consulta no final

        query = sql.SQL("""
            UPDATE consulta
            SET {campos}
            WHERE id_consulta = %s
        """).format(
            campos=sql.SQL(', ').join(
                sql.SQL("{} = %s").format(campo) for campo in campos
            )
        )

        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def deletar_consulta(id_consulta):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            DELETE FROM consulta WHERE id_consulta = %s
        """
        cursor.execute(query, (id_consulta,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def adicionar_tratamento(id_consulta, id_tratamento):
        """
        Adiciona um tratamento a uma consulta específica.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO consulta_tratamento (id_consulta, id_tratamento)
            VALUES (%s, %s)
        """
        cursor.execute(query, (id_consulta, id_tratamento))
        conn.commit()
        cursor.close()
        conn.close()