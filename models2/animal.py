from app import db
from app.validators import AnimalValidator


class Animal:    
    def __repr__(self):
        return f"<Animal {self.nome}>"
    
        def __init__(self, id_animal, id_tutor, id_animal, nome, especie, raca, ano_nascimento, sexo, peso, cor):
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
        id_animal = data['id_animal']
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

    def atualizar_animal(id_animal, **kwargs):
            """
            Atualiza os campos fornecidos em kwargs para o agendamento com o id_agendamento especificado.
            """
            # Validar os dados
            valido, mensagem = AnimalValidator.validar_atualizar_animal(kwargs)
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
            valores.append(id_animal)  # Adicionar o id_agendamento no final

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

      def deletar_animal(id_animal):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            DELETE FROM animal WHERE id_animal = %s
        """)
        cursor.execute(query, (id_animal,))
        conn.commit()
        cursor.close()
        conn.close()