from app import db

<<<<<<< Updated upstream

class Tratamento(db.Model):
    __tablename__ = 'tratamentos'

    id_tratamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_consulta = db.Column(db.Integer, db.ForeignKey('consultas.id_consulta'), nullable=False)
    tipo_tratamento = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    duracao_estimada = db.Column(db.String(50), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)

    # Relacionamento com a tabela Consultas
    consulta = db.relationship('Consulta', backref='tratamentos')
=======
class Tratamento:
    def __init__(self, id_tratamento, descricao, preco):
        self.id_tratamento = id_tratamento
        self.descricao = descricao
        self.preco = preco
>>>>>>> Stashed changes

    def __repr__(self):
        return f"<Tratamento {self.id_tratamento}>"
    
    @staticmethod
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
        descricao = data['descricao']
        preco = data['preco']

        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Tratamento (descricao, preco)
            VALUES (%s, %s)
            RETURNING id_tratamento
        """
        cursor.execute(query, (descricao, preco))
        id_tratamento = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return id_tratamento

    @staticmethod
    def buscar_tratamento_por_id(id_tratamento):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT * FROM Tratamento WHERE id_tratamento = %s
        """
        cursor.execute(query, (id_tratamento,))
        tratamento = cursor.fetchone()
        cursor.close()
        conn.close()
        if tratamento:
            return Tratamento(*tratamento)
        return None

    @staticmethod
    def atualizar_tratamento(id_tratamento, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para o tratamento com o id_tratamento especificado.
        """
        # Validar os dados
        valido, mensagem = TratamentoValidator.validar_atualizar_tratamento(kwargs)
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
    
    
    @staticmethod
    def deletar_tratamento(id_tratamento):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            DELETE FROM Tratamento WHERE id_tratamento = %s
        """
        cursor.execute(query, (id_tratamento,))
        conn.commit()
        cursor.close()
        conn.close()