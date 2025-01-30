from datetime import datetime

class ExameValidator:
    @staticmethod
    def validar_criar_exame(data):
        """Valida os campos ao criar um exame."""
        # Campos obrigatórios
        campos_obrigatorios = ['id_consulta', 'id_animal', 'id_tipo_exame', 'data_exame']
        for campo in campos_obrigatorios:
            if campo not in data or not data[campo]:
                return False, f"Campo obrigatório faltando: {campo}"

        # Validar data_exame (formato DD/MM/YYYY)
        try:
            data_exame = datetime.strptime(data['data_exame'], '%d/%m/%Y').date()
        except ValueError:
            return False, "Campo 'data_exame' deve estar no formato DD/MM/YYYY."

        # Validar resultado (opcional, até 500 caracteres)
        if 'resultado' in data and len(data['resultado']) > 500:
            return False, "Campo 'resultado' deve ter no máximo 500 caracteres."

        # Validar observacoes (opcional, até 150 caracteres)
        if 'observacoes' in data and len(data['observacoes']) > 150:
            return False, "Campo 'observacoes' deve ter no máximo 150 caracteres."

        return True, None
    