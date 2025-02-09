from app import db

class Receita:
    def __init__(self, id_receita, id_consulta, id_tratamento, id_veterinario, data, observacoes):
        self.id_receita = id_receita
        self.id_consulta = id_consulta
        self.id_tratamento = id_tratamento
        self.id_veterinario = id_veterinario       
        self.data = data
        self.observacoes = observacoes
   
    def __repr__(self):
        return f"<Receita {self.id_receita}>"
    
    def criar_receita(data):
        """
        Cria uma nova receita no banco de dados.
        Recebe um dicionário `data` com os campos da receita.
        """
        # Validar os dados
        valido, mensagem = ReceitaValidator.validar_criar_receita(data)
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        id_receita = data['id_receita']
        id_consulta = data['id_consulta']
        id_tratamento = data['id_tratamento']
        id_veterinario = data['id_veterinario']
        data_agendamento = datetime.strptime(data['data'], '%d/%m/%Y').date()
        observacoes = data['observacoes']
        
        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO Receita (id_receita, id_consulta, id_tratamento, id_veterinario, data, observacoes)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_receita
        """)
        cursor.execute(query, (id_receita, id_consulta, id_tratamento, data_agendamento, id_veterinario, observacoes))
        id_receita = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return id_receita

    def buscar_receita_por_id(id_receita):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            SELECT * FROM Receita WHERE id_receita = %s
        """)
        cursor.execute(query, (id_receita,))
        receita = cursor.fetchone()
        cursor.close()
        conn.close()
        if receita:
            return Receita(*receita)
        return None

    def atualizar_receita(id_receita, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para o agendamento com o id_receita especificado.
        """
        # Validar os dados
        valido, mensagem = ReceitaValidator.validar_atualizar_receita(kwargs)
        if not valido:
            raise ValueError(mensagem)

        # Converter 'data' e 'observacoes' para os tipos corretos, se presentes
        if 'data' in kwargs:
            kwargs['data'] = datetime.strptime(kwargs['data'], '%d/%m/%Y').date()
       
        # Construir a query dinamicamente
        conn = get_db_connection()
        cursor = conn.cursor()
        campos = []
        valores = []
        for campo, valor in kwargs.items():
            campos.append(sql.Identifier(campo))
            valores.append(valor)
        valores.append(id_receita)  # Adicionar o id_receita no final

        query = sql.SQL("""
            UPDATE Receita
            SET {campos}
            WHERE id_receita = %s
        """).format(
            campos=sql.SQL(', ').join(
                sql.SQL("{} = %s").format(campo) for campo in campos
            )
        )

        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()
    
    
    def deletar_receita(id_receita):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            DELETE FROM Receita WHERE id_receita = %s
        """)
        cursor.execute(query, (id_receita,))
        conn.commit()
        cursor.close()
        conn.close()
