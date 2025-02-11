from app import db

class Usuario:
    def __init__(self, email_usuario, nome, telefone, endereco, senha):
        self.email_usuario = email_usuario
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.senha = senha

    def __repr__(self):
        return f"<Usuario {self.email_usuario}>"

    
    def criar_usuario(data):
        """
        Cria um novo usuário no banco de dados.
        Recebe um dicionário `data` com os campos do usuário.
        """
        # Validar os dados
        valido, mensagem = UsuarioValidator.validar_usuario(data)
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        email_usuario = data['email_usuario']
        nome = data['nome']
        telefone = data['telefone']
        endereco = data['endereco']
        senha = data['senha']

        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Usuario (email_usuario, nome, telefone, endereco, senha)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (email_usuario, nome, telefone, endereco, senha))
        conn.commit()
        cursor.close()
        conn.close()

    
    def buscar_usuario_por_email(email_usuario):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT * FROM Usuario WHERE email_usuario = %s
        """
        cursor.execute(query, (email_usuario,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        if usuario:
            return Usuario(*usuario)
        return None

  
    def atualizar_usuario(email_usuario, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para o usuário com o email_usuario especificado.
        """
        # Validar os dados
        valido, mensagem = UsuarioValidator.validar_atualizar_usuario(kwargs)
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
        valores.append(email_usuario)  # Adicionar o email_usuario no final

        query = sql.SQL("""
            UPDATE Usuario
            SET {campos}
            WHERE email_usuario = %s
        """).format(
            campos=sql.SQL(', ').join(
                sql.SQL("{} = %s").format(campo) for campo in campos
            )
        )

        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()

    
    def deletar_usuario(email_usuario):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            DELETE FROM Usuario WHERE email_usuario = %s
        """
        cursor.execute(query, (email_usuario,))
        conn.commit()
        cursor.close()
        conn.close()