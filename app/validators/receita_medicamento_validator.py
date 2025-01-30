class ReceitaMedicamentoValidator:
    @staticmethod
    def validar_criar_receita_medicamento(data):
        """Valida os campos ao criar um registro na tabela Receita_Medicamento."""
        # Campos obrigatórios
        campos_obrigatorios = ['id_receita', 'id_medicamento', 'quantidade', 'tipo_quantidade', 'frequencia', 'duracao']
        for campo in campos_obrigatorios:
            if campo not in data or not data[campo]:
                return False, f"Campo obrigatório faltando: {campo}"

        # Validar quantidade (número de até 4 dígitos)
        if not isinstance(data['quantidade'], int) or data['quantidade'] < 1 or data['quantidade'] > 9999:
            return False, "Campo 'quantidade' deve ser um número inteiro entre 1 e 9999."

        # Validar tipo_quantidade (char de até 5 caracteres)
        if len(data['tipo_quantidade']) > 5:
            return False, "Campo 'tipo_quantidade' deve ter no máximo 5 caracteres."

        # Validar frequencia (char de até 25 caracteres)
        if len(data['frequencia']) > 25:
            return False, "Campo 'frequencia' deve ter no máximo 25 caracteres."

        # Validar duracao (char de até 75 caracteres)
        if len(data['duracao']) > 75:
            return False, "Campo 'duracao' deve ter no máximo 75 caracteres."

        return True, None