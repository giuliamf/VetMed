from app import db

class Tutor:
    def __init__(self, id_tutor, nome, data_nascimento, telefone, endereco, email):
        self.id_tutor = id_tutor
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.endereco = endereco
        self.email = email

    def __repr__(self):
        return f"<Tutor {self.id_tutor}>"
    
    def criar_tutor(data):
        """
        Cria um novo tutor no banco de dados.
        Recebe um dicionário `data` com os campos do tutor.
        """
        # Validar os dados
        valido, mensagem = TutorValidator.validar_criar_tutor(data)
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        id_tutor = data['id_tutor']
        nome = data['nome']
        data_nascimento = data['data_nascimento']
        telefone = data['telefone']
        endereco = data['endereco']
        email = data['email']
        id_tutor = data['id_tutor']
        
        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO Tutor (id_tutor, nome, data_nascimento, telefone, endereco, email)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_tutor
        """)
        cursor.execute(query, (id_tutor, nome, data_nascimento, telefone, endereco, email))
        id_tutor = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return id_tutor

    def buscar_tutor_por_id(id_tutor):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            SELECT * FROM Tutor WHERE id_tutor = %s
        """)
        cursor.execute(query, (id_tutor,))
        tutor = cursor.fetchone()
        cursor.close()
        conn.close()
        if tutor:
            return Tutor(*tutor)
        return None

    def atualizar_tutor(id_tutor, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para o tutor com o id_tutor especificado.
        """
        # Validar os dados
        valido, mensagem = TutorValidator.validar_atualizar_tutor(kwargs)
        if not valido:
            raise ValueError(mensagem)

        # Converter 'data' e 'telefone' para os tipos corretos, se presentes
        if 'data' in kwargs:
            kwargs['data'] = datetime.strptime(kwargs['data'], '%d/%m/%Y').date()
        if 'telefone' in kwargs:
            kwargs['telefone'] = datetime.strptime(kwargs['telefone'], '%H:%M').time()

        # Construir a query dinamicamente
        conn = get_db_connection()
        cursor = conn.cursor()
        campos = []
        valores = []
        for campo, valor in kwargs.items():
            campos.append(sql.Identifier(campo))
            valores.append(valor)
        valores.append(id_tutor)  # Adicionar o id_tutor no final

        query = sql.SQL("""
            UPDATE Tutor
            SET {campos}
            WHERE id_tutor = %s
        """).format(
            campos=sql.SQL(', ').join(
                sql.SQL("{} = %s").format(campo) for campo in campos
            )
        )

        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()
    
    
    def deletar_tutor(id_tutor):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            DELETE FROM Tutor WHERE id_tutor = %s
        """)
        cursor.execute(query, (id_tutor,))
        conn.commit()
        cursor.close()
        conn.close()
