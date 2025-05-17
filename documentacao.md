# Documentação do Sistema Task Planner

## Visão Geral

O Task Planner é um sistema de gerenciamento de tarefas desenvolvido em Python, utilizando a biblioteca Tkinter para a interface gráfica. O sistema foi projetado com uma arquitetura modular, separando as responsabilidades em diferentes componentes para facilitar a manutenção e extensão do código.

## Arquitetura do Sistema

O sistema foi desenvolvido seguindo princípios de modularização e separação de responsabilidades, sendo dividido em vários módulos:

### 1. Módulo de Configuração (`config.py`)
- Centraliza todas as configurações globais do sistema
- Define o esquema de cores da interface
- Configura a localização para português
- Define constantes como dimensões da janela e status possíveis das tarefas

### 2. Módulo de Modelo de Dados (`models.py`)
- Define a estrutura de dados das tarefas usando `@dataclass`
- Cada tarefa possui:
  - ID (identificador único)
  - Título
  - Descrição
  - Status
  - Tag (opcional)
  - Data limite
  - Prioridade

### 3. Módulo de Banco de Dados (`database.py`)
- Gerencia a persistência dos dados usando SQLite
- Possui duas classes principais:
  - `DatabaseInitializer`: Responsável pela inicialização e conexão com o banco
  - `TaskRepository`: Implementa as operações CRUD (Create, Read, Update, Delete)

### 4. Módulo de Componentes GUI (`gui_components.py`)
- Contém componentes reutilizáveis da interface
- Implementa:
  - Barra de menu
  - Lista de tarefas
  - Formulário de tarefa
  - Botões estilizados

### 5. Módulo GUI Principal (`gui.py`)
- Classe principal que integra todos os componentes
- Gerencia a lógica de negócio e eventos da interface
- Implementa funcionalidades como:
  - Adição/edição/remoção de tarefas
  - Filtros e ordenação
  - Exportação/importação CSV
  - Visualização em calendário

## Fluxo de Funcionamento

### 1. Inicialização
1. O sistema é iniciado através do `main.py`
2. A classe `PlannerGUI` é instanciada
3. O banco de dados é inicializado
4. A interface gráfica é construída
5. Os estilos visuais são aplicados

### 2. Operações Principais

#### Adição de Tarefa
1. Usuário preenche o formulário
2. Sistema valida os campos obrigatórios
3. Tarefa é persistida no banco de dados
4. Lista de tarefas é atualizada

#### Edição de Tarefa
1. Usuário seleciona uma tarefa na lista
2. Dados são carregados no formulário
3. Usuário modifica os campos desejados
4. Sistema atualiza os dados no banco
5. Lista é atualizada

#### Remoção de Tarefa
1. Usuário seleciona uma tarefa
2. Confirma a remoção
3. Sistema remove do banco de dados
4. Lista é atualizada

#### Filtros e Ordenação
1. Usuário define critérios de busca/filtro
2. Sistema consulta o banco de dados
3. Aplica os filtros em memória
4. Ordena conforme critério selecionado
5. Atualiza a visualização

### 3. Recursos Adicionais

#### Exportação CSV
1. Usuário seleciona local para salvar
2. Sistema recupera todas as tarefas
3. Converte para formato CSV
4. Salva no local especificado

#### Importação CSV
1. Usuário seleciona arquivo CSV
2. Sistema lê e valida os dados
3. Converte para objetos Task
4. Persiste no banco de dados
5. Atualiza a interface

#### Visualização em Calendário
1. Abre nova janela com calendário
2. Carrega todas as tarefas
3. Marca as datas com eventos
4. Permite visualização mensal

## Aspectos Técnicos

### Persistência de Dados
- Utiliza SQLite como banco de dados
- Arquivo `tasks.db` criado automaticamente
- Estrutura de tabela com todos os campos necessários

### Interface Gráfica
- Desenvolvida com Tkinter 

### Tratamento de Erros
- Validação de campos obrigatórios
- Tratamento de exceções do banco de dados
- Confirmação de ações críticas
