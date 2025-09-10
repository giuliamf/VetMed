# VetMed - Projeto de Banco de Dados

Sistema desenvolvido para otimizar a gestão de clínicas veterinárias. O projeto foi desenvolvido como parte da disciplina de Banco de Dados do curso de Ciência da Computação da Universidade de Brasília, no semestre 2024.2.

A aplicação possui um **CRUD funcional**, com:

* Criptografia de senhas;
* Cadastro de usuários (médicos ou secretários), pacientes (animais) e tutores;
* Médicos devem ter especialidade e horários de atendimento, que são utilizados no agendamento de consultas;
* Agendamento de consultas filtrando médico/especialidade/horário;
* Cancelamento de consultas.

Além disso, foi criado um **Modelo de Entidade-Relacionamento (MER)**, posteriormente transformado em **Modelo Relacional** (`docs/diagrama_mr.png`).
As formas normais foram analisadas em cinco tabelas do banco, e foi elaborado um diagrama da camada de mapeamento para auxiliar na compreensão do armazenamento e acesso aos dados.

---

## Estrutura do Projeto

### Diretório principal

* `application/`

  * `database/`: Scripts SQL e código relacionado ao banco de dados.
  * `routes/`: Rotas da aplicação (Flask).
  * `static/`: Arquivos estáticos

    * `css/`: Estilos da aplicação
    * `icones/`: Ícones da interface
    * `images/`: Imagens da aplicação
    * `js/`: Scripts JavaScript
    * `profile_pictures/`: Imagens de perfil de usuários
  * `templates/`: Templates HTML

    * `partials/`: Partes de templates reutilizáveis
    * `tela_cadastros/`: Templates de cadastros e edições
  * `utils/`: Funções utilitárias
  * `__init__.py`: Inicialização da aplicação Flask
  * `config.py`: Configurações gerais
  * `database.py`: Conexão e manipulação do banco
  * `main.py`: Ponto de entrada da aplicação
  * `simulação_bd.py`: Scripts para simulação de dados no banco

### Documentação

* `docs/`

  * `app_screenshots/`: Prints de telas principais da aplicação
  * `Código para o PlantUML...`: Código para gerar diagramas
  * `Descrição Textual do Banco de Dados.txt`
  * `Diagrama link.txt`
  * `diagrama_mr.png`: Modelo Relacional
  * `link txt`
  * `arquivolog`

### Outros arquivos

* `install_dependencies.bash`: Script para instalar dependências
* `requirements.txt`: Lista de pacotes Python necessários
* `README.md`: Este arquivo
* `LICENSE`: Licença do projeto

---

## Como Rodar o Projeto

1. Clone o repositório:

   ```bash
   git clone https://github.com/SEU_USUARIO/VetMed.git
   cd VetMed
   ```

2. Crie e ative o ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/Mac
   venv\Scripts\activate       # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação:

   ```bash
   python application/main.py
   ```

---

## Tecnologias Utilizadas

* Python (Flask)
* PostgreSQL
* HTML, CSS, JavaScript

---

## Autores

Projeto desenvolvido por [Ana Luiza](https://github.com/analuiza-cs), [Celio Eduardo](https://github.com/celio-eduardo), [Giulia Moura](https://github.com/giuliamf) e [Leticia Xavier](https://github.com/laetitiaX).
