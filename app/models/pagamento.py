class Pagamento:
    def __init__(self, id_pagamento, id_consulta, data_pagamento, id_meio_pagamento):
        self.id_pagamento = id_pagamento
        self.id_consulta = id_consulta
        self.data_pagamento = data_pagamento
        self.id_meio_pagamento = id_meio_pagamento

    def __repr__(self):
        return f"<Pagamento {self.id_pagamento}>"


def criar_pagamento(data):   #verificar esse dicinário de entrada com o célio!!!
        """
        Cria um novo pagamento no banco de dados.
        Recebe um dicionário `data` com os campos do agendamento.
        """
        # Validar os dados
        valido, mensagem = PagamentoValidator.validar_criar_pagamento(data) 
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        id_pagamento = data['id_pagamento']
        id_consulta = data['id_consulta']
        data_pagamento = datetime.strptime(data['data_pagamento'], '%d/%m/%Y').date()
        id_meio_pagamento = data['id_meio_pagamento']

        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO pagamento (id_pagamento, id_consulta, data_pagamento, id_meio_pagamento)
            VALUES (%s, %s, %s, %s)
            RETURNING id_pagamento
        """)
        cursor.execute(query, (id_pagamento, id_consulta, data_pagamento, id_meio_pagamento))
        id_pagamento = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return id_pagamento

    def buscar_pagamento_por_id(id_pagamento):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            SELECT * FROM pagamento WHERE id_pagamento = %s
        """)
        cursor.execute(query, (id_pagamento,))
        pagamento = cursor.fetchone()
        cursor.close()
        conn.close()
        if pagamento:
            return Pagamento(*pagamento)
        return None

    def atualizar_pagamento(id_pagamento, id_consulta, data_pagamento, id_meio_pagamento):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            UPDATE pagamento
            SET id_pagamento = %s, id_consulta = %s, data_pagamento = %s, id_meio_pagamento = %s
            WHERE id_pagamento = %s
        """)
        cursor.execute(query, (id_pagamento, id_consulta, data_pagamento, id_meio_pagamento))
        conn.commit()
        cursor.close()
        conn.close()
 