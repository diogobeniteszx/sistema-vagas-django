# Sistema de Vagas

Aplicação web desenvolvida com **Django** para gerenciamento de oportunidades de emprego e candidaturas.

O sistema permite que usuários encontrem vagas, criem seu currículo e realizem candidaturas. Usuários com acesso administrativo podem gerenciar as vagas e acompanhar os candidatos.

## Sobre o projeto

O **Sistema de Vagas** foi desenvolvido para simular uma plataforma de recrutamento, centralizando o processo de publicação de vagas e candidatura em uma única aplicação.

A aplicação conta com autenticação de usuários, controle de permissões, gerenciamento de currículos, upload de arquivos PDF, filtros de vagas, paginação e acompanhamento de candidaturas.

## Funcionalidades

### Para candidatos

* Cadastro e autenticação de usuários
* Visualização de vagas disponíveis
* Busca e filtragem de vagas
* Ordenação das vagas
* Visualização dos detalhes de uma vaga
* Cadastro e edição de currículo
* Upload de currículo em PDF
* Candidatura para vagas
* Prevenção de candidaturas duplicadas
* Visualização das próprias candidaturas
* Acompanhamento do status das candidaturas

### Para administradores

* Cadastro de vagas
* Edição de vagas
* Exclusão de vagas
* Ativação e desativação de vagas
* Visualização dos candidatos de uma vaga
* Gerenciamento através do sistema de permissões do Django

## Tecnologias

| Tecnologia           | Utilização                |
| -------------------- | ------------------------- |
| **Python**           | Linguagem principal       |
| **Django 6.0.4**     | Framework web             |
| **PostgreSQL**       | Banco de dados            |
| **Django ORM**       | Comunicação com o banco   |
| **Django Templates** | Interface da aplicação    |
| **HTML5**            | Estrutura das páginas     |
| **CSS3**             | Estilização               |
| **python-dotenv**    | Variáveis de ambiente     |
| **psycopg2**         | Integração com PostgreSQL |

## Arquitetura

O projeto utiliza a arquitetura **MVT (Model-View-Template)** do Django.

## Principais entidades

O sistema possui três modelos principais:

### Vaga

Representa uma oportunidade de emprego publicada no sistema.

Uma vaga possui informações como empresa, localização, modalidade, salário, descrição, requisitos e status.

### Currículo

Representa o currículo de um usuário.

Além das informações profissionais, o sistema permite o armazenamento de um arquivo PDF associado ao currículo.

### Candidatura

Relaciona um candidato a uma vaga.

A candidatura possui um status que permite acompanhar seu andamento:

* Enviada
* Em análise
* Aprovada
* Rejeitada

O sistema impede que o mesmo candidato se candidate mais de uma vez à mesma vaga.

## Requisitos

Antes de executar o projeto, certifique-se de possuir:

* **Python 3.12+**
* **PostgreSQL**

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/diogobeniteszx/sistema-vagas-django.git
```

Entre na pasta do projeto:

```bash
cd sistema-vagas-django
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

No terminal:

```bash
source venv/Scripts/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta
DEBUG=True

DB_NAME=sistema_vagas
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

> O arquivo `.env` contém informações sensíveis e não deve ser versionado no Git.

### 5. Configure o banco de dados

Crie um banco PostgreSQL com o mesmo nome definido em `DB_NAME`.

Em seguida, execute as migrações:

```bash
python manage.py migrate
```

### 6. Crie um usuário administrador

```bash
python manage.py createsuperuser
```

Siga as instruções exibidas no terminal.

### 7. Execute a aplicação

```bash
python manage.py runserver
```

## Banco de dados

O projeto utiliza **PostgreSQL** como sistema de gerenciamento de banco de dados.

A conexão é configurada através de variáveis de ambiente, evitando que credenciais sejam armazenadas diretamente no código-fonte.

As migrações do banco são gerenciadas pelo próprio Django:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Sistema de autenticação

A autenticação utiliza o sistema nativo do Django.

O acesso às funcionalidades administrativas é controlado através das permissões de usuário, enquanto as funcionalidades de candidato ficam disponíveis para usuários autenticados.

## Currículos

Os usuários podem cadastrar suas informações profissionais e anexar um currículo em formato **PDF**.

Os arquivos enviados são armazenados no diretório:

```text
media/curriculos/
```

Durante o desenvolvimento, esse diretório é utilizado como armazenamento local dos arquivos enviados.

## E-mails

O projeto utiliza o sistema de e-mail do Django para enviar uma confirmação após uma candidatura.

No ambiente de desenvolvimento, o backend configurado utiliza o **console**, fazendo com que o conteúdo do e-mail seja exibido no terminal em vez de ser enviado por um serviço externo.

## Licença

Este projeto foi desenvolvido para fins de estudo e prática de desenvolvimento web com Django.
