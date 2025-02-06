from app import db
from app.validators import AnimalValidator


class Animal:
    def __init__(self, id_animal, id_tutor, nome, especie, raca, ano_nascimento, sexo, peso, cor):
        self.id_animal = id_animal
        self.id_tutor = id_tutor
        self.nome = nome
        self.especie = especie
        self.raca = raca
        self.ano_nascimento = ano_nascimento
        self.sexo = sexo
        self.peso = peso
        self.cor = cor

    def __repr__(self):
        return f"<Animal {self.id_animal}>"

    @staticmethod
    def criar_animal(data):
        """
        Cria um novo animal no banco de dados.
        Recebe um dicionário `data` com os campos do animal.
        """
        # Validar os dados
        valido, mensagem = AnimalValidator.validar_criar_animal(data)
        if not valido:
            raise ValueError(mensagem)

        # Extrair os valores do dicionário
        id_tutor = data.get('id_tutor')
        nome = data.get('nome')
        especie = data.get('especie')
        raca = data.get('raca')
        ano_nascimento = data.get('ano_nascimento')
        sexo = data.get('sexo')
        peso = data.get('peso')
        cor = data.get('cor')

        # GIULIA:
        # id do animal deve ser criado diretamente no banco de dados utilizando o comando SERIAL
        #with get_db_connection() as conn:
        #with conn.cursor() as cursor:
        #cursor.execute(query, (id_tutor, nome, especie, raca, ano_nascimento, sexo, peso, cor))
        #id_animal = cursor.fetchone()[0]
        #conn.commit()

        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO animais (id_animal, id_tutor, id_animal, nome, especie, raca, ano_nascimento, sexo, peso, cor)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_animal
        """)

        cursor.execute(query, (id_animal, id_tutor, id_animal, nome, especie, raca, ano_nascimento, sexo, peso, cor))
        id_animal = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()

        return id_animal
