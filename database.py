import os
import sqlite3
from models import Task

class DatabaseInitializer:
    """
    Classe responsável por inicializar e gerenciar a conexão com o banco de dados SQLite.
    """
    def __init__(self, db_path: str = None):
        """
        Inicializa o gerenciador de banco de dados.
        :param db_path: Caminho opcional para o arquivo do banco de dados
        """
        if db_path:
            self.db_path = db_path
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(base_dir, "tasks.db")
        self.conn: sqlite3.Connection | None = None

    def connect(self) -> sqlite3.Connection:
        """Estabelece conexão com o banco de dados"""
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def initialize_schema(self) -> None:
        """
        Inicializa o esquema do banco de dados.
        Cria a tabela de tarefas se não existir.
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT due_date FROM tasks LIMIT 1")
            needs_create = False
        except sqlite3.OperationalError:
            needs_create = True
            cursor.execute("DROP TABLE IF EXISTS tasks")
            
        if needs_create:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo       TEXT NOT NULL,
                    description  TEXT NOT NULL,
                    status       TEXT NOT NULL DEFAULT 'não iniciado',
                    tag         TEXT,
                    due_date    DATE,
                    priority    TEXT DEFAULT 'média'
                );
            """)
            conn.commit()

    def close(self) -> None:
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
            self.conn = None

class TaskRepository:
    """
    Classe responsável por realizar operações CRUD (Create, Read, Update, Delete)
    no banco de dados para as tarefas.
    """
    def __init__(self, db_init: DatabaseInitializer):
        self.conn = db_init.connect()

    def add(self, task: Task) -> int:
        """
        Adiciona uma nova tarefa ao banco de dados
        :param task: Objeto Task a ser adicionado
        :return: ID da tarefa criada ou -1 em caso de erro
        """
        try:
            cursor = self.conn.execute(
                "INSERT INTO tasks (titulo, description, status, tag, due_date, priority) VALUES (?, ?, ?, ?, ?, ?)",
                (task.titulo, task.description, task.status, task.tag, task.due_date, task.priority)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error:
            return -1

    def get_all(self) -> list[Task]:
        """Retorna todas as tarefas do banco de dados"""
        cur = self.conn.execute("SELECT id, titulo, description, status, tag, due_date, priority FROM tasks")
        return [Task(id=row[0], titulo=row[1], description=row[2], status=row[3], tag=row[4], due_date=row[5], priority=row[6]) 
                for row in cur.fetchall()]

    def update(self, task: Task) -> bool:
        """
        Atualiza uma tarefa existente
        :param task: Objeto Task com as informações atualizadas
        :return: True se a atualização foi bem sucedida
        """
        cur = self.conn.execute(
            "UPDATE tasks SET titulo = ?, description = ?, status = ?, tag = ?, due_date = ?, priority = ? WHERE id = ?",
            (task.titulo, task.description, task.status, task.tag, task.due_date, task.priority, task.id)
        )
        self.conn.commit()
        return cur.rowcount > 0

    def delete(self, task_id: int) -> bool:
        """
        Remove uma tarefa do banco de dados
        :param task_id: ID da tarefa a ser removida
        :return: True se a remoção foi bem sucedida
        """
        cur = self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def exists(self, task_id: int) -> bool:
        """Verifica se uma tarefa existe no banco de dados"""
        cur = self.conn.execute("SELECT 1 FROM tasks WHERE id = ?", (task_id,))
        return cur.fetchone() is not None 
