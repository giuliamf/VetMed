from app import db

class Meio_Pagamento:
    def __init__(self, id_meio_pagamento, nome):
        self.id_meio_pagamento = id_meio_pagamento
        self.nome = nome
        
    def __repr__(self):
        return f"<Meio_Pagamento {self.id_meio_pagamento}>"
    
    def criar_meio_pagamento(data):
        """
        Cria um novo meio_pagamento no banco de dados.
        Recebe um dicionário `data` com os campos do meio_pagamento.
        """
        # Validar os dados
        valido, mensagem = Meio_PagamentoValidator.validar_criar_meio_pagamento(data)
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        id_meio_pagamento = data['id_meio_pagamento']
        nome = data['nome']
        
        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO Meio_Pagamento (id_meio_pagamento, nome)
            VALUES (%s, %s)
            RETURNING id_meio_pagamento
        """)
        cursor.execute(query, (id_meio_pagamento, nome))
        id_meio_pagamento = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return id_meio_pagamento

    def buscar_meio_pagamento_por_id(id_meio_pagamento):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            SELECT * FROM Meio_Pagamento WHERE id_meio_pagamento = %s
        """)
        cursor.execute(query, (id_meio_pagamento,))
        meio_pagamento = cursor.fetchone()
        cursor.close()
        conn.close()
        if meio_pagamento:
            return Meio_Pagamento(*meio_pagamento)
        return None

    def atualizar_meio_pagamento(id_meio_pagamento, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para o meio_pagamento com o id_meio_pagamento especificado.
        """
        # Validar os dados
        valido, mensagem = Meio_PagamentoValidator.validar_atualizar_meio_pagamento(kwargs)
        if not valido:
            raise ValueError(mensagem)

        # Construir a query dinamicamente
        conn = get_db_connection()
        cursor = conn.cursor()
        campos = []
        valores = []
        for campo, valor in kwargs.items():
            campos.append(sql.Identifier(campo))
            valores.append(valor)
        valores.append(id_meio_pagamento)  # Adicionar o id_meio_pagamento no final

        query = sql.SQL("""
            UPDATE Meio_Pagamento
            SET {campos}
            WHERE id_meio_pagamento = %s
        """).format(
            campos=sql.SQL(', ').join(
                sql.SQL("{} = %s").format(campo) for campo in campos
            )
        )

        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()
    
    
    def deletar_meio_pagamento(id_meio_pagamento):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            DELETE FROM Meio_Pagamento WHERE id_meio_pagamento = %s
        """)
        cursor.execute(query, (id_meio_pagamento,))
        conn.commit()
        cursor.close()
        conn.close()