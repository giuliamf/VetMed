from app import db

class Tipo:
    def __init__(self, id_tipo, nome, categoria, descricao):
        self.id_tipo = id_tipo
        self.nome = nome
        self.categoria = categoria
        self.descricao = descricao
        
    def __repr__(self):
        return f"<Tipo {self.id_tipo}>"
    
    def criar_tipo(data):
        """
        Cria um novo tipo no banco de dados.
        Recebe um dicionário `data` com os campos do tipo.
        """
        # Validar os dados
        valido, mensagem = TipoValidator.validar_criar_tipo(data)
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        id_tipo = data['id_tipo']
        nome = data['nome']
        categoria = data['categoria']
        descricao = data['descricao']
        
        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO Tipo (id_tipo, nome)
            VALUES (%s, %s)
            RETURNING id_tipo
        """)
        cursor.execute(query, (id_tipo, nome))
        id_ipo = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return id_tipo

    def buscar_meio_pagamento_por_id(id_tipo):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            SELECT * FROM Tipo WHERE id_tipo = %s
        """)
        cursor.execute(query, (id_tipo,))
        tipo = cursor.fetchone()
        cursor.close()
        conn.close()
        if tipo:
            return Tipo(*tipo)
        return None

    def atualizar_meio_pagamento(id_tipo, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para o tipo com o id_tipo especificado.
        """
        # Validar os dados
        valido, mensagem = TipoValidator.validar_atualizar_tipo(kwargs)
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
        valores.append(id_tipo)  # Adicionar o id_tipo no final

        query = sql.SQL("""
            UPDATE Tipo
            SET {campos}
            WHERE id_tipo = %s
        """).format(
            campos=sql.SQL(', ').join(
                sql.SQL("{} = %s").format(campo) for campo in campos
            )
        )

        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()
    
    
    def deletar_tipo(id_tipo):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            DELETE FROM Tipo WHERE id_tipo = %s
        """)
        cursor.execute(query, (id_tipo,))
        conn.commit()
        cursor.close()
        conn.close()