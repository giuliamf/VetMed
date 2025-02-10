from datetime import datetime

class AgendamentoValidator:
    @staticmethod
    def validar_criar_agendamento(data):
        """Valida os campos ao criar um agendamento."""
        # Campos obrigatórios
        campos_obrigatorios = ['id_animal', 'data', 'hora', 'id_status']
        for campo in campos_obrigatorios:
            if campo not in data or not data[campo]:
                return False, f"Campo obrigatório faltando: {campo}"

        # Validar data (formato DD/MM/YYYY)
        try:
            data_agendamento = datetime.strptime(data['data'], '%d/%m/%Y').date()
        except ValueError:
            return False, "Campo 'data' deve estar no formato DD/MM/YYYY."

        # Validar hora (formato HH:MM)
        try:
            hora_agendamento = datetime.strptime(data['hora'], '%H:%M').time()
        except ValueError:
            return False, "Campo 'hora' deve estar no formato HH:MM."

        return True, None

    @staticmethod
    def validar_atualizar_agendamento(data):
        """
        Valida os campos ao atualizar um agendamento.
        Aceita campos variáveis, mas valida os formatos de 'data' e 'hora', se presentes.
        """
        # Validar data (formato DD/MM/YYYY), se presente
        if 'data' in data:
            try:
                datetime.strptime(data['data'], '%d/%m/%Y').date()
            except ValueError:
                return False, "Campo 'data' deve estar no formato DD/MM/YYYY."

        # Validar hora (formato HH:MM), se presente
        if 'hora' in data:
            try:
                datetime.strptime(data['hora'], '%H:%M').time()
            except ValueError:
                return False, "Campo 'hora' deve estar no formato HH:MM."

        return True, None