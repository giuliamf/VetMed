from app.database import execute_sql


class Animal:
    def __init__(self, id_animal, id_tutor, nome, especie, raca, nascimento, sexo, peso, cor):
        self.id_animal = id_animal
        self.id_tutor = id_tutor
        self.nome = nome
        self.especie = especie
        self.raca = raca
        self.nascimento = nascimento
        self.sexo = sexo
        self.peso = peso
        self.cor = cor

    @staticmethod
    def criar_animal(data):
        """
        Cria um novo animal no banco de dados, verificando se o tutor existe antes.
        """
        cpf_tutor = data['cpf_tutor']

        # Verificar se o tutor existe no banco de dados
        query_tutor = "SELECT id_tutor FROM Tutor WHERE cpf = %s"  # Pega o id do tutor de acordo com o cpf dele
        tutor = execute_sql(query_tutor, (cpf_tutor,), fetch_one=True)

        if not tutor:
            raise ValueError("Tutor não encontrado. Cadastre o tutor primeiro.")

        # Criar o animal no banco
        query = """
            INSERT INTO Animal (id_tutor, nome, especie, raca, nascimento, sexo, peso, cor)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_animal
        """
        id_animal = execute_sql(query, (tutor[0], data['nome'], data['especie'], data['raca'],
                                        data['nascimento'], data['sexo'], data['peso'], data['cor']), fetch_one=True)

        return id_animal[0] if id_animal else None

    @staticmethod
    def buscar_animal_por_id(id_animal):
        """
        Busca um animal no banco de dados pelo ID e retorna junto com o nome do tutor.
        """
        query = """
            SELECT a.*, t.cpf, t.nome AS nome_tutor
            FROM Animal a
            JOIN Tutor t ON a.id_tutor = t.id_tutor
            WHERE a.id_animal = %s
        """
        animal = execute_sql(query, (id_animal,), fetch_one=True)

        if animal:
            return {
                "id_animal": animal[0],
                "id_tutor": animal[1],
                "nome": animal[2],
                "especie": animal[3],
                "raca": animal[4],
                "nascimento": animal[5],
                "sexo": animal[6],
                "peso": animal[7],
                "cor": animal[8],
                "cpf_tutor": animal[9],
                "nome_tutor": animal[10]
            }
        return None

    @staticmethod
    def buscar_todos_animais():
        """
        Retorna todos os animais com o nome do tutor associado.
        """
        query = """
            SELECT a.id_animal, a.nome, t.nome AS nome_tutor
            FROM Animal a
            JOIN Tutor t ON a.id_tutor = t.id_tutor
        """
        animais = execute_sql(query, fetch_all=True)

        return [{"id_animal": a[0], "nome": a[1], "tutor": a[2]} for a in animais] if animais else []

    @staticmethod
    def atualizar_animal(id_animal, data):
        """
        Atualiza os dados de um animal. Se o tutor for alterado, verifica se o CPF já está cadastrado.
        """
        cpf_tutor = data.get("cpf_tutor")

        if cpf_tutor:
            # Verificar se o CPF do tutor existe no banco de dados
            query_tutor = "SELECT id_tutor FROM Tutor WHERE cpf = %s"
            tutor = execute_sql(query_tutor, (cpf_tutor,), fetch_one=True)

            if not tutor:
                raise ValueError("O CPF informado não pertence a um tutor cadastrado.")

        # Construir a query dinamicamente
        campos = []
        valores = []

        for campo, valor in data.items():
            if campo == "cpf_tutor":
                campos.append("id_tutor")
                valores.append(tutor[0])  # Usa o ID do tutor, não o CPF
            else:
                campos.append(campo)
                valores.append(valor)

        valores.append(id_animal)  # Adiciona o ID do animal para a cláusula WHERE

        query = f"""
                   UPDATE Animal
                   SET {', '.join([f"{campo} = %s" for campo in campos])}
                   WHERE id_animal = %s
               """

        execute_sql(query, tuple(valores))
