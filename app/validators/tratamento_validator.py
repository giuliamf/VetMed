from datetime import datetime

class TratamentoValidator:
    @staticmethod
    def validar_criar_tratamento(data):
        """Valida os campos ao criar um tratamento."""
        # Campos obrigatórios
        campos_obrigatorios = ['id_consulta', 'tipo_tratamento', 'descricao', 'duracao_estimada', 'data_inicio']
        for campo in campos_obrigatorios:
            if campo not in data or not data[campo]:
                return False, f"Campo obrigatório faltando: {campo}"

        # Validar tipo_tratamento (char de até 50 caracteres)
        if len(data['tipo_tratamento']) > 50:
            return False, "Campo 'tipo_tratamento' deve ter no máximo 50 caracteres."

        # Validar descricao (texto de até 500 caracteres)
        if len(data['descricao']) > 500:
            return False, "Campo 'descricao' deve ter no máximo 500 caracteres."

        # Validar duracao_estimada (char de até 50 caracteres)
        if len(data['duracao_estimada']) > 50:
            return False, "Campo 'duracao_estimada' deve ter no máximo 50 caracteres."

        # Validar data_inicio (formato DD/MM)
        try:
            data_inicio = datetime.strptime(data['data_inicio'], '%d/%m').date()
        except ValueError:
            return False, "Campo 'data_inicio' deve estar no formato DD/MM."

        return True, None