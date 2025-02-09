from app import db

class TipoExame:
    def __init__(self, id_tipo_exame, nome, descricao):
        self.id_tipo_exame = id_tipo_exame
        self.nome = nome
        self.descricao = descricao
        
    def __repr__(self):
        return f"<TipoExame {self.id_tipo_exame}>"
    
    def criar_tipo_exame(data):
        """
        Cria um novo tipo_exame no banco de dados.
        Recebe um dicionário `data` com os campos do tipo_exame.
        """
        # Validar os dados
        valido, mensagem = TipoExameValidator.validar_criar_tipo_exame(data)
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        id_tipo_exame = data['id_tipo_exame']
        nome = data['nome']
        descricao = data['descricao']

        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO TipoExame (id_tipo_exame, nome)
            VALUES (%s, %s)
            RETURNING id_tipo_exame
        """)
        cursor.execute(query, (id_tipo_exame, nome))
        id_tipo_exame = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return id_tipo_exame

    def buscar_tipo_exame_por_id(id_tipo_exame):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            SELECT * FROM TipoExame WHERE id_tipo_exame = %s
        """)
        cursor.execute(query, (id_tipo_exame,))
        tipo_exame = cursor.fetchone()
        cursor.close()
        conn.close()
        if tipo_exame:
            return TipoExame(*tipo_exame)
        return None

    def atualizar_tipo_exame(id_tipo_exame, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para o tipo_exame com o id_tipo_exame especificado.
        """
        # Validar os dados
        valido, mensagem = TipoExameValidator.validar_atualizar_tipo_exame(kwargs)
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
        valores.append(id_tipo_exame)  # Adicionar o id_tipo_exame no final

        query = sql.SQL("""
            UPDATE TipoExame
            SET {campos}
            WHERE id_tipo_exame = %s
        """).format(
            campos=sql.SQL(', ').join(
                sql.SQL("{} = %s").format(campo) for campo in campos
            )
        )

        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()
    
    
    def deletar_tipo_exame(id_tipo_exame):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            DELETE FROM TipoExame WHERE id_tipo_exame = %s
        """)
        cursor.execute(query, (id_tipo_exame,))
        conn.commit()
        cursor.close()
        conn.close()