INSERT INTO especialidade (nome)
SELECT unnest(ARRAY[
    'Clínico Geral',
    'Cirurgia',
    'Cardiologia',
    'Dermatologia',
    'Odontologia',
    'Oftalmologia'
        ])
WHERE NOT EXISTS (SELECT 1 FROM especialidade); -- Apenas insere se a tabela estiver vazia
