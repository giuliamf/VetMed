<<<<<<< Updated upstream
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

-- Tabela 'super'
CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario SERIAL PRIMARY KEY,  -- id serial automático
    email VARCHAR(50) UNIQUE NOT NULL,  -- Unique para evitar emails iguais
    nome VARCHAR(90) NOT NULL,
    senha VARCHAR(256) NOT NULL,
    cargo VARCHAR(3) CHECK (cargo IN ('vet', 'sec')) NOT NULL  -- Restrição CHECK para aceitar valores específicos
);

-- Tabela de Especialidades (cadastra as possíveis especialidades)
CREATE TABLE IF NOT EXISTS Especialidade (
    id_especialidade SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

-- Sub-tabela de Veterinário (herda de Usuario)
CREATE TABLE IF NOT EXISTS Veterinario (
    id_veterinario INT PRIMARY KEY REFERENCES Usuario(id_usuario) ON DELETE CASCADE,  -- Herda ID de Usuario
    id_especialidade INT NOT NULL REFERENCES Especialidade(id_especialidade)
    -- Especialidade obrigatória, não é PK porque cada veterinário tem apenas uma especialidade e ela é obrigatória
);

CREATE TABLE IF NOT EXISTS Tutor (
    id_tutor SERIAL PRIMARY KEY,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE NOT NULL,
    telefone VARCHAR(15) NOT NULL,
    endereco VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS Animal (
    id_animal SERIAL PRIMARY KEY,
    id_tutor INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raca VARCHAR(50) NOT NULL,
    nascimento DATE NOT NULL,
    sexo CHAR(1) CHECK (sexo IN ('F', 'M')) NOT NULL, -- CHAR pq tem obrigatoriamente um único caractere
    peso NUMERIC(5,2) NOT NULL,
    cor VARCHAR(50) NOT NULL,
    CONSTRAINT fk_tutor FOREIGN KEY (id_tutor) REFERENCES Tutor(id_tutor)
);

CREATE TABLE IF NOT EXISTS Status (
    id_status SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Agendamento (
    id_agendamento SERIAL PRIMARY KEY,
    id_animal INTEGER NOT NULL,
    id_status INTEGER NOT NULL,
    data DATE NOT NULL,
    hora CHAR(5) NOT NULL, -- Time retorna HH:MM:SS, nesse caso apenas a string é suficiente
    CONSTRAINT fk_animal FOREIGN KEY (id_animal) REFERENCES Animal(id_animal),
    CONSTRAINT fk_status FOREIGN KEY (id_status) REFERENCES Status(id_status)
);

CREATE TABLE IF NOT EXISTS Tipo_Consulta (
    id_tipo SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
);

CREATE TABLE IF NOT EXISTS Consulta (
    id_consulta SERIAL PRIMARY KEY,
    id_veterinario CHAR(11) NOT NULL,
    id_agendamento INTEGER NOT NULL,
    data DATE NOT NULL,
    horario TIME NOT NULL,
    id_tipo INTEGER NOT NULL,
    valor_total NUMERIC(10, 2) GENERATED ALWAYS AS (
        (SELECT COALESCE(SUM(p.preco), 0)
         FROM Consulta_Tratamento cp
         JOIN Tratamento p ON cp.id_tratamento = p.id_tratamento
         WHERE cp.id_consulta = Consulta.id_consulta)
    ) STORED,
    status VARCHAR(20) NOT NULL DEFAULT 'em aberto',
    CONSTRAINT fk_veterinario FOREIGN KEY (id_veterinario) REFERENCES Veterinario(id_veterinario),
    CONSTRAINT fk_tipo FOREIGN KEY (id_tipo) REFERENCES Tipo_Consulta(id_tipo),
    CONSTRAINT fk_agendamento FOREIGN KEY (id_agendamento) REFERENCES Agendamento(id_agendamento)
);

CREATE TABLE IF NOT EXISTS Tratamento (
    id_tratamento SERIAL PRIMARY KEY,
    descricao TEXT NOT NULL,
    preco NUMERIC(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS Consulta_Tratamento (
    id_consulta_procedimento SERIAL PRIMARY KEY,
    id_tratamento INTEGER NOT NULL,
    id_consulta INTEGER NOT NULL,
    CONSTRAINT fk_tratamento FOREIGN KEY (id_tratamento) REFERENCES Tratamento(id_tratamento),
    CONSTRAINT fk_consulta FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta)
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

-- Trigger para atualizar o status da consulta para 'pago' quando o pagamento é registrado
CREATE OR REPLACE FUNCTION AtualizarStatusConsulta() RETURNS TRIGGER AS $$
BEGIN
    -- Atualiza o status da consulta se o valor total foi pago
    IF (SELECT COALESCE(SUM(valor_pago), 0) FROM Pagamento WHERE id_consulta = NEW.id_consulta) >= 
       (SELECT valor_total FROM Consulta WHERE id_consulta = NEW.id_consulta) THEN
        UPDATE Consulta
        SET status = 'pago'
        WHERE id_consulta = NEW.id_consulta;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER atualizar_status_consulta
AFTER INSERT ON Pagamento
FOR EACH ROW
=======
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


CREATE TABLE IF NOT EXISTS Usuario (
    email_usuario CHAR(50) PRIMARY KEY,  -- E-mail do usuário
    nome VARCHAR(90) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    endereco VARCHAR(120) NOT NULL,
    senha VARCHAR(256) NOT NULL
);

CREATE TABLE IF NOT EXISTS Tutor (
    cpf_tutor VARCHAR(14) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE,
    telefone VARCHAR(15),
    endereco VARCHAR(200),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS Animal (
    id_animal SERIAL PRIMARY KEY,
    cpf_tutor VARCHAR(14) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raca VARCHAR(50),
    ano_nascimento INTEGER,
    sexo VARCHAR(1),
    peso FLOAT,
    cor VARCHAR(50),
    CONSTRAINT fk_tutor FOREIGN KEY (cpf_tutor) REFERENCES Tutor(cpf_tutor)
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

CREATE TABLE IF NOT EXISTS Status (
    id_status SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Agendamento (
    id_agendamento SERIAL PRIMARY KEY,
    id_animal INTEGER NOT NULL,
    data DATE NOT NULL,
    hora TIME NOT NULL,
    id_status INTEGER NOT NULL,
    CONSTRAINT fk_animal FOREIGN KEY (id_animal) REFERENCES Animal(id_animal),
    CONSTRAINT fk_status FOREIGN KEY (id_status) REFERENCES Status(id_status)
);

CREATE TABLE IF NOT EXISTS Tipo_Consulta (
    id_tipo SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
);

CREATE TABLE IF NOT EXISTS Consulta (
    id_consulta SERIAL PRIMARY KEY,
    id_veterinario CHAR(11) NOT NULL,
    id_agendamento INTEGER NOT NULL,
    data DATE NOT NULL,
    horario TIME NOT NULL,
    id_tipo INTEGER NOT NULL,
    valor_total NUMERIC(10, 2) GENERATED ALWAYS AS (
        (SELECT COALESCE(SUM(p.preco), 0)
         FROM Consulta_Tratamento cp
         JOIN Tratamento p ON cp.id_tratamento = p.id_tratamento
         WHERE cp.id_consulta = Consulta.id_consulta)
    ) STORED,
    status VARCHAR(20) NOT NULL DEFAULT 'em aberto',
    CONSTRAINT fk_veterinario FOREIGN KEY (id_veterinario) REFERENCES Veterinario(id_veterinario),
    CONSTRAINT fk_tipo FOREIGN KEY (id_tipo) REFERENCES Tipo_Consulta(id_tipo),
    CONSTRAINT fk_agendamento FOREIGN KEY (id_agendamento) REFERENCES Agendamento(id_agendamento)
);

CREATE TABLE IF NOT EXISTS Tratamento (
    id_tratamento SERIAL PRIMARY KEY,
    descricao TEXT NOT NULL,
    preco NUMERIC(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS Consulta_Tratamento (
    id_consulta_procedimento SERIAL PRIMARY KEY,
    id_tratamento INTEGER NOT NULL,
    id_consulta INTEGER NOT NULL,
    CONSTRAINT fk_tratamento FOREIGN KEY (id_tratamento) REFERENCES Tratamento(id_tratamento),
    CONSTRAINT fk_consulta FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta)
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

-- Trigger para atualizar o status da consulta para 'pago' quando o pagamento é registrado
CREATE OR REPLACE FUNCTION AtualizarStatusConsulta() RETURNS TRIGGER AS $$
BEGIN
    -- Atualiza o status da consulta se o valor total foi pago
    IF (SELECT COALESCE(SUM(valor_pago), 0) FROM Pagamento WHERE id_consulta = NEW.id_consulta) >= 
       (SELECT valor_total FROM Consulta WHERE id_consulta = NEW.id_consulta) THEN
        UPDATE Consulta
        SET status = 'pago'
        WHERE id_consulta = NEW.id_consulta;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER atualizar_status_consulta
AFTER INSERT ON Pagamento
FOR EACH ROW
>>>>>>> Stashed changes
EXECUTE FUNCTION AtualizarStatusConsulta();