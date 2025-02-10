from app.validators.base_validator import BaseValidator


class AnimalValidator(BaseValidator):
    @staticmethod
    def validar_criar_animal(data):
        # Campos obrigatórios
        campos_obrigatorios = ['cpf_tutor', 'nome', 'especie', 'cor']
        valido, mensagem = BaseValidator.validar_campos_obrigatorios(data, campos_obrigatorios)
        if not valido:
            return False, mensagem

        # Validar ID Tutor (CPF)
        valido, mensagem = BaseValidator.validar_formato_cpf(data, 'cpf_tutor')
        if not valido:
            return False, mensagem

        # Validar Nome (char de 80 caracteres)
        valido, mensagem = BaseValidator.validar_tamanho_string(data, 'nome', 80)
        if not valido:
            return False, mensagem

        # Validar Espécie (char de 25 caracteres)
        valido, mensagem = BaseValidator.validar_tamanho_string(data, 'especie', 25)
        if not valido:
            return False, mensagem

        # Validar Raça (char de 25 caracteres)
        valido, mensagem = BaseValidator.validar_tamanho_string(data, 'raca', 25)
        if not valido:
            return False, mensagem

        # Validar Ano de Nascimento (inteiro de 4 dígitos)
        valido, mensagem = BaseValidator.validar_ano_nascimento(data, 'ano_nascimento')
        if not valido:
            return False, mensagem

        # Validar Sexo (char de 1 caractere)
        if 'sexo' in data:
            sexo = data['sexo']
            if not isinstance(sexo, str) or len(sexo) != 1 or sexo.upper() not in ['M', 'F']:
                return False, "Campo sexo deve ser 'M' ou 'F'"

        # Validar Peso (float com até 3 dígitos inteiros e 2 decimais)
        valido, mensagem = BaseValidator.validar_peso(data, 'peso')
        if not valido:
            return False, mensagem

        # Validar Cor (char de 25 caracteres)
        valido, mensagem = BaseValidator.validar_tamanho_string(data, 'cor', 25)
        if not valido:
            return False, mensagem

        return True, None