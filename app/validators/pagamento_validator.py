from datetime import datetime

class PagamentoValidator:
    @staticmethod
    def validar_criar_pagamento(data):
        """Valida os campos ao criar um pagamento."""
        # Campos obrigatórios
        campos_obrigatorios = ['id_consulta', 'valor', 'data_pagamento', 'id_meio_pagamento']
        for campo in campos_obrigatorios:
            if campo not in data or not data[campo]:
                return False, f"Campo obrigatório faltando: {campo}"

        # Validar valor (NUMERIC(15, 2))
        try:
            valor = float(data['valor'])
            if valor <= 0:
                return False, "Campo 'valor' deve ser um número positivo."
        except ValueError:
            return False, "Campo 'valor' deve ser um número válido."

        # Validar data_pagamento (formato DD/MM/YYYY)
        try:
            data_pagamento = datetime.strptime(data['data_pagamento'], '%d/%m/%Y').date()
        except ValueError:
            return False, "Campo 'data_pagamento' deve estar no formato DD/MM/YYYY."

        return True, None