INSERT INTO status_agendamento (nome)
SELECT unnest(ARRAY[
    'Agendado',
    'Em atendimento',
    'Cancelado',
    'Finalizado'
        ])
WHERE NOT EXISTS (SELECT 1 FROM status_agendamento); -- Apenas insere se a tabela estiver vazia
