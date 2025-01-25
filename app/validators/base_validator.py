from datetime import datetime
from flask import jsonify

class BaseValidator:
    @staticmethod
    def validar_campos_obrigatorios(data, campos_obrigatorios):
        """Verifica se todos os campos obrigatórios estão presentes."""
        for campo in campos_obrigatorios:
            if campo not in data or data[campo] is None:
                return False, f"Campo obrigatório faltando: {campo}"
        return True, None

    @staticmethod
    def validar_tipo(data, campo, tipo):
        """Valida o tipo de um campo."""
        if campo in data and not isinstance(data[campo], tipo):
            return False, f"Campo {campo} deve ser do tipo {tipo.__name__}"
        return True, None

    @staticmethod
    def validar_data(data, campo, formato='%Y-%m-%d'):
        """Valida se um campo é uma data válida."""
        if campo in data:
            try:
                datetime.strptime(data[campo], formato)
            except ValueError:
                return False, f"Campo {campo} deve ser uma data no formato {formato}"
        return True, None

    @staticmethod
    def validar_email(data, campo):
        """Valida se um campo é um e-mail válido."""
        if campo in data:
            if '@' not in data[campo] or '.' not in data[campo]:
                return False, f"Campo {campo} deve ser um e-mail válido"
        return True, None

    @staticmethod
    def validar_tamanho(data, campo, min_len=None, max_len=None):
        """Valida o tamanho de um campo string."""
        if campo in data:
            valor = data[campo]
            if min_len is not None and len(valor) < min_len:
                return False, f"Campo {campo} deve ter pelo menos {min_len} caracteres"
            if max_len is not None and len(valor) > max_len:
                return False, f"Campo {campo} deve ter no máximo {max_len} caracteres"
        return True, None
    
    @staticmethod
    def validar_tamanho_string(data, campo, max_len):
        """Valida o tamanho máximo de uma string."""
        if campo in data and len(str(data[campo])) > max_len:
            return False, f"Campo {campo} deve ter no máximo {max_len} caracteres"
        return True, None

    @staticmethod
    def validar_formato_cpf(data, campo):
        """Valida se um campo é um CPF válido (11 caracteres numéricos)."""
        if campo in data:
            cpf = str(data[campo])
            if not cpf.isdigit() or len(cpf) != 11:
                return False, f"Campo {campo} deve ser um CPF válido (11 dígitos)"
        return True, None

    @staticmethod
    def validar_data_nascimento(data, campo):
        """Valida se a data de nascimento está no formato DD/MM/YYYY e é válida."""
        if campo in data:
            data_str = data[campo]
            try:
                datetime.strptime(data_str, '%d/%m/%Y')
                dia, mes, ano = map(int, data_str.split('/'))
                if ano < 1880 or ano > datetime.now().year:
                    return False, f"Campo {campo} deve ser um ano entre 1880 e {datetime.now().year}"
                if mes < 1 or mes > 12:
                    return False, f"Campo {campo} deve ser um mês entre 01 e 12"
                if dia < 1 or dia > 31:
                    return False, f"Campo {campo} deve ser um dia entre 01 e 31"
                # Verificar meses com 30 dias
                if mes in [4, 6, 9, 11] and dia > 30:
                    return False, f"Campo {campo}: o mês {mes} só tem 30 dias"
                # Verificar fevereiro e anos bissextos
                if mes == 2:
                    if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
                        if dia > 29:
                            return False, f"Campo {campo}: fevereiro no ano bissexto {ano} só tem 29 dias"
                    else:
                        if dia > 28:
                            return False, f"Campo {campo}: fevereiro no ano {ano} só tem 28 dias"
            except ValueError:
                return False, f"Campo {campo} deve estar no formato DD/MM/YYYY"
        return True, None

    @staticmethod
    def validar_telefone(data, campo):
        """Valida o formato do telefone."""
        if campo in data:
            telefone = data[campo]
            padrao = re.compile(r'^\+\d{2} \d{2} \d{4,5}-?\d{4}$')
            if not padrao.match(telefone):
                return False, f"Campo {campo} deve estar no formato +XX XX XXXX-XXXX ou +XX XX XXXXX-XXXX"
        return True, None

    @staticmethod
    def validar_email(data, campo):
        """Valida o formato do e-mail."""
        if campo in data:
            email = data[campo]
            padrao = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if not padrao.match(email):
                return False, f"Campo {campo} deve ser um e-mail válido"
        return True, None
    
    @staticmethod
    def validar_crmv(data, campo):
        """Valida o formato do CRMV."""
        if campo in data:
            crmv = data[campo]
            if not re.match(r'^\d{2}\d{7}$', crmv):
                return False, f"Campo {campo} deve estar no formato XXYYYYYYY (XX = estado, YYYYYYY = número)"
            estado = int(crmv[:2])
            if estado < 1 or estado > 27:  # 27 estados brasileiros
                return False, f"Campo {campo}: código de estado inválido (deve ser entre 01 e 27)"
        return True, None