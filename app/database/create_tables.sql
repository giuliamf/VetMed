-- Nome do banco de dados: VetMed
-- Codificacao: UTF-8
-- Regiao: Brasil (pt_BR)
-- Porta padrao: 5432 (PostgreSQL)
-- Proposito: Banco de dados para sistema de gestao de clinica veterinaria

-- Configuracoes adicionais do banco de dados
SET client_encoding = 'UTF8';
SET TIMEZONE = 'America/Sao_Paulo'; -- Fuso horario do Brasil

-- Permissoes e roles (opcional, dependendo do ambiente)
-- Cria um role especifico para o banco de dados (substitua 'admin' e 'senha_segura' conforme necessario)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'admin') THEN
        CREATE ROLE admin WITH LOGIN PASSWORD 'senha_segura';
    END IF;
END $$;

GRANT ALL PRIVILEGES ON DATABASE VetMed TO admin;

-- Configuracoes de extensoes (opcional, se necessario)
-- Exemplo: Habilita a extensao pgcrypto para criptografia
-- CREATE EXTENSION IF NOT EXISTS pgcrypto; -criptografia feita no front-end-

-- Configuracoes de tabelas e esquemas (opcional)
-- Cria um esquema especifico para organizar as tabelas (substitua 'vet_schema' pelo nome desejado)
CREATE SCHEMA IF NOT EXISTS vet_schema;
SET search_path TO vet_schema;

-- Comentarios adicionais
COMMENT ON DATABASE VetMed IS 'Banco de dados para gestao da clinica veterinaria MED VET.';

-- Tabela 'super'
CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario SERIAL PRIMARY KEY,  -- id serial automatico
    email VARCHAR(50) UNIQUE NOT NULL,  -- Unique para evitar emails iguais
    nome VARCHAR(90) NOT NULL,
    senha VARCHAR(256) NOT NULL,
    cargo VARCHAR(3) CHECK (cargo IN ('vet', 'sec')) NOT NULL  -- Restricao CHECK para aceitar valores especificos
);

-- Tabela de Especialidades (cadastra as possiveis especialidades)
CREATE TABLE IF NOT EXISTS Especialidade (
    id_especialidade SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

-- Sub-tabela de Veterinario (herda de Usuario)
CREATE TABLE IF NOT EXISTS Veterinario (
    id_veterinario INT PRIMARY KEY REFERENCES Usuario(id_usuario) ON DELETE CASCADE,  -- Herda ID de Usuario
    id_especialidade INT NOT NULL REFERENCES Especialidade(id_especialidade)
    -- Especialidade obrigatoria, nao eh PK porque cada veterinario tem apenas uma especialidade e ela eh obrigatoria
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
    sexo CHAR(1) CHECK (sexo IN ('F', 'M')) NOT NULL, -- CHAR porque tem obrigatoriamente um unico caractere
    peso NUMERIC(5,2) NOT NULL,
    cor VARCHAR(50) NOT NULL,
    CONSTRAINT fk_tutor FOREIGN KEY (id_tutor) REFERENCES Tutor(id_tutor)
);

CREATE TABLE IF NOT EXISTS StatusAgendamento (
    id_status SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Agendamento (
    id_agendamento SERIAL PRIMARY KEY,
    id_animal INT NOT NULL,
    id_status INT NOT NULL DEFAULT 1,
    data DATE NOT NULL,
    horario CHAR(5) NOT NULL, -- Time retorna HH:MM:SS, nesse caso apenas a string HH:MM eh suficiente
    CONSTRAINT fk_animal FOREIGN KEY (id_animal) REFERENCES Animal(id_animal),
    CONSTRAINT fk_status FOREIGN KEY (id_status) REFERENCES StatusAgendamento(id_status)
);

CREATE TABLE IF NOT EXISTS Tipo_Consulta (
    id_tipo SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Consulta (
    id_consulta SERIAL PRIMARY KEY,
    id_veterinario INT NOT NULL,
    id_agendamento INTEGER NOT NULL,
    data DATE NOT NULL,
    horario TIME NOT NULL,
    id_tipo INTEGER NOT NULL,
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
    id_tratamento INT NOT NULL,
    id_consulta INT NOT NULL,
    CONSTRAINT fk_tratamento FOREIGN KEY (id_tratamento) REFERENCES Tratamento(id_tratamento),
    CONSTRAINT fk_consulta FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta)
);

CREATE TABLE IF NOT EXISTS Meio_Pagamento (
    id_meio_pagamento SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    id_consulta INT NOT NULL,
    valor NUMERIC(15, 2) NOT NULL,
    data_pagamento DATE NOT NULL,
    id_meio_pagamento INT NOT NULL,
    CONSTRAINT fk_consulta FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta),
    CONSTRAINT fk_meio_pagamento FOREIGN KEY (id_meio_pagamento) REFERENCES Meio_Pagamento(id_meio_pagamento)
);

-- Trigger para atualizar o status da consulta para 'pago' quando o pagamento eh registrado
CREATE OR REPLACE FUNCTION AtualizarStatusConsulta() RETURNS TRIGGER AS $$
BEGIN
    -- Atualiza o status da consulta se o valor total foi pago
    IF (SELECT COALESCE(SUM(valor), 0) FROM Pagamento WHERE id_consulta = NEW.id_consulta) >=
       (SELECT valor_total FROM Consulta WHERE id_consulta = NEW.id_consulta) THEN
        UPDATE Consulta
        SET status = 'pago'
        WHERE id_consulta = NEW.id_consulta;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- View para atualizar dinamicamente o valor total da consulta
CREATE OR REPLACE VIEW View_Consulta_Valor AS
SELECT
    c.id_consulta,
    COALESCE(SUM(t.preco), 0) AS valor_total_atualizado
FROM Consulta c
LEFT JOIN Consulta_Tratamento ct ON c.id_consulta = ct.id_consulta
LEFT JOIN Tratamento t ON ct.id_tratamento = t.id_tratamento
GROUP BY c.id_consulta;


-- Verifica e remove o trigger caso já exista antes de recriá-lo
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'atualizar_status_consulta') THEN
        DROP TRIGGER atualizar_status_consulta ON Pagamento;
    END IF;
END $$;

CREATE OR REPLACE VIEW View_Consulta_Valor AS
SELECT
    c.id_consulta,
    COALESCE(SUM(t.preco), 0) AS valor_total_atualizado
FROM Consulta c
LEFT JOIN Consulta_Tratamento ct ON c.id_consulta = ct.id_consulta
LEFT JOIN Tratamento t ON ct.id_tratamento = t.id_tratamento
GROUP BY c.id_consulta;

-- Criar o trigger após garantir que ele não existe
-- Verifica e remove o trigger caso já exista antes de recriá-lo
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'atualizar_status_consulta') THEN
        DROP TRIGGER atualizar_status_consulta ON Pagamento;
    END IF;
END $$;

-- Criar o trigger após garantir que ele não existe
CREATE TRIGGER atualizar_status_consulta
AFTER INSERT ON Pagamento
FOR EACH ROW
EXECUTE FUNCTION AtualizarStatusConsulta();
