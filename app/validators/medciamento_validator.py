class MedicamentoValidator:
    @staticmethod
    def validar_criar_medicamento(data):
        """Valida os campos ao criar um medicamento."""
        # Campos obrigatórios
        campos_obrigatorios = ['nome', 'descricao', 'quantidade', 'tipo', 'uso']
        for campo in campos_obrigatorios:
            if campo not in data or not data[campo]:
                return False, f"Campo obrigatório faltando: {campo}"

        # Validar nome (char de até 70 caracteres)
        if len(data['nome']) > 70:
            return False, "Campo 'nome' deve ter no máximo 70 caracteres."

        # Validar descricao (char de até 150 caracteres)
        if len(data['descricao']) > 150:
            return False, "Campo 'descricao' deve ter no máximo 150 caracteres."

        # Validar quantidade (inteiro)
        if not isinstance(data['quantidade'], int) or data['quantidade'] < 0:
            return False, "Campo 'quantidade' deve ser um número inteiro positivo."

        # Validar tipo (char de até 20 caracteres)
        if len(data['tipo']) > 20:
            return False, "Campo 'tipo' deve ter no máximo 20 caracteres."

        # Validar uso (char de até 25 caracteres)
        if len(data['uso']) > 25:
            return False, "Campo 'uso' deve ter no máximo 25 caracteres."

        return True, None