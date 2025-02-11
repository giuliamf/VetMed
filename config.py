import psycopg2


def create_database(firstcursor, db_name='vetmed'):
    """ Cria o banco de dados caso ele não exista """
    try:
        firstcursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
        exists = firstcursor.fetchone()

        if not exists:
            firstcursor.execute(f"CREATE DATABASE {db_name} "
                           f"ENCODING 'UTF8' "
                           f"LC_COLLATE 'pt_BR.UTF-8' "
                           f"LC_CTYPE 'pt_BR.UTF-8' "
                           f"TEMPLATE template0;")
            print(f'Banco de dados >{db_name}< criado com sucesso!')
        else:
            print(f'Banco de dados >{db_name}< já existe!')
    except Exception as e:
        print(f'Erro ao criar o banco de dados: {e}')


# Conecta ao banco de dados padrão (postgres)
first_connection = psycopg2.connect(
    dbname="postgres",  # Conecta ao banco de dados padrão
    user="postgres",    # Substitua pelo seu usuário
    password="giulia",  # Substitua pela sua senha
    host="localhost",
    port="5432"
)
print("Conectado ao banco de dados padrão com sucesso!")
first_connection.autocommit = True
first_cursor = first_connection.cursor()

print("Criando o VetMed...")
create_database(first_cursor)     # Criando o bd vetmed

print("Conectando com o vetmed...")


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:giulia@localhost:5432/vetmed'  # Modifique com suas credenciais
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Evita avisos desnecessários

