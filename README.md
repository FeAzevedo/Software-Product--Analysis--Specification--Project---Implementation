# Cadastro de Veículos

Este é um projeto de cadastro de veículos utilizando **FastAPI** para o backend e **Streamlit** para o frontend.

## Tecnologias Utilizadas

- **FastAPI**: Framework para criação da API.
- **SQLite**: Banco de dados para armazenar os dados dos veículos.
- **SQLModel**: ORM para interação com o banco de dados.
- **Streamlit**: Interface gráfica para cadastro e exibição dos veículos.
- **Requests**: Biblioteca para fazer requisições HTTP no frontend.

## Como Rodar o Projeto

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/cadastro-de-veiculos.git
cd cadastro-de-veiculos
```

### 2. Criar um Ambiente Virtual (Opcional, mas recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Rodar o Backend (FastAPI)
```bash
fastapi dev main.py
```

O servidor FastAPI rodará em `http://127.0.0.1:8000`.

### 5. Rodar o Frontend (Streamlit)
Abra outro terminal e execute:
```bash
streamlit run frontend_streamlit.py
```

O frontend estará acessível em `http://localhost:8501`.

## Endpoints da API

- **`GET /veiculos`** - Lista todos os veículos cadastrados.
- **`POST /veiculos`** - Cadastra um novo veículo.

## Funcionalidades

- Cadastro de veículos com modelo, valor, cor e ano.
- Listagem de veículos cadastrados.
- Interface gráfica para interação fácil com o usuário.

## Contribuição
Se quiser contribuir com o projeto, fique à vontade para abrir uma *issue* ou enviar um *pull request*.

## Licença
Este projeto está sob a licença MIT.

