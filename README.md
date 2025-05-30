# Task Planner

Um aplicativo de gerenciamento de tarefas com interface gráfica desenvolvido em Python usando Tkinter.

## Funcionalidades

- Adicionar, editar e remover tarefas
- Filtrar tarefas por título, tag e status
- Ordenar tarefas por data limite, prioridade ou status
- Visualização em calendário
- Exportar e importar tarefas em formato CSV
- Interface gráfica moderna e intuitiva

## Requisitos Técnicos

### Versões das Linguagens e Frameworks
- Python 3.7 ou superior
- SQLite 3 (incluído no Python)
- tkinter (incluído no Python)

### Dependências Externas
- tkcalendar==1.6.1

## Instalação

1. Clone ou baixe este repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Instalação no Linux

Para executar o aplicativo no Linux, siga estes passos:

### 1. Configuração do Ambiente Virtual (Recomendado)
```bash
# Instalar o pacote para criar ambientes virtuais
sudo apt install python3-venv

# Criar um ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate

# Instalar as dependências Python
pip install -r requirements.txt
```

### 2. Dependências do Sistema

#### Para a Interface Gráfica (Tkinter)
```bash
# Instalar o Tkinter
sudo apt-get update && sudo apt-get install python3-tk
```

#### Para o Suporte ao Português Brasileiro
```bash
# Gerar e configurar o locale pt_BR.UTF-8
sudo locale-gen pt_BR.UTF-8
sudo update-locale LANG=pt_BR.UTF-8

# Adicionar as seguintes linhas ao seu arquivo ~/.bashrc ou ~/.profile:
echo 'export LANG=pt_BR.UTF-8' >> ~/.bashrc
echo 'export LANGUAGE=pt_BR:pt' >> ~/.bashrc
echo 'export LC_ALL=pt_BR.UTF-8' >> ~/.bashrc

# Recarregar as configurações do shell
source ~/.bashrc
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

## Esquema do Banco de Dados

O sistema utiliza SQLite como banco de dados. O arquivo `tasks.db` é criado automaticamente na primeira execução.

### Tabela: tasks

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo       TEXT NOT NULL,
    description  TEXT NOT NULL,
    status       TEXT NOT NULL DEFAULT 'não iniciado',
    tag         TEXT,
    due_date    DATE,
    priority    TEXT DEFAULT 'média'
);
```

### Campos da Tabela

- `id`: Identificador único da tarefa (auto-incrementado)
- `titulo`: Título da tarefa (obrigatório)
- `description`: Descrição detalhada da tarefa (obrigatório)
- `status`: Status atual da tarefa (padrão: 'não iniciado')
  - Valores possíveis: 'não iniciado', 'em andamento', 'concluído'
- `tag`: Tag opcional para categorização
- `due_date`: Data limite para conclusão (formato: DD/MM/YYYY)
- `priority`: Nível de prioridade (padrão: 'média')
  - Valores possíveis: 'baixa', 'média', 'alta'

### Dados Iniciais

O banco de dados é criado vazio e não possui dados iniciais. Os dados são inseridos através da interface gráfica ou importação de CSV.

## Notas

- O banco de dados SQLite será criado automaticamente na primeira execução
- A localização está configurada para pt_BR
- As tarefas são salvas localmente no arquivo `tasks.db`
- O sistema suporta exportação e importação de dados em formato CSV

## Autores

- Thiago Godinho Pancieri
- Rafael Ferraresso de Freitas
- Victor Hugo Mendes de Sousa
- Nathália Chaves Teixeira
- Gabryel Gomes Linhares 
