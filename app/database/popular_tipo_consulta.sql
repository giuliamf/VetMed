INSERT INTO tipo_consulta (nome)
SELECT unnest(ARRAY[
    'Consulta',
    'Exame Laboratorial',
    'Exame de Imagem',
    'Cirurgia'
    ])
WHERE NOT EXISTS (SELECT 1 FROM tipo_consulta); -- Apenas insere se a tabela estiver vazia
