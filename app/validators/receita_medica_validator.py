from datetime import datetime

class ReceitaMedicaValidator:
    @staticmethod
    def validar_criar_receita_medica(data):
        """Valida os campos ao criar uma receita médica."""
        # Campos obrigatórios
        campos_obrigatorios = ['id_consulta', 'id_tratamento', 'id_veterinario', 'data']
        for campo in campos_obrigatorios:
            if campo not in data or not data[campo]:
                return False, f"Campo obrigatório faltando: {campo}"

        # Validar data (formato DD/MM/YYYY)
        try:
            data_receita = datetime.strptime(data['data'], '%d/%m/%Y').date()
        except ValueError:
            return False, "Campo 'data' deve estar no formato DD/MM/YYYY."

        # Validar observacoes (opcional, até 150 caracteres)
        if 'observacoes' in data and len(data['observacoes']) > 150:
            return False, "Campo 'observacoes' deve ter no máximo 150 caracteres."

        return True, None