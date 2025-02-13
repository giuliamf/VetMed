INSERT INTO Horario_Funcionamento (horario, turno)
SELECT * FROM unnest(
    ARRAY['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
          '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30'],
    ARRAY['manha', 'manha', 'manha', 'manha', 'manha', 'manha', 'manha', 'manha',
          'tarde', 'tarde', 'tarde', 'tarde', 'tarde', 'tarde', 'tarde', 'tarde']
)
WHERE NOT EXISTS (SELECT 1 FROM Horario_Funcionamento);
