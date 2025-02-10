import psycopg2
from psycopg2 import sql
from datetime import datetime
from app.validators.animal_validator import AnimalValidator

def get_db_connection():
    conn = psycopg2.connect(
        dbname='your_dbname',
        user='your_user',
        password='your_password',
        host='your_host',
        port='your_port'
    )
    return conn

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
        id_tutor = data['id_tutor']
        nome = data['nome']
        especie = data['especie']
        raca = data['raca']
        ano_nascimento = data['ano_nascimento']
        sexo = data['sexo']
        peso = data['peso']
        cor = data['cor']

        # Inserir no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO animal (id_tutor, nome, especie, raca, ano_nascimento, sexo, peso, cor)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_animal
        """
        cursor.execute(query, (id_tutor, nome, especie, raca, ano_nascimento, sexo, peso, cor))
        id_animal = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return id_animal

    @staticmethod
    def buscar_animal_por_id(id_animal):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT * FROM animal WHERE id_animal = %s
        """
        cursor.execute(query, (id_animal,))
        animal = cursor.fetchone()
        cursor.close()
        conn.close()
        if animal:
            return Animal(*animal)
        return None

    @staticmethod
    def atualizar_animal(id_animal, **kwargs):
        """
        Atualiza os campos fornecidos em kwargs para o animal com o id_animal especificado.
        """
        # Validar os dados
        valido, mensagem = AnimalValidator.validar_atualizar_animal(kwargs)
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
        valores.append(id_animal)  # Adicionar o id_animal no final

        query = sql.SQL("""
            UPDATE animal
            SET {campos}
            WHERE id_animal = %s
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
    def deletar_animal(id_animal):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            DELETE FROM animal WHERE id_animal = %s
        """
        cursor.execute(query, (id_animal,))
        conn.commit()
        cursor.close()
        conn.close()