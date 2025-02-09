from app import db

class Status:
    def __init__(self, id_status, nome):
        self.id_status = id_status
        self.nome = nome
        
    def __repr__(self):
        return f"<Status {self.id_status}>"
    
    def criar_status(data):
        """
        Cria um novo status no banco de dados.
        Recebe um dicionário `data` com os campos do status.
        """
        # Validar os dados
        valido, mensagem = StatusValidator.validar_criar_status(data)
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        id_status = data['id_status']
        nome = data['nome']
        
        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO Status (id_status, nome)
            VALUES (%s, %s)
            RETURNING id_status
        """)
        cursor.execute(query, (id_status, nome))
        id_status = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return id_status

    def buscar_status_por_id(id_status):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            SELECT * FROM Status WHERE id_status = %s
        """)
        cursor.execute(query, (id_status,))
        statu = cursor.fetchone()
        cursor.close()
        conn.close()
        if statu:
            return Status(*statu)
        return None

    def atualizar_status(id_status, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para o status com o id_status especificado.
        """
        # Validar os dados
        valido, mensagem = StatusValidator.validar_atualizar_status(kwargs)
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
        valores.append(id_status)  # Adicionar o id_status no final

        query = sql.SQL("""
            UPDATE Status
            SET {campos}
            WHERE id_status = %s
        """).format(
            campos=sql.SQL(', ').join(
                sql.SQL("{} = %s").format(campo) for campo in campos
            )
        )

        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()
    
    
    def deletar_status(id_status):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            DELETE FROM Status WHERE id_status = %s
        """)
        cursor.execute(query, (id_status,))
        conn.commit()
        cursor.close()
        conn.close()