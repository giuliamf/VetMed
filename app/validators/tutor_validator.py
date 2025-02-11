from app.validators.base_validator import BaseValidator

class TutorValidator(BaseValidator):
    @staticmethod
    def validar_criar_tutor(data):
        # Campos obrigatórios
        campos_obrigatorios = ['cpf_tutor', 'nome', 'data_nascimento', 'telefone', 'endereço', 'email']
        valido, mensagem = BaseValidator.validar_campos_obrigatorios(data, campos_obrigatorios)
        if not valido:
            return False, mensagem

        # Validar ID Tutor (CPF)
        valido, mensagem = BaseValidator.validar_formato_cpf(data, 'cpf_tutor')
        if not valido:
            return False, mensagem

        # Validar Nome (char de até 90 caracteres)
        valido, mensagem = BaseValidator.validar_tamanho_string(data, 'nome', 90)
        if not valido:
            return False, mensagem

        # Validar Data de Nascimento (formato DD/MM/YYYY e data válida)
        valido, mensagem = BaseValidator.validar_data_nascimento(data, 'data_nascimento')
        if not valido:
            return False, mensagem

        # Validar Telefone (formato +XX XX XXXX-XXXX ou +XX XX XXXXX-XXXX)
        valido, mensagem = BaseValidator.validar_telefone(data, 'telefone')
        if not valido:
            return False, mensagem

        # Validar Endereço (char de até 120 caracteres)
        valido, mensagem = BaseValidator.validar_tamanho_string(data, 'endereço', 120)
        if not valido:
            return False, mensagem

        # Validar Email (formato de e-mail válido)
        valido, mensagem = BaseValidator.validar_email(data, 'email')
        if not valido:
            return False, mensagem

        return True, None