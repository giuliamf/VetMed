INSERT INTO status_agendamento (nome)
SELECT unnest(ARRAY[
    'Agendado',
    'Cancelado'
        ])
WHERE NOT EXISTS (SELECT 1 FROM status_agendamento); -- Apenas insere se a tabela estiver vazia
