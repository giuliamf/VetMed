# VetMed - Projeto de Banco de Dados
Sistema desenvolvido para otimizar a gestão de clínicas veterinárias. O projeto foi desenvolvido como parte da disciplina de Banco de Dados do curso de Ciência da Computação da Universidade de Brasília, no semestre 2024.2.

Para estruturar o banco de dados, foi criado um **Modelo de Entidade-Relacionamento (MER)**, posteriormente transformado em Modelo Relacional (`docs/diagarama_mr.png`), as formas normais foram analisadas em cinco tabelas do banco para evitar redundâncias e foi elaborado um diagrama da camada de mapeamento para auxiliar na compreensão do armazenamento e acesso aos dados.

## Descrição dos arquivos
### **Diretório principal da aplicação(`app/`)**
- `database/`: Scripts SQL para criação do banco de dados e inserção de dados iniciais.
- `routes/`: Scripts Python que implementam as rotas da aplicação.
- `static/`: Arquivos estáticos da aplicação
  - `css/`: Estilos da aplicação
  - `icones/`: Ícones da interface
  - `images/`: Imagens da aplicação
  - `js/`: Scripts JavaScript da aplicação
  - `profile_pictures/`: Imagens de perfil dos usuários
- `templates/`: Templates HTML da aplicação
  - `partials/`: Partes de templates reutilizáveis
  - `tela_cadastros/`: Templates de cadastros e edições
- `utils/`: Funções utilitárias da aplicação

## Tecnologias Utilizadas
- Python
- Flask
- PostgreSQL
- HTML
- CSS
- JavaScript

## Autores
Projeto desenvolvido por [Ana Luiza](https://github.com/analuiza-cs), [Celio Eduardo](https://github.com/celio-eduardo), [Giulia Moura](https://github.com/giuliamf) e [Leticia Xavier](https://github.com/laetitiaX).

