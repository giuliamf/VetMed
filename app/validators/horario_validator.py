from datetime import time
from app.models.consulta import Consulta

class HorarioValidator:
    @staticmethod
    def validar_horario(horario):
        """Valida o formato e o intervalo do horário."""
        try:
            horas, minutos = map(int, horario.split(':'))
            horario_obj = time(horas, minutos)
            if not (7 <= horas < 19):
                return False, "Horário deve estar entre 07:00 e 19:00."
            return True, None
        except ValueError:
            return False, "Horário deve estar no formato HH:MM."

    @staticmethod
    def verificar_conflito_horario(id_veterinario, data, horario):
        """Verifica se já existe uma consulta para o mesmo veterinário no mesmo dia e horário."""
        consulta_existente = Consulta.query.filter_by(
            id_veterinario=id_veterinario,
            data=data,
            horario=horario
        ).first()
        if consulta_existente:
            return False, "Já existe uma consulta para este veterinário no mesmo dia e horário."
        return True, None