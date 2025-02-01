-- Nome do banco de dados: med_vet_bd
-- Codificação: UTF-8
-- Região: Brasil (pt_BR)
-- Porta padrão: 5432 (PostgreSQL)
-- Propósito: Banco de dados para sistema de gestão de clínica veterinária

-- Configurações adicionais do banco de dados
SET client_encoding = 'UTF8';
SET TIMEZONE = 'America/Sao_Paulo'; -- Fuso horário do Brasil

-- Permissões e roles (opcional, dependendo do ambiente)
-- Cria um role específico para o banco de dados (substitua 'med_vet_user' e 'senha_segura' conforme necessário)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'med_vet_user') THEN
        CREATE ROLE med_vet_user WITH LOGIN PASSWORD 'senha_segura';
    END IF;
END $$;

GRANT ALL PRIVILEGES ON DATABASE med_vet_bd TO med_vet_user;

-- Configurações de extensões (opcional, se necessário)
-- Exemplo: Habilita a extensão pgcrypto para criptografia
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Configurações de tabelas e esquemas (opcional)
-- Cria um esquema específico para organizar as tabelas (substitua 'vet_schema' pelo nome desejado)
CREATE SCHEMA IF NOT EXISTS vet_schema;
SET search_path TO vet_schema;

-- Comentários adicionais
COMMENT ON DATABASE med_vet_bd IS 'Banco de dados para gestão da clínica veterinária MED VET.';


CREATE TABLE IF NOT EXISTS Tutor (
    id_tutor SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE,
    telefone VARCHAR(15),
    endereço VARCHAR(200),
    email VARCHAR(100) UNIQUE
);


CREATE TABLE IF NOT EXISTS Animal (
    id_animal SERIAL PRIMARY KEY,
    id_tutor INTEGER NOT NULL,
    nome VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raca VARCHAR(50),
    ano_nascimento INTEGER,
    sexo VARCHAR(1),
    peso FLOAT,
    cor VARCHAR(50),
    CONSTRAINT fk_tutor FOREIGN KEY (id_tutor) REFERENCES Tutor(id_tutor)
);


CREATE TABLE IF NOT EXISTS Veterinario (
    id_veterinario CHAR(11) PRIMARY KEY,  -- CPF do veterinário
    nome VARCHAR(90) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    endereco VARCHAR(120) NOT NULL,
    email VARCHAR(100) NOT NULL,
    crmv CHAR(9) NOT NULL UNIQUE          -- Formato: XX (estado) + 7 dígitos
);

CREATE TABLE IF NOT EXISTS Especialidade (
    id_especialidade SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Veterinario_Especialidade (
    id_veterinario CHAR(11) REFERENCES Veterinario(id_veterinario),
    id_especialidade INT REFERENCES Especialidade(id_especialidade),
    PRIMARY KEY (id_veterinario, id_especialidade)
);


CREATE TABLE IF NOT EXISTS Tipo_Consulta (
    id_tipo SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    categoria VARCHAR(50),
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS Consulta (
    id_consulta SERIAL PRIMARY KEY,
    id_animal INTEGER NOT NULL,
    id_veterinario VARCHAR(11) NOT NULL,
    data DATE NOT NULL,
    horario TIME NOT NULL,
    id_tipo INTEGER NOT NULL,
    CONSTRAINT fk_animal FOREIGN KEY (id_animal) REFERENCES Animal(id_animal),
    CONSTRAINT fk_veterinario FOREIGN KEY (id_veterinario) REFERENCES Veterinario(id_veterinario),
    CONSTRAINT fk_tipo FOREIGN KEY (id_tipo) REFERENCES Tipo_Consulta(id_tipo)
);


CREATE TABLE IF NOT EXISTS Tipo_Tratamento (
    id_tipo_tratamento SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS Tratamento (
    id_tratamento SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    id_tipo_tratamento INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    duracao_estimada VARCHAR(50) NOT NULL,
    data_inicio DATE NOT NULL,
    CONSTRAINT fk_consulta FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta),
    CONSTRAINT fk_tipo_tratamento FOREIGN KEY (id_tipo_tratamento) REFERENCES Tipo_Tratamento(id_tipo_tratamento)
);


CREATE TABLE IF NOT EXISTS Tipo_Exame (
    id_tipo_exame SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS Exame (
    id_exame SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    id_animal INTEGER NOT NULL,
    id_tipo_exame INTEGER NOT NULL,
    resultado TEXT,
    data_exame DATE NOT NULL,
    observacoes VARCHAR(150),
    CONSTRAINT fk_consulta FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta),
    CONSTRAINT fk_animal FOREIGN KEY (id_animal) REFERENCES Animal(id_animal),
    CONSTRAINT fk_tipo_exame FOREIGN KEY (id_tipo_exame) REFERENCES Tipo_Exame(id_tipo_exame)
);


CREATE TABLE IF NOT EXISTS Medicamento (
    id_medicamento SERIAL PRIMARY KEY,
    nome VARCHAR(70) NOT NULL,
    descricao VARCHAR(150) NOT NULL,
    quantidade INTEGER NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    uso VARCHAR(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS Receita_Medica (
    id_receita SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    id_tratamento INTEGER NOT NULL,
    id_veterinario VARCHAR(11) NOT NULL,
    data DATE NOT NULL,
    observacoes VARCHAR(150),
    CONSTRAINT fk_consulta FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta),
    CONSTRAINT fk_tratamento FOREIGN KEY (id_tratamento) REFERENCES Tratamento(id_tratamento),
    CONSTRAINT fk_veterinario FOREIGN KEY (id_veterinario) REFERENCES Veterinario(id_veterinario)
);

CREATE TABLE IF NOT EXISTS Receita_Medicamento (
    id_receita INTEGER NOT NULL,
    id_medicamento INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    tipo_quantidade VARCHAR(5) NOT NULL,
    frequencia VARCHAR(25) NOT NULL,
    duracao VARCHAR(75) NOT NULL,
    PRIMARY KEY (id_receita, id_medicamento),
    CONSTRAINT fk_receita FOREIGN KEY (id_receita) REFERENCES Receita_Medica(id_receita),
    CONSTRAINT fk_medicamento FOREIGN KEY (id_medicamento) REFERENCES Medicamento(id_medicamento)
);


CREATE TABLE IF NOT EXISTS Meio_Pagamento (
    id_meio_pagamento SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    valor NUMERIC(15, 2) NOT NULL,
    data_pagamento DATE NOT NULL,
    id_meio_pagamento INTEGER NOT NULL,
    CONSTRAINT fk_consulta FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta),
    CONSTRAINT fk_meio_pagamento FOREIGN KEY (id_meio_pagamento) REFERENCES Meio_Pagamento(id_meio_pagamento)
);


CREATE TABLE IF NOT EXISTS Status (
    id_status SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Agendamento (
    id_agendamento SERIAL PRIMARY KEY,
    id_tutor INTEGER NOT NULL,
    id_animal INTEGER NOT NULL,
    data DATE NOT NULL,
    hora TIME NOT NULL,
    id_status INTEGER NOT NULL,
    CONSTRAINT fk_tutor FOREIGN KEY (id_tutor) REFERENCES Tutor(id_tutor),
    CONSTRAINT fk_animal FOREIGN KEY (id_animal) REFERENCES Animal(id_animal),
    CONSTRAINT fk_status FOREIGN KEY (id_status) REFERENCES Status(id_status)
);