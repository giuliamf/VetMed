from datetime import datetime

pacientes = [
    {'id': 1, 'nome': 'Marley', 'tutor': 1, 'especie': 'Cachorro', 'raca':
        'Labrador', 'nascimento': '02-05-2018', 'sexo': 'M', 'peso': 10, 'cor': 'Preto'},
    {'id': 2, 'nome': 'Catherine', 'tutor': 3, 'especie': 'Gato', 'raca':
        'SRD', 'nascimento': '15-08-2019', 'sexo': 'F', 'peso': 5, 'cor': 'Branco'},
    {'id': 3, 'nome': 'Thor', 'tutor': 2, 'especie': 'Cachorro', 'raca': 'Pitbull',
     'nascimento': '10-10-2017', 'sexo': 'M', 'peso': 15, 'cor': 'Marrom'},
    {'id': 4, 'nome': 'Mel', 'tutor': 4, 'especie': 'Cachorro', 'raca': 'Poodle',
     'nascimento': '25-12-2016', 'sexo': 'F', 'peso': 7.200, 'cor': 'Branco'},
    {'id': 5, 'nome': 'Rex', 'tutor': 5, 'especie': 'Cachorro', 'raca': 'SRD',
     'nascimento': '30-07-2019', 'sexo': 'M', 'peso': 8, 'cor': 'Preto'}
]

tutores = [
    {'id': 1, 'nome': 'Ana Luiza Campos', 'cpf': '123.456.789-00', 'nascimento': '02-05-1995', 'telefone':
        '(61) 99999-9999', 'endereco': {'bairro': 'Asa Sul', 'cidade': 'Brasília', 'estado': 'DF'}},
    {'id': 2, 'nome': 'João Pedro Souza', 'cpf': '456.789.123-00', 'nascimento': '10-10-1996', 'telefone':
        '(61) 77777-7777', 'endereco': {'bairro': 'Taguatinga', 'cidade': 'Brasília', 'estado': 'DF'}},
    {'id': 3, 'nome': 'Célio Eduardo Júnior', 'cpf': '987.654.321-00', 'nascimento': '15-08-1994', 'telefone':
        '(61) 88888-8888', 'endereco': {'bairro': 'Samambaia', 'cidade': 'Brasília', 'estado': 'DF'}},
    {'id': 4, 'nome': 'Fernanda Oliveira', 'cpf': '789.123.456-00', 'nascimento': '25-12-1997', 'telefone':
        '(61) 66666-6666', 'endereco': {'bairro': 'Ceilândia', 'cidade': 'Brasília', 'estado': 'DF'}},
    {'id': 5, 'nome': 'Carlos Eduardo Santos', 'cpf': '321.654.987-00', 'nascimento': '30-07-1998', 'telefone':
        '(61) 55555-4444', 'endereco': {'bairro': 'Asa Norte', 'cidade': 'Brasília', 'estado': 'DF'}}
]

usuarios = [
    {'id': 1, 'nome': 'Giulia Moura Ferreira', 'email': 'giulia@gmail.com', 'cargo': 'vet', 'especialidade': 1, 'senha':
        'e4c2eed8a6df0147265631e9ff25b70fd0e4b3a246896695b089584bf3ce8b90'},
    {'id': 2, 'nome': 'Célio Eduardo Júnior', 'email': 'celio@gmail.com', 'cargo': 'sec', 'senha':
        '60fe67ed8156498b9a17f3d983bcf3961d7aa8c36e33bf2edf2ccf1706d33fef'},
    {'id': 3, 'nome': 'Ana Luiza Campos', 'email': 'analuiza@gmail.com', 'cargo': 'vet', 'especialidade': 2,
     'senha': '0a3fa8009c0f56804c7bee62f18836d7bf84743d7ba2b2d0fb151e03b71a6b81'},
]

especialidades = [
    {'id': 1, 'nome': 'Clínica Geral'},
    {'id': 2, 'nome': 'Ortopedia'},
    {'id': 3, 'nome': 'Dermatologia'},
    {'id': 4, 'nome': 'Oftalmologia'},
    {'id': 5, 'nome': 'Cardiologia'},
    {'id': 6, 'nome': 'Cirurgia'}
]

agendamento = [
    {'id': 1, 'hora': '11:20', 'data': datetime.strptime('19/02/2025', '%d/%m/%Y'), 'paciente': 4,
     'tutor': 4, 'status': 1},
    {'id': 2, 'hora': '14:30', 'data': datetime.strptime('19/02/2025', '%d/%m/%Y'), 'paciente': 2,
     'tutor': 3, 'status': 1},
    {'id': 3, 'hora': '09:00', 'data': datetime.strptime('19/02/2025', '%d/%m/%Y'), 'paciente': 1,
     'tutor': 1, 'status': 1},
    {'id': 4, 'hora': '15:00', 'data': datetime.strptime('10/02/2025', '%d/%m/%Y'), 'paciente': 3,
     'tutor': 2, 'status': 1}
]

status = [
    {'id': 1, 'nome': 'Agendado'},
    {'id': 2, 'nome': 'Em andamento'},
    {'id': 3, 'nome': 'Realizado'},
    {'id': 4, 'nome': 'Cancelado'}
]
