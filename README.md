# Task Planner

Um aplicativo de gerenciamento de tarefas com interface gráfica desenvolvido em Python usando Tkinter.

## Funcionalidades

- Adicionar, editar e remover tarefas
- Filtrar tarefas por título, tag e status
- Ordenar tarefas por data limite, prioridade ou status
- Visualização em calendário
- Exportar e importar tarefas em formato CSV
- Interface gráfica moderna e intuitiva

## Requisitos

- Python 3.7 ou superior
- tkinter (geralmente vem com Python)
- tkcalendar

## Instalação

1. Clone ou baixe este repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Executar

Execute o arquivo principal:
```bash
python main.py
```

## Estrutura do Projeto

- `main.py` - Ponto de entrada da aplicação
- `config.py` - Configurações e constantes
- `models.py` - Modelo de dados
- `database.py` - Gerenciamento do banco de dados
- `gui.py` - Interface gráfica principal
- `gui_components.py` - Componentes reutilizáveis da interface

## Notas

- O banco de dados SQLite será criado automaticamente na primeira execução
- A localização está configurada para pt_BR
- As tarefas são salvas localmente no arquivo `tasks.db`

## Autores

- Thiago Godinho Pancieri
- Rafael Ferraresso de Freitas
- Victor Hugo Mendes de Sousa
- Nathália Chaves Teixeira
- Gabryel Gomes Linhares 
