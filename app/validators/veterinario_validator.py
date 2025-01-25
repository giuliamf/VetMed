from app.validators.base_validator import BaseValidator

class VeterinarioValidator(BaseValidator):
    @staticmethod
    def validar_criar_veterinario(data):
        # Campos obrigatórios
        campos_obrigatorios = ['id_veterinario', 'nome', 'telefone', 'endereco', 'email', 'crmv']
        valido, mensagem = BaseValidator.validar_campos_obrigatorios(data, campos_obrigatorios)
        if not valido:
            return False, mensagem

        # Validar ID Veterinário (CPF)
        valido, mensagem = BaseValidator.validar_formato_cpf(data, 'id_veterinario')
        if not valido:
            return False, mensagem

        # Validar Nome (char de até 90 caracteres)
        valido, mensagem = BaseValidator.validar_tamanho_string(data, 'nome', 90)
        if not valido:
            return False, mensagem

        # Validar Telefone (formato +XX XX XXXX-XXXX ou +XX XX XXXXX-XXXX)
        valido, mensagem = BaseValidator.validar_telefone(data, 'telefone')
        if not valido:
            return False, mensagem

        # Validar Endereço (char de até 120 caracteres)
        valido, mensagem = BaseValidator.validar_tamanho_string(data, 'endereco', 120)
        if not valido:
            return False, mensagem

        # Validar Email (formato de e-mail válido)
        valido, mensagem = BaseValidator.validar_email(data, 'email')
        if not valido:
            return False, mensagem

        # Validar CRMV (formato XXYYYYYYY)
        valido, mensagem = BaseValidator.validar_crmv(data, 'crmv')
        if not valido:
            return False, mensagem

        return True, None