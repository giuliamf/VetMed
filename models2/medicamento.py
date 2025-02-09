from app import db

class Medicamento:
    def __init__(self, id_medicamento, nome, descricao, tipo, uso):
        self.id_medicamento = id_medicamento
        self.nome = nome
        self.descricao = descricao
        self.tipo = tipo
        self.uso = uso

    def __repr__(self):
        return f"<Medicamento {self.id_medicamento}>"
    
    def criar_medicamento(data):
        """
        Cria um novo agendamento no banco de dados.
        Recebe um dicionário `data` com os campos do agendamento.
        """
        # Validar os dados
        valido, mensagem = MedicamentoValidator.validar_criar_mecicamento(data)
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        id_medicamento = data['id_medicamento']
        nome = data['nome']
        descricao = data['descricao']
        tipo = data['tipo']
        uso = data['uso']

        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO medicamento (id_medicamento, nome, descricao, tipo, uso)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_medicamento
        """)
        cursor.execute(query, (id_medicamento, nome, descricao, tipo, uso))
        id_medicamento = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return id_medicamento

    def buscar_medicamento_por_id(id_medicamento):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            SELECT * FROM medicamento WHERE id_medicamento = %s
        """)
        cursor.execute(query, (id_medicamento,))
        medicamento = cursor.fetchone()
        cursor.close()
        conn.close()
        if medicamento:
            return Medicamento(*medicamento)
        return None

    def atualizar_medicamento(id_medicamento, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para o medicamento com o id_medicamento especificado.
        """
        # Validar os dados
        valido, mensagem = MedicamentoValidator.validar_atualizar_medicamento(kwargs)
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
        valores.append(id_medicamento)  # Adicionar o id_medicamento no final

        query = sql.SQL("""
            UPDATE Medicamento
            SET {campos}
            WHERE id_medicamento = %s
        """).format(
            campos=sql.SQL(', ').join(
                sql.SQL("{} = %s").format(campo) for campo in campos
            )
        )

        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()
    
    
    def deletar_medicamento(id_medicamento):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            DELETE FROM Medicamento WHERE id_medicamento = %s
        """)
        cursor.execute(query, (id_medicamento,))
        conn.commit()
        cursor.close()
        conn.close()