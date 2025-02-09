from app import db

class Tratamento:
    def __init__(self, id_tratamento, id_consulta, tipo_tratamento, descricao, duracao_estimada, data_inicio):
        self.id_tratamento = id_tratamento
        self.id_consulta = id_consulta
        self.tipo_tratamento = tipo_tratamento
        self.descricao = descricao
        self.duracao_estimada = duracao_estimada
        self.data_inicio = data_inicio

    def __repr__(self):
        return f"<Tratamento {self.id_tratamento}>"
    
    def criar_tratamento(data):
        """
        Cria um novo tratamento no banco de dados.
        Recebe um dicionário `data` com os campos do tratamento.
        """
        # Validar os dados
        valido, mensagem = TratamentoValidator.validar_criar_tratamento(data)
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        id_tratamento = data['id_tratamento']
        id_consulta = data['id_consulta']
        tipo_tratamento = data['tipo_tratamento']
        descricao_tratamento = data['descricao']
        duracao_estimada = data['duracao_estimada']
        data_inicio = datetime.strptime(data['data_inicio'], '%d/%m/%Y').date()

        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO Tratamento (id_tratamento, id_consulta, tipo_tratamento, descricao, duracao_estimada, data_inicio)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_tratamento
        """)
        cursor.execute(query, (id_tratamento, id_consulta, tipo_tratamento, descricao, duracao_estimada, data_inicio))
        id_tratamento = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return id_tratamento

    def buscar_tratamento_por_id(id_tratamento):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            SELECT * FROM Tratamento WHERE id_tratamento = %s
        """)
        cursor.execute(query, (id_tratamento,))
        tratamento = cursor.fetchone()
        cursor.close()
        conn.close()
        if tratamento:
            return Tratamento(*tratamento)
        return None

    def atualizar_tratamento(id_tratamento, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para o tratamento com o id_tratamento especificado.
        """
        # Validar os dados
        valido, mensagem = TratamentoValidator.validar_atualizar_tratamento(kwargs)
        if not valido:
            raise ValueError(mensagem)

        # Converter 'data_inicio' para o tipo correto, se presente
        if 'data_inicio' in kwargs:
            kwargs['data_inicio'] = datetime.strptime(kwargs['data_inicio'], '%d/%m/%Y').date()

        # Construir a query dinamicamente
        conn = get_db_connection()
        cursor = conn.cursor()
        campos = []
        valores = []
        for campo, valor in kwargs.items():
            campos.append(sql.Identifier(campo))
            valores.append(valor)
        valores.append(id_tratamento)  # Adicionar o id_tratamento no final

        query = sql.SQL("""
            UPDATE Tratamento
            SET {campos}
            WHERE id_tratamento = %s
        """).format(
            campos=sql.SQL(', ').join(
                sql.SQL("{} = %s").format(campo) for campo in campos
            )
        )

        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()
    
    
    def deletar_tratamento(id_tratamento):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            DELETE FROM Tratamento WHERE id_tratamento = %s
        """)
        cursor.execute(query, (id_tratamento,))
        conn.commit()
        cursor.close()
        conn.close()
