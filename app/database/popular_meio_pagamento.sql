INSERT INTO meio_pagamento (nome)
SELECT unnest(ARRAY[
    'Dinheiro',
    'Cartão de Crédito',
    'Cartão de Débito',
    'Pix',
    'Transferência Bancária'
        ])
WHERE NOT EXISTS (SELECT 1 FROM meio_pagamento); -- Apenas insere se a tabela estiver vazia