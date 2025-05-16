import os
import sqlite3
from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk, messagebox

#TODO melhorar a implementação visual (layout, botões, icones)
#TODO separar as tarefas em 3 colunas / listas : Backlog, Em Andamento, Concluido
#TODO Fazer conexão com banco de dados (retirar arquivo txt)
#TODO Adicionar confirmação para deletar um arquivo
#TODO Deixar o ID das tarefas Auto increment - não permitir o usuário alterar
#TODO Talvez implementar um sistema de login, agregando tarefa por usuário

# 1) Inicializador do Banco de Dados
class DatabaseInitializer:
    def __init__(self, db_path: str = None):
        if db_path:
            self.db_path = db_path
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(base_dir, "tasks.db")
        self.conn: sqlite3.Connection | None = None

    def connect(self) -> sqlite3.Connection:
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def initialize_schema(self) -> None:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id           TEXT PRIMARY KEY,
                description  TEXT NOT NULL,
                status       TEXT NOT NULL DEFAULT 'não iniciado'
            );
            """
        )
        conn.commit()

    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None

# 2) Modelo de Domínio
@dataclass
class Task:
    id: str
    description: str
    status: str = "não iniciado"

# 3) Repositório para CRUD
class TaskRepository:
    def __init__(self, db_init: DatabaseInitializer):
        self.conn = db_init.connect()

    def add(self, task: Task) -> bool:
        try:
            self.conn.execute(
                "INSERT INTO tasks (id, description, status) VALUES (?, ?, ?)",
                (task.id, task.description, task.status)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all(self) -> list[Task]:
        cur = self.conn.execute("SELECT id, description, status FROM tasks")
        return [Task(id=row[0], description=row[1], status=row[2]) for row in cur.fetchall()]

    def update(self, task: Task) -> bool:
        cur = self.conn.execute(
            "UPDATE tasks SET description = ?, status = ? WHERE id = ?",
            (task.description, task.status, task.id)
        )
        self.conn.commit()
        return cur.rowcount > 0

    def delete(self, task_id: str) -> bool:
        cur = self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def exists(self, task_id: str) -> bool:
        cur = self.conn.execute("SELECT 1 FROM tasks WHERE id = ?", (task_id,))
        return cur.fetchone() is not None

# 4) Interface Tkinter com Treeview moderna

def on_closing(gui):
    gui.db_init.close()
    gui.root.destroy()

class PlannerGUI:
    def __init__(self):
        # Inicializa banco e repositório
        self.db_init = DatabaseInitializer()
        self.db_init.initialize_schema()
        self.repo = TaskRepository(self.db_init)

        # Janela principal
        self.root = tk.Tk()
        self.root.title("Task Manager")
        self.root.geometry("1250x450")
        self.root.protocol("WM_DELETE_WINDOW", lambda: on_closing(self))

        # Estilo moderno
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('Treeview', rowheight=24, font=('Segoe UI', 10))
        style.configure('Treeview.Heading', font=('Segoe UI', 11, 'bold'))
        style.configure('TButton', font=('Segoe UI', 10), padding=6)
        style.configure('TLabel', font=('Segoe UI', 10))
        style.configure('TEntry', font=('Segoe UI', 10))
        style.configure('TCombobox', font=('Segoe UI', 10))

        # Título
        title = ttk.Label(self.root, text="Task Manager", font=('Segoe UI', 16, 'bold'))
        title.pack(pady=10)

        # Divisão principal
        main_pane = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # Frame da lista
        frame_list = ttk.Frame(main_pane)
        main_pane.add(frame_list, weight=3)

        # Treeview para exibir tarefas
        cols = ('ID', 'Descrição', 'Status')
        self.tree = ttk.Treeview(frame_list, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
            if col == 'Descrição':
                self.tree.column(col, width=300)
            else:
                self.tree.column(col, width=100, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar = ttk.Scrollbar(frame_list, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Frame do formulário
        frame_form = ttk.LabelFrame(main_pane, text="Detalhes da Tarefa")
        main_pane.add(frame_form, weight=1)

        # Campos do formulário
        ttk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky=tk.W, padx=6, pady=4)
        self.id_entry = ttk.Entry(frame_form, width=20)
        self.id_entry.grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(frame_form, text="Descrição:").grid(row=1, column=0, sticky=tk.W, padx=6, pady=4)
        self.desc_entry = ttk.Entry(frame_form, width=30)
        self.desc_entry.grid(row=1, column=1, padx=6, pady=4)

        ttk.Label(frame_form, text="Status:").grid(row=2, column=0, sticky=tk.W, padx=6, pady=4)
        self.status_combobox = ttk.Combobox(
            frame_form,
            values=["não iniciado", "em andamento", "concluído"],
            state="readonly",
            width=18
        )
        self.status_combobox.grid(row=2, column=1, padx=6, pady=4)
        self.status_combobox.current(0)

        # Botões principais
        btn_frame = ttk.Frame(frame_form)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=12)
        ttk.Button(btn_frame, text="Adicionar", command=self.add_task).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Salvar Alterações", command=self.update_task).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Deletar", command=self.delete_task).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Sair", command=lambda: on_closing(self)).pack(side=tk.LEFT, padx=4)

        # Carrega dados e inicia GUI
        self.load_tasks()
        self.root.mainloop()

    def load_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for t in self.repo.get_all():
            self.tree.insert('', tk.END, values=(t.id, t.description, t.status))

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0])['values']
        id_, desc, status = values
        self.id_entry.delete(0, tk.END); self.id_entry.insert(0, id_)
        self.desc_entry.delete(0, tk.END); self.desc_entry.insert(0, desc)
        self.status_combobox.set(status)

    def add_task(self):
        id_ = self.id_entry.get().strip()
        desc = self.desc_entry.get().strip()
        status = self.status_combobox.get()
        if not id_ or not desc:
            messagebox.showwarning("Aviso", "ID e Descrição são obrigatórios.")
            return
        if self.repo.exists(id_):
            messagebox.showwarning("Aviso", "ID já existente.")
            return
        if self.repo.add(Task(id=id_, description=desc, status=status)):
            messagebox.showinfo("Sucesso", f"Tarefa '{id_}' adicionada.")
            self.load_tasks()
        else:
            messagebox.showerror("Erro", "Falha ao adicionar tarefa.")

    def update_task(self):
        id_ = self.id_entry.get().strip()
        desc = self.desc_entry.get().strip()
        status = self.status_combobox.get()
        if not id_ or not desc:
            messagebox.showwarning("Aviso", "ID e Descrição são obrigatórios.")
            return
        if not self.repo.exists(id_):
            messagebox.showwarning("Aviso", "ID não encontrado.")
            return
        if self.repo.update(Task(id=id_, description=desc, status=status)):
            messagebox.showinfo("Sucesso", f"Tarefa '{id_}' atualizada.")
            self.load_tasks()
        else:
            messagebox.showerror("Erro", "Falha ao atualizar tarefa.")

    def delete_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para deletar.")
            return
        id_ = self.tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirmação", f"Remover tarefa '{id_}'?"):
            if self.repo.delete(id_):
                messagebox.showinfo("Sucesso", f"Tarefa '{id_}' deletada.")
                self.load_tasks()
            else:
                messagebox.showerror("Erro", "Falha ao deletar tarefa.")

if __name__ == "__main__":
    PlannerGUI()