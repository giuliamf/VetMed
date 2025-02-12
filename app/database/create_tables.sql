-- Nome do banco de dados: vetmed
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

GRANT ALL PRIVILEGES ON DATABASE vetmed TO admin;

-- Configuracoes de extensoes (opcional, se necessario)
-- Exemplo: Habilita a extensao pgcrypto para criptografia
-- CREATE EXTENSION IF NOT EXISTS pgcrypto; -criptografia feita no front-end-

-- Configuracoes de tabelas e esquemas (opcional)
-- Cria um esquema especifico para organizar as tabelas (substitua 'vet_schema' pelo nome desejado)
CREATE SCHEMA IF NOT EXISTS vet_schema;
SET search_path TO vet_schema;

-- Comentarios adicionais
COMMENT ON DATABASE vetmed IS 'Banco de dados para gestao da clinica veterinaria MED VET.';

-- Tabela 'super'
CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario SERIAL PRIMARY KEY,  -- id serial automatico
    email VARCHAR(50) UNIQUE NOT NULL,  -- Unique para evitar emails iguais
    nome VARCHAR(90) NOT NULL,
    senha VARCHAR(64) NOT NULL,
    cargo VARCHAR(3) CHECK (cargo IN ('vet', 'sec', 'adm')) NOT NULL,  -- Restricao CHECK para aceitar valores especificos
);

CREATE TABLE IF NOT EXISTS Usuario_Foto (
    id_usuario INT PRIMARY KEY REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    foto bytea NOT NULL -- ver oq fazer aqui com a foto!! default
);

-- Tabela de Especialidades (cadastra as possiveis especialidades)
CREATE TABLE IF NOT EXISTS Especialidade (
    id_especialidade SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

-- Sub-tabela de Veterinario (herda de Usuario)
CREATE TABLE IF NOT EXISTS Veterinario (
    id_veterinario INT PRIMARY KEY REFERENCES Usuario(id_usuario) ON DELETE CASCADE,  -- Herda ID de Usuario
    id_especialidade INT NOT NULL REFERENCES Especialidade(id_especialidade),
    carga_horaria CHAR(5) CHECK (carga_horaria IN ('manhã', 'tarde')) NOT NULL
    -- Especialidade obrigatoria, nao eh PK porque cada veterinario tem apenas uma especialidade e ela eh obrigatoria
);

CREATE TABLE IF NOT EXISTS Tutor (
    id_tutor SERIAL PRIMARY KEY,
    cpf CHAR(14) UNIQUE NOT NULL CHECK ( cpf ~ '^\d{3}\.\d{3}\.\d{3}-\d{2}$' ), -- Restricao CHECK para CPF
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
    CONSTRAINT fk_tutor FOREIGN KEY (id_tutor) REFERENCES Tutor(id_tutor) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Status_Agendamento (
    id_status SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Agendamento (
    id_agendamento SERIAL PRIMARY KEY,
    id_animal INT NOT NULL,
    id_status INT NOT NULL DEFAULT 1,
    id_veterinario INT NOT NULL,
    data DATE NOT NULL,
    horario TIME NOT NULL, -- Time retorna HH:MM:SS tratar como HH:MM no select/back end
    CONSTRAINT fk_animal FOREIGN KEY (id_animal) REFERENCES Animal(id_animal) ON DELETE CASCADE,
    CONSTRAINT fk_status FOREIGN KEY (id_status) REFERENCES Status_Agendamento(id_status),
    CONSTRAINT fk_veterinario FOREIGN KEY (id_veterinario) REFERENCES Veterinario(id_veterinario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Horario_Funcionamento (
    id_horario SERIAL PRIMARY KEY,
    horario TIME NOT NULL,
    turno CHAR(5) CHECK (turno IN ('manhã', 'tarde')) NOT NULL
);

CREATE TABLE IF NOT EXISTS Carga_Horaria (
       id_veterinario INT NOT NULL,
       turno CHAR(5) CHECK (turno IN ('manhã', 'tarde')) NOT NULL,
        PRIMARY KEY (id_veterinario, turno),
        FOREIGN KEY (id_veterinario) REFERENCES veterinario(id_veterinario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Horario_Ocupado (
    id_veterinario INT NOT NULL,
    id_agendamento INT NOT NULL,
    data DATE NOT NULL,
    horario TIME NOT NULL,
    PRIMARY KEY (id_veterinario, id_agendamento),
    FOREIGN KEY (id_veterinario) REFERENCES veterinario(id_veterinario) ON DELETE CASCADE,
    FOREIGN KEY (id_agendamento) REFERENCES agendamento(id_agendamento) ON DELETE CASCADE
);

-- FUNCOES, TRIGGERS, VIEWS

-- Funcao para remover horario ocupado quando um agendamento for cancelado
CREATE OR REPLACE FUNCTION remover_horario_ocupado()
RETURNS TRIGGER AS $$
BEGIN
    -- Se o status do agendamento mudar para 2 (cancelado), remover o horário ocupado correspondente
    IF NEW.id_status = 2 THEN
        DELETE FROM Horario_Ocupado
        WHERE id_veterinario = NEW.id_veterinario
        AND id_agendamento = NEW.id_agendamento;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Conferir se o trigger de remover horário já existe antes de re-criar
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_remover_horario_ocupado') THEN
        DROP TRIGGER trg_remover_horario_ocupado ON Agendamento;
    END IF;
END $$;

-- Criar (ou recriar, caso já exista antes) o trigger para remover horario ocupado
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_definir_foto_padrao') THEN
        DROP TRIGGER trg_definir_foto_padrao ON Usuario;
    END IF;
END $$;

-- Trigger para definir foto padrão do usuário
CREATE OR REPLACE FUNCTION definir_foto_padrao()
RETURNS TRIGGER AS $$
DECLARE
    v_foto_padrao BYTEA;
BEGIN
    -- Carrega a imagem padrão do diretório
    SELECT pg_read_binary_file('app/static/profile_pictures/padrao.jpg') INTO v_foto_padrao;

    -- Se a foto for NULL (inserção ou remoção da foto pelo usuário), definir imagem padrão
    IF NEW.foto IS NULL THEN
        NEW.foto := v_foto_padrao;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Chamada para criar o trigger
CREATE TRIGGER trg_definir_foto_padrao
BEFORE INSERT OR UPDATE ON Usuario
FOR EACH ROW
EXECUTE FUNCTION definir_foto_padrao();

-- Conferir se o trigger de foto já existe
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_definir_foto_padrao') THEN
        DROP TRIGGER trg_definir_foto_padrao ON Usuario;
    END IF;
END $$;

-- Trigger para definir foto padrão do usuário
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_definir_foto_padrao') THEN
        DROP TRIGGER trg_definir_foto_padrao ON Usuario;
    END IF;
END $$;

CREATE OR REPLACE FUNCTION definir_foto_padrao()
RETURNS TRIGGER AS $$
DECLARE
    v_foto_padrao BYTEA;
BEGIN
    -- Carrega a imagem padrão do diretório para armazenar no banco
    SELECT pg_read_binary_file('app/static/profile_pictures/padrao.jpg') INTO v_foto_padrao;

    -- Se o usuário não enviou uma foto, define a imagem padrão
    IF NEW.foto IS NULL THEN
        NEW.foto := v_foto_padrao;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_definir_foto_padrao
BEFORE INSERT ON Usuario
FOR EACH ROW
EXECUTE FUNCTION definir_foto_padrao();


-- View para listar horários que um veterinário tem agendamento
CREATE OR REPLACE VIEW Horarios_Agendados_Veterinario AS
SELECT
    a.id_agendamento,
    v.id_veterinario,
    u.nome AS nome_veterinario,
    a.data,
    a.horario,
    sa.nome AS status_agendamento,
    an.nome AS nome_animal,
    t.nome AS nome_tutor
FROM Agendamento a
JOIN Veterinario v ON a.id_veterinario = v.id_veterinario
JOIN Usuario u ON u.id_usuario = v.id_veterinario -- Nome do veterinário vem da tabela Usuario
JOIN Animal an ON a.id_animal = an.id_animal
JOIN Tutor t ON an.id_tutor = t.id_tutor
JOIN Status_Agendamento sa ON a.id_status = sa.id_status
ORDER BY a.data, a.horario;

-- Procedure para realizar um agendamento
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'realizar_agendamento') THEN
        DROP PROCEDURE realizar_agendamento;
    END IF;
END $$;

CREATE PROCEDURE realizar_agendamento(
    IN p_id_animal INT,
    IN p_id_veterinario INT,
    IN p_data DATE,
    IN p_horario TIME
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_tutor INT;
    v_turno CHAR(5);
    v_horario_disponivel INT;
BEGIN
    -- Verifica se o animal existe e encontra o tutor associado
    SELECT id_tutor INTO v_tutor FROM Animal WHERE id_animal = p_id_animal;
    IF v_tutor IS NULL THEN
        RAISE EXCEPTION 'O animal informado não existe.';
    END IF;

    -- Verifica se o veterinário atende no turno desse horário
    SELECT turno INTO v_turno FROM Horario_Funcionamento WHERE horario = p_horario;
    IF NOT EXISTS (SELECT 1 FROM Carga_Horaria WHERE id_veterinario = p_id_veterinario AND turno = v_turno) THEN
        RAISE EXCEPTION 'O veterinário não atende neste turno.';
    END IF;

    -- Verifica se o horário está disponível
    SELECT COUNT(*) INTO v_horario_disponivel
    FROM Horario_Ocupado
    WHERE id_veterinario = p_id_veterinario AND data = p_data AND horario = p_horario;

    IF v_horario_disponivel > 0 THEN
        RAISE EXCEPTION 'Este horário já está ocupado para este veterinário.';
    END IF;

    -- Se passou em todas as verificações, insere o agendamento
    INSERT INTO Agendamento (id_animal, id_status, id_veterinario, data, horario)
    VALUES (p_id_animal, 1, p_id_veterinario, p_data, p_horario)
    RETURNING id_agendamento INTO v_horario_disponivel;

    -- Adiciona o horário como ocupado
    INSERT INTO Horario_Ocupado (id_veterinario, id_agendamento, data, horario)
    VALUES (p_id_veterinario, v_horario_disponivel, p_data, p_horario);
END;
$$;
