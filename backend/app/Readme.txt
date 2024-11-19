quiz_project/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py        # Torna o diretório um pacote Python
│   │   ├── routes.py          # Define os endpoints da API
│   │   ├── quiz_manager.py    # Gerencia a lógica de dados no Redis
│   │   └── populate_quiz.py   # Script para popular o banco de dados
│   └── main.py                # Ponto de entrada da aplicação
│
├── frontend/
│   ├── index.html             # Estrutura da interface do usuário
│   ├── script.js              # Lógica de interação do lado do cliente
│   └── styles.css             # Estilização da interface do usuário
│
├── venv/
│   ├── bin/
│   │   └── activate           # Ativa o ambiente virtual
│   └── ...                    # Outros arquivos do ambiente virtual
│
└── requirements.txt           # Dependências do projeto