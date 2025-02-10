// FUNCOES DE BUSCAR TUTOR
    // buscar tutor a partir de seu cpf
export function buscarTutorCpf(cpf) {
    return fetch("/api/tutores")
        .then(response => response.json())
        .then(tutores => tutores.find(tutor => tutor.cpf === cpf))
        .catch(error => console.error("Erro ao buscar tutor: ", error));
}
    // buscar cpf do tutor a partir de seu id
export function buscarCpfPorId(id) {
    return fetch("/api/tutores")
        .then(response => response.json())
        .then(tutores => {
            const tutor = tutores.find(tutor => tutor.id === parseInt(id));
            return tutor ? tutor.cpf : null;
        })
        .catch(error => console.error("Erro ao buscar CPF do tutor: ", error));
}
    // buscar nome do tutor a partir de seu id
export function buscarNomeIdTutor(id) {
    return fetch("/api/tutores")
        .then(response => response.json())
        .then(tutores => {
            const tutor = tutores.find(tutor => tutor.id === parseInt(id));

            return tutor ? tutor.nome : null;
        })
        .catch(error => console.error("Erro ao buscar nome do tutor: ", error));
}
    // buscar o objeto tutor a partir de seu id
export function getTutor(id) {
    return fetch("/api/tutores")
        .then(response => response.json())
        .then(tutores => tutores.find(tutor => tutor.id === parseInt(id)))
        .catch(error => console.error("Erro ao buscar tutor: ", error));
}

// FUNCOES DE BUSCAR PACIENTE
    // buscar o objeto paciente a partir de seu id
export function getPaciente(id) {
    return fetch("/api/pacientes")
        .then(response => response.json())
        .then(pacientes => pacientes.find(paciente => paciente.id === parseInt(id)))
        .catch(error => console.error("Erro ao buscar paciente: ", error));
}
    // buscar o nome do paciente a partir de seu id
export function buscarNomeIdPaciente(id) {
    return fetch("/api/pacientes")
        .then(response => response.json())
        .then(pacientes => {
            const paciente = pacientes.find(paciente => paciente.id === parseInt(id));
            return paciente ? paciente.nome : null;
        })
        .catch(error => {
            console.error("Erro ao buscar nome do paciente: ", error);
            return "Erro";
        });
}
    // buscar todos os pacientes com o id do tutor
export function buscarPacientesPorTutor(id) {
    return fetch("/api/pacientes")
        .then(response => response.json())
        .then(pacientes => pacientes.filter(paciente => paciente.tutor === parseInt(id)))
        .catch(error => console.error("Erro ao buscar pacientes do tutor: ", error));
}

// FUNCOES DE BUSCAR USUÁRIO

// FUNCOES DE BUSCAR AGENDAMENTO
    // buscar o objeto agendamento a partir de seu id
export function getAgendamento(id) {
    return fetch("/api/agendamentos")
        .then(response => response.json())
        .then(agendamentos => agendamentos.find(agendamento => agendamento.id === parseInt(id)))
        .catch(error => console.error("Erro ao buscar agendamento: ", error));
}

// FUNCOES DE BUSCAR STATUS
    // buscar o nome do status a partir de seu id
export function buscarNomeStatus(id) {
    return fetch("/api/status")
        .then(response => response.json())
        .then(status => {
            const statusObj = status.find(s => s.id === parseInt(id));
            return statusObj ? statusObj.nome : "Sem status";
        })
        .catch(error => console.error("Erro ao buscar nome do status: ", error));
}



window.buscarNomeIdTutor = buscarNomeIdTutor; // Adiciona a função ao escopo global