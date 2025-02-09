from app import db

class Exame:
    def __init__(self, id_exame, id_consulta, id_animal, id_tipo_exame, resultado, data_exame, observacoes):
        self.id_exame = id_exame
        self.id_consulta = id_consulta
        self.id_animal = id_animal
        self.id_tipo_exame = id_tipo_exame
        self.resultado = resultado
        self.data_exame = data_exame
        self.observacoes = observacoes

    def __repr__(self):
        return f"<Exame {self.id_exame}>"

    def criar_exame(data):
        """
        Cria um novo exame no banco de dados.
        Recebe um dicionário `data` com os campos do exame.
        """
        # Validar os dados
        valido, mensagem = Exame.validar_criar_exame(data)
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        id_exame = data['id_exame']
        id_consulta = data['id_consulta']
        id_animal = data['id_animal']
        id_tipo_exame = data['id_tipo_exame']
        resultado = data['resultado']
        data_exame = datetime.strptime(data['data_exame'], '%d/%m/%Y').date()
        observacoes = data['observacoes']

        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO exame (id_exame, id_consulta, id_animal, id_tipo_exame, resultado, data_exame, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_exame
        """)
        cursor.execute(query, (id_tutor, id_animal, data_agendamento, hora_agendamento, id_status))
        id_exame = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return id_exame

        def buscar_exame(id_exame):
            conn = get_db_connection()
            cursor = conn.cursor()
            query = sql.SQL("""
                SELECT * FROM exame WHERE id_exame = %s
            """)
            cursor.execute(query, (id_exame,))
            exame = cursor.fetchone()
            cursor.close()
            conn.close()
            if exame:
                return Exame(*exame)
            return None

    def atualizar_exame(id_exame, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para o agendamento com o id_exame especificado.
        """
        # Validar os dados
        valido, mensagem = ExameValidator.validar_atualizar_exame(kwargs)
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
        valores.append(id_exame)  # Adicionar o id_exame no final

        query = sql.SQL("""
            UPDATE Exame
            SET {campos}
            WHERE id_exame = %s
        """).format(
            campos=sql.SQL(', ').join(
                sql.SQL("{} = %s").format(campo) for campo in campos
            )
        )

        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()

        def deletar_exame(id_exame):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            DELETE FROM Exame WHERE id_exame = %s
        """)
        cursor.execute(query, (id_exame,))
        conn.commit()
        cursor.close()
        conn.close()
