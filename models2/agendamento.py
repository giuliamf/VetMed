class Agendamento:
    def __init__(self, id_agendamento, id_tutor, id_animal, data, hora, id_status):
        self.id_agendamento = id_agendamento
        self.id_tutor = id_tutor
        self.id_animal = id_animal
        self.data = data
        self.hora = hora
        self.id_status = id_status

    def __repr__(self):
        return f"<Agendamento {self.id_agendamento}>"
    
    def criar_agendamento(data):
        """
        Cria um novo agendamento no banco de dados.
        Recebe um dicionário `data` com os campos do agendamento.
        """
        # Validar os dados
        valido, mensagem = AgendamentoValidator.validar_criar_agendamento(data)
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        id_tutor = data['id_tutor']
        id_animal = data['id_animal']
        data_agendamento = datetime.strptime(data['data'], '%d/%m/%Y').date()
        hora_agendamento = datetime.strptime(data['hora'], '%H:%M').time()
        id_status = data['id_status']

        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO agendamentos (id_tutor, id_animal, data, hora, id_status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_agendamento
        """)
        cursor.execute(query, (id_tutor, id_animal, data_agendamento, hora_agendamento, id_status))
        id_agendamento = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return id_agendamento

    def buscar_agendamento_por_id(id_agendamento):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            SELECT * FROM agendamentos WHERE id_agendamento = %s
        """)
        cursor.execute(query, (id_agendamento,))
        agendamento = cursor.fetchone()
        cursor.close()
        conn.close()
        if agendamento:
            return Agendamento(*agendamento)
        return None

    def atualizar_agendamento(id_agendamento, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para o agendamento com o id_agendamento especificado.
        """
        # Validar os dados
        valido, mensagem = AgendamentoValidator.validar_atualizar_agendamento(kwargs)
        if not valido:
            raise ValueError(mensagem)

        # Converter 'data' e 'hora' para os tipos corretos, se presentes
        if 'data' in kwargs:
            kwargs['data'] = datetime.strptime(kwargs['data'], '%d/%m/%Y').date()
        if 'hora' in kwargs:
            kwargs['hora'] = datetime.strptime(kwargs['hora'], '%H:%M').time()

        # Construir a query dinamicamente
        conn = get_db_connection()
        cursor = conn.cursor()
        campos = []
        valores = []
        for campo, valor in kwargs.items():
            campos.append(sql.Identifier(campo))
            valores.append(valor)
        valores.append(id_agendamento)  # Adicionar o id_agendamento no final

        query = sql.SQL("""
            UPDATE agendamentos
            SET {campos}
            WHERE id_agendamento = %s
        """).format(
            campos=sql.SQL(', ').join(
                sql.SQL("{} = %s").format(campo) for campo in campos
            )
        )

        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()
    
    
    def deletar_agendamento(id_agendamento):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            DELETE FROM agendamentos WHERE id_agendamento = %s
        """)
        cursor.execute(query, (id_agendamento,))
        conn.commit()
        cursor.close()
        conn.close()
