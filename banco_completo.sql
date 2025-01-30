-- Nome do banco de dados: med_vet_bd
-- Codificação: UTF-8
-- Região: Brasil (pt_BR)
-- Porta padrão: 5432 (PostgreSQL)
-- Propósito: Banco de dados para sistema de gestão de clínica veterinária

-- Criação do banco de dados
CREATE DATABASE med_vet_bd
    ENCODING 'UTF8'
    LC_COLLATE 'pt_BR.UTF-8'
    LC_CTYPE 'pt_BR.UTF-8'
    TEMPLATE template0;

-- Conecta ao banco de dados med_vet_bd
\c med_vet_bd;

-- Configurações adicionais do banco de dados
SET client_encoding = 'UTF8';
SET TIMEZONE = 'America/Sao_Paulo'; -- Fuso horário do Brasil

-- Permissões e roles (opcional, dependendo do ambiente)
-- Cria um role específico para o banco de dados (substitua 'med_vet_user' e 'senha_segura' conforme necessário)
CREATE ROLE med_vet_user WITH LOGIN PASSWORD 'senha_segura';
GRANT ALL PRIVILEGES ON DATABASE med_vet_bd TO med_vet_user;

-- Configurações de extensões (opcional, se necessário)
-- Exemplo: Habilita a extensão pgcrypto para criptografia
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Configurações de tabelas e esquemas (opcional)
-- Cria um esquema específico para organizar as tabelas (substitua 'vet_schema' pelo nome desejado)
CREATE SCHEMA IF NOT EXISTS vet_schema;
SET search_path TO vet_schema;

-- Comentários adicionais
COMMENT ON DATABASE med_vet_bd IS 'Banco de dados para gestão de clínica veterinária.';


CREATE TABLE animais (
    id_animal SERIAL PRIMARY KEY,
    id_tutor INTEGER NOT NULL,
    nome VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raca VARCHAR(50),
    ano_nascimento INTEGER,
    sexo VARCHAR(1),
    peso FLOAT,
    cor VARCHAR(50),
    CONSTRAINT fk_tutor FOREIGN KEY (id_tutor) REFERENCES tutores(id_tutor)
);


CREATE TABLE tutores (
    id_tutor SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE,
    telefone VARCHAR(15),
    endereço VARCHAR(200),
    email VARCHAR(100) UNIQUE
);


CREATE TABLE Veterinarios (
    id_veterinario CHAR(11) PRIMARY KEY,  -- CPF do veterinário
    nome VARCHAR(90) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    endereco VARCHAR(120) NOT NULL,
    email VARCHAR(100) NOT NULL,
    crmv CHAR(9) NOT NULL UNIQUE          -- Formato: XX (estado) + 7 dígitos
);

CREATE TABLE Especialidades (
    id_especialidade SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Veterinarios_Especialidades (
    id_veterinario CHAR(11) REFERENCES Veterinarios(id_veterinario),
    id_especialidade INT REFERENCES Especialidades(id_especialidade),
    PRIMARY KEY (id_veterinario, id_especialidade)
);


CREATE TABLE consultas (
    id_consulta SERIAL PRIMARY KEY,
    id_animal INTEGER NOT NULL,
    id_veterinario VARCHAR(11) NOT NULL,
    data DATE NOT NULL,
    horario TIME NOT NULL,
    id_tipo INTEGER NOT NULL,
    CONSTRAINT fk_animal FOREIGN KEY (id_animal) REFERENCES animais(id_animal),
    CONSTRAINT fk_veterinario FOREIGN KEY (id_veterinario) REFERENCES veterinarios(id_veterinario),
    CONSTRAINT fk_tipo FOREIGN KEY (id_tipo) REFERENCES tipos_consultas(id_tipo)
);

CREATE TABLE tipos_consultas (
    id_tipo SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    categoria VARCHAR(50),
    descricao TEXT
);


CREATE TABLE tratamentos (
    id_tratamento SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    tipo_tratamento VARCHAR(50) NOT NULL,
    descricao TEXT NOT NULL,
    duracao_estimada VARCHAR(50) NOT NULL,
    data_inicio DATE NOT NULL,
    CONSTRAINT fk_consulta FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta)
);


CREATE TABLE exames (
    id_exame SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    id_animal INTEGER NOT NULL,
    id_tipo_exame INTEGER NOT NULL,
    resultado TEXT,
    data_exame DATE NOT NULL,
    observacoes VARCHAR(150),
    CONSTRAINT fk_consulta FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta),
    CONSTRAINT fk_animal FOREIGN KEY (id_animal) REFERENCES animais(id_animal),
    CONSTRAINT fk_tipo_exame FOREIGN KEY (id_tipo_exame) REFERENCES tipos_exames(id_tipo_exame)
);

CREATE TABLE tipos_exames (
    id_tipo_exame SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    descricao TEXT
);


CREATE TABLE medicamentos (
    id_medicamento SERIAL PRIMARY KEY,
    nome VARCHAR(70) NOT NULL,
    descricao VARCHAR(150) NOT NULL,
    quantidade INTEGER NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    uso VARCHAR(25) NOT NULL
);

CREATE TABLE receitas_medicas (
    id_receita SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    id_tratamento INTEGER NOT NULL,
    id_veterinario VARCHAR(11) NOT NULL,
    data DATE NOT NULL,
    observacoes VARCHAR(150),
    CONSTRAINT fk_consulta FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta),
    CONSTRAINT fk_tratamento FOREIGN KEY (id_tratamento) REFERENCES tratamentos(id_tratamento),
    CONSTRAINT fk_veterinario FOREIGN KEY (id_veterinario) REFERENCES veterinarios(id_veterinario)
);

CREATE TABLE receita_medicamento (
    id_receita INTEGER NOT NULL,
    id_medicamento INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    tipo_quantidade VARCHAR(5) NOT NULL,
    frequencia VARCHAR(25) NOT NULL,
    duracao VARCHAR(75) NOT NULL,
    PRIMARY KEY (id_receita, id_medicamento),
    CONSTRAINT fk_receita FOREIGN KEY (id_receita) REFERENCES receitas_medicas(id_receita),
    CONSTRAINT fk_medicamento FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id_medicamento)
);


CREATE TABLE pagamentos (
    id_pagamento SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    valor NUMERIC(15, 2) NOT NULL,
    data_pagamento DATE NOT NULL,
    id_meio_pagamento INTEGER NOT NULL,
    CONSTRAINT fk_consulta FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta),
    CONSTRAINT fk_meio_pagamento FOREIGN KEY (id_meio_pagamento) REFERENCES meios_pagamentos(id_meio_pagamento)
);

CREATE TABLE meios_pagamentos (
    id_meio_pagamento SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);


CREATE TABLE agendamentos (
    id_agendamento SERIAL PRIMARY KEY,
    id_tutor INTEGER NOT NULL,
    id_animal INTEGER NOT NULL,
    data DATE NOT NULL,
    hora TIME NOT NULL,
    id_status INTEGER NOT NULL,
    CONSTRAINT fk_tutor FOREIGN KEY (id_tutor) REFERENCES tutores(id_tutor),
    CONSTRAINT fk_animal FOREIGN KEY (id_animal) REFERENCES animais(id_animal),
    CONSTRAINT fk_status FOREIGN KEY (id_status) REFERENCES status(id_status)
);

CREATE TABLE status (
    id_status SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);