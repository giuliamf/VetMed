<<<<<<< Updated upstream
class Pagamento:
    def __init__(self, id_pagamento, id_consulta, data_pagamento, id_meio_pagamento):
        self.id_pagamento = id_pagamento
        self.id_consulta = id_consulta
=======
from app import db

class Pagamento:
    def __init__(self, id_pagamento, id_consulta, valor, data_pagamento, id_meio_pagamento):
        self.id_pagamento = id_pagamento
        self.id_consulta = id_consulta
        self.valor = valor
>>>>>>> Stashed changes
        self.data_pagamento = data_pagamento
        self.id_meio_pagamento = id_meio_pagamento

    def __repr__(self):
        return f"<Pagamento {self.id_pagamento}>"
<<<<<<< Updated upstream


def criar_pagamento(data):   #verificar esse dicinário de entrada com o célio!!!
        """
        Cria um novo pagamento no banco de dados.
        Recebe um dicionário `data` com os campos do agendamento.
        """
        # Validar os dados
        valido, mensagem = PagamentoValidator.validar_criar_pagamento(data) 
=======
    
    def criar_pagamento(data):
        """
        Cria um novo pagamento no banco de dados.
        Recebe um dicionário `data` com os campos do pagamento.
        """
        # Validar os dados
        valido, mensagem = PagamentoValidator.validar_criar_pagamento(data)
>>>>>>> Stashed changes
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        id_pagamento = data['id_pagamento']
        id_consulta = data['id_consulta']
<<<<<<< Updated upstream
=======
        valor = data['valor']
>>>>>>> Stashed changes
        data_pagamento = datetime.strptime(data['data_pagamento'], '%d/%m/%Y').date()
        id_meio_pagamento = data['id_meio_pagamento']

        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
<<<<<<< Updated upstream
            INSERT INTO pagamento (id_pagamento, id_consulta, data_pagamento, id_meio_pagamento)
            VALUES (%s, %s, %s, %s)
            RETURNING id_pagamento
        """)
        cursor.execute(query, (id_pagamento, id_consulta, data_pagamento, id_meio_pagamento))
=======
            INSERT INTO Pagamento (id_pagamento, id_consulta, valor, data_pagamento, id_meio_pagamento))
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_pagamento
        """)
        cursor.execute(query, (id_consulta, valor, data_pagamento, id_meio_pagamento, id_status))
>>>>>>> Stashed changes
        id_pagamento = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return id_pagamento

    def buscar_pagamento_por_id(id_pagamento):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
<<<<<<< Updated upstream
            SELECT * FROM pagamento WHERE id_pagamento = %s
=======
            SELECT * FROM Pagamento WHERE id_pagamento = %s
>>>>>>> Stashed changes
        """)
        cursor.execute(query, (id_pagamento,))
        pagamento = cursor.fetchone()
        cursor.close()
        conn.close()
        if pagamento:
            return Pagamento(*pagamento)
        return None

<<<<<<< Updated upstream
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
 
=======
    def atualizar_pagamento(id_pagamento, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para o pagamento com o id_pagamento especificado.
        """
        # Validar os dados
        valido, mensagem = PagamentoValidator.validar_atualizar_pagamento(kwargs)
        if not valido:
            raise ValueError(mensagem)

        # Converter 'data' e 'id_meio_pagamento' para os tipos corretos, se presentes
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
        valores.append(id_pagamento)  # Adicionar o id_pagamento no final

        query = sql.SQL("""
            UPDATE Pagamento
            SET {campos}
            WHERE id_pagamento = %s
        """).format(
            campos=sql.SQL(', ').join(
                sql.SQL("{} = %s").format(campo) for campo in campos
            )
        )

        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()
    
    
    def deletar_pagamento(id_pagamento):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            DELETE FROM Pagamento WHERE id_pagamento = %s
        """)
        cursor.execute(query, (id_pagamento,))
        conn.commit()
        cursor.close()
        conn.close()
>>>>>>> Stashed changes
