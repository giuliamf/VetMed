from app import db

class Veterinario:
    def __init__(self, id_veterinario, nome, telefone, endereco, email, crmv):
        self.id_veterinario = id_veterinario
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.email = email
        self.crmv = crmv

    def __repr__(self):
        return f"<Veterinario {self.id_veterinario}>"

    @staticmethod
    def criar_veterinario(data):
        """
        Cria um novo veterinário no banco de dados.
        Recebe um dicionário `data` com os campos do veterinário.
        """
        # Validar os dados
        valido, mensagem = VeterinarioValidator.validar_veterinario(data)
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        id_veterinario = data['id_veterinario']
        nome = data['nome']
        telefone = data['telefone']
        endereco = data['endereco']
        email = data['email']
        crmv = data['crmv']

        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Veterinario (id_veterinario, nome, telefone, endereco, email, crmv)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (id_veterinario, nome, telefone, endereco, email, crmv))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def buscar_veterinario_por_id(id_veterinario):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT * FROM Veterinario WHERE id_veterinario = %s
        """
        cursor.execute(query, (id_veterinario,))
        veterinario = cursor.fetchone()
        cursor.close()
        conn.close()
        if veterinario:
            return Veterinario(*veterinario)
        return None

    @staticmethod
    def atualizar_veterinario(id_veterinario, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para o veterinário com o id_veterinario especificado.
        """
        # Validar os dados
        valido, mensagem = VeterinarioValidator.validar_atualizar_veterinario(kwargs)
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
        valores.append(id_veterinario)  # Adicionar o id_veterinario no final

        query = sql.SQL("""
            UPDATE Veterinario
            SET {campos}
            WHERE id_veterinario = %s
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
    def deletar_veterinario(id_veterinario):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            DELETE FROM Veterinario WHERE id_veterinario = %s
        """
        cursor.execute(query, (id_veterinario,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def adicionar_especialidade(id_veterinario, id_especialidade):
        """
        Adiciona uma especialidade a um veterinário específico.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Veterinario_Especialidade (id_veterinario, id_especialidade)
            VALUES (%s, %s)
        """
        cursor.execute(query, (id_veterinario, id_especialidade))
        conn.commit()
        cursor.close()
        conn.close()