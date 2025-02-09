from app import db

class Receita_Medicamento:
    def __init__(self, id_receita_med, id_medicamento, quantidade, tipo_quantidade, frequencia, duracao):
        self.id_receita_med = id_receita_med
        self.id_medicamento = id_medicamento
        self.quantidade = quantidade
        self.tipo_quantidade = tipo_quantidade
        self.frequencia = frequencia
        self.duracao = duracao

    def __repr__(self):
        return f"<Receita_Medicamento {self.id_receita_med}>"
    
    def criar_receita_med(data):
        """
        Cria um novo agendamento no banco de dados.
        Recebe um dicionário `data` com os campos do agendamento.
        """
        # Validar os dados
        valido, mensagem = Receita_MedicamentoValidator.validar_criar_receita_med(data)
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        id_receita_med = data[ 'id_receita_med']
        id_medicamento = data[ 'id_medicamento']
        quantidade = data[ 'quantidade']
        tipo_quantidade = data['tipo_quantidade']
        frequencia = data[ 'frequencia']
        duracao = data['duracao']

        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO Receita_Medicamento (id_receita_med, id_medicamento, quantidade, tipo_quantidade, frequencia, duracao)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_receita_med
        """)
        cursor.execute(query, (id_medicamento, quantidade, data_receita_med, tipo_quantidade_receita_med, frequencia))
        receita_med = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return receita_med

    def buscar_receita_med_por_id(id_receita_med):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            SELECT * FROM Receita_Medicamento WHERE id_receita_med = %s
        """)
        cursor.execute(query, (id_receita_med,))
        receita_med = cursor.fetchone()
        cursor.close()
        conn.close()
        if receita_med:
            return Receita_Medicamento(*receita_med)
        return None

    def atualizar_receita_med(id_receita_med, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para a receita médica com o id_receita_med especificado.
        """
        # Validar os dados
        valido, mensagem = Receita_MedicamentoValidator.validar_atualizar_receita_med(kwargs)
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
        valores.append(id_receita_med)  # Adicionar o id_receita_med no final

        query = sql.SQL("""
            UPDATE Receita_Medicamento
            SET {campos}
            WHERE id_receita_med = %s
        """).format(
            campos=sql.SQL(', ').join(
                sql.SQL("{} = %s").format(campo) for campo in campos
            )
        )

        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()
    
    
    def deletar_receita_med(id_receita_med):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            DELETE FROM Receita_Medicamento WHERE id_receita_med = %s
        """)
        cursor.execute(query, (id_receita_med,))
        conn.commit()
        cursor.close()
        conn.close()
