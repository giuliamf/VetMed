export function buscarTutorCpf(cpf) {
    return fetch("/api/tutores")
        .then(response => response.json())
        .then(tutores => tutores.find(tutor => tutor.cpf === cpf))
        .catch(error => console.error("Erro ao buscar tutor: ", error));
}


export function buscarCpfPorId(id) {
    return fetch("/api/tutores")
        .then(response => response.json())
        .then(tutores => {
            const tutor = tutores.find(tutor => tutor.id === id);
            return tutor ? tutor.cpf : null;
        })
        .catch(error => console.error("Erro ao buscar CPF do tutor: ", error));
}


export function buscarNomeIdTutor(id) {
    console.log("Chamando API de tutores para ID:", id);

    return fetch("/api/tutores")
        .then(response => response.json())
        .then(tutores => {
            console.log("Tutores recebidos:", tutores);

            const tutor = tutores.find(tutor => tutor.id === id);
            console.log("Tutor encontrado:", tutor);

            return tutor ? tutor.nome : null;
        })
        .catch(error => console.error("Erro ao buscar nome do tutor: ", error));
}


export function getTutor(id) {
    return fetch("/api/tutores")
        .then(response => response.json())
        .then(tutores => tutores.find(tutor => tutor.id === id))
        .catch(error => console.error("Erro ao buscar tutor: ", error));
}

export function buscarPacienteId(id) {
    return fetch("/api/pacientes")
        .then(response => response.json())
        .then(pacientes => pacientes.find(paciente => paciente.id === id))
        .catch(error => console.error("Erro ao buscar paciente: ", error));
}

// Tornar global
window.buscarNomeIdTutor = buscarNomeIdTutor;
