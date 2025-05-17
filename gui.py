import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import Calendar
from datetime import datetime
import csv
from collections import defaultdict

from config import COLOR_SCHEME
from models import Task
from database import DatabaseInitializer, TaskRepository
from gui_components import (
    create_menu, create_task_list, create_task_form,
    create_button
)

class PlannerGUI:
    """
    Classe principal da interface gráfica do Planner.
    Responsável por criar e gerenciar todos os elementos visuais da aplicação.
    """
    def __init__(self):
        # Inicialização do banco de dados
        self.db_init = DatabaseInitializer()
        self.db_init.initialize_schema()
        self.repo = TaskRepository(self.db_init)

        # Configuração da janela principal
        self.root = tk.Tk()
        self.root.title("Planner")
        
        # Configurar janela para iniciar em tela cheia
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.state('zoomed')
        
        # Criação do menu
        create_menu(self.root, self)
        
        # Carrega ícone se existir
        try:
            icon_path = "icon.png"
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon)
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configuração dos estilos
        self._setup_styles()
        
        # Criação dos elementos da interface
        self._create_main_layout()
        
        # Carrega dados iniciais
        self.load_tasks()
        
        # Inicia a aplicação
        self.root.mainloop()

    def _setup_styles(self):
        """Configura os estilos visuais da aplicação"""
        style = ttk.Style(self.root)
        style.theme_use('clam')
        
        # Configuração do estilo da árvore de tarefas
        style.configure('Treeview', 
                       rowheight=30,
                       font=('Segoe UI', 10),
                       background=COLOR_SCHEME['bg'],
                       fieldbackground=COLOR_SCHEME['bg'],
                       foreground=COLOR_SCHEME['fg'])
                       
        style.configure('Treeview.Heading',
                       font=('Segoe UI', 11, 'bold'),
                       background=COLOR_SCHEME['accent'],
                       foreground='white',
                       padding=5)
                       
        style.map('Treeview.Heading',
                 background=[('active', COLOR_SCHEME['accent_dark'])])

        # Configuração das barras de rolagem
        for orientation in ['Vertical', 'Horizontal']:
            style.configure(f"Custom.{orientation}.TScrollbar",
                          background=COLOR_SCHEME['scrollbar'],
                          bordercolor=COLOR_SCHEME['bg'],
                          arrowcolor=COLOR_SCHEME['fg'],
                          troughcolor=COLOR_SCHEME['bg'],
                          width=10)
            
            style.map(f"Custom.{orientation}.TScrollbar",
                     background=[("pressed", COLOR_SCHEME['scrollbar_active']),
                               ("active", COLOR_SCHEME['scrollbar_hover'])])

        # Configuração do estilo do formulário
        style.configure('TLabelframe',
                       background=COLOR_SCHEME['form_bg'])
        style.configure('TLabelframe.Label',
                       background=COLOR_SCHEME['form_bg'],
                       foreground=COLOR_SCHEME['fg'],
                       font=('Segoe UI', 10, 'bold'))
        style.configure('TLabel',
                       background=COLOR_SCHEME['form_bg'],
                       foreground=COLOR_SCHEME['fg'])
        style.configure('TEntry',
                       fieldbackground=COLOR_SCHEME['bg'])
        style.configure('TCombobox',
                       fieldbackground=COLOR_SCHEME['bg'])
        style.configure('TFrame',
                       background=COLOR_SCHEME['form_bg'])

    def _create_main_layout(self):
        """Cria o layout principal da aplicação"""
        # Container principal com cor de fundo
        main_container = ttk.Frame(self.root, style='TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Configure the root window background
        self.root.configure(bg=COLOR_SCHEME['bg'])

        # Título
        title = ttk.Label(main_container, 
                         text="Planner",
                         font=('Segoe UI', 24, 'bold'),
                         foreground=COLOR_SCHEME['accent'],
                         background=COLOR_SCHEME['form_bg'])
        title.pack(pady=(0, 20))

        # Painel principal
        main_pane = ttk.PanedWindow(main_container, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True)

        # Área da lista de tarefas
        create_task_list(main_pane, self)
        
        # Área do formulário
        create_task_form(main_pane, self)

    def load_tasks(self):
        """Carrega as tarefas do banco de dados para a interface"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        tasks = self.repo.get_all()
        # Ordenar por data por padrão
        def get_date(task):
            if not task.due_date:
                return datetime.max
            try:
                return datetime.strptime(task.due_date, '%d/%m/%Y')
            except ValueError:
                return datetime.max
        tasks.sort(key=get_date)
        for t in tasks:
            self.tree.insert('', tk.END, values=(
                t.id, t.titulo, t.description, t.status, 
                t.tag or '', t.due_date or '', t.priority
            ))

    def clear_form(self):
        """Limpa todos os campos do formulário"""
        self.titulo_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.tag_entry.delete(0, tk.END)
        self.status_combobox.current(0)
        self.due_date_entry.set_date(datetime.now())
        self.priority_combobox.current(1)

    def on_select(self, event):
        """Manipula o evento de seleção de uma tarefa na lista"""
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0])['values']
        _, titulo, desc, status, tag, due_date, priority = values
        
        self.titulo_entry.delete(0, tk.END)
        self.titulo_entry.insert(0, titulo)
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, desc)
        self.tag_entry.delete(0, tk.END)
        self.tag_entry.insert(0, tag if tag else '')
        self.status_combobox.set(status)
        
        if due_date:
            try:
                date_obj = datetime.strptime(due_date, '%d/%m/%Y')
                self.due_date_entry.set_date(date_obj)
            except ValueError:
                self.due_date_entry.set_date(datetime.now())
        else:
            self.due_date_entry.set_date(datetime.now())
            
        self.priority_combobox.set(priority)

    def add_task(self):
        """Adiciona uma nova tarefa"""
        titulo = self.titulo_entry.get().strip()
        desc = self.desc_entry.get().strip()
        tag = self.tag_entry.get().strip()
        status = self.status_combobox.get()
        due_date = self.due_date_entry.get_date().strftime('%d/%m/%Y')
        priority = self.priority_combobox.get()
        
        if not titulo:
            messagebox.showwarning("Aviso", "Título é obrigatório.")
            return
            
        if not desc:
            messagebox.showwarning("Aviso", "Descrição é obrigatória.")
            return
            
        task = Task(id=None, titulo=titulo, description=desc, status=status,
                   tag=tag if tag else None, due_date=due_date, priority=priority)
        new_id = self.repo.add(task)
        
        if new_id != -1:
            messagebox.showinfo("Sucesso", f"Tarefa '{new_id}' adicionada.")
            self.load_tasks()
            self.clear_form()
        else:
            messagebox.showerror("Erro", "Falha ao adicionar tarefa.")

    def update_task(self):
        """Atualiza uma tarefa existente"""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para atualizar.")
            return
            
        task_id = self.tree.item(sel[0])['values'][0]
        titulo = self.titulo_entry.get().strip()
        desc = self.desc_entry.get().strip()
        tag = self.tag_entry.get().strip()
        status = self.status_combobox.get()
        due_date = self.due_date_entry.get_date().strftime('%d/%m/%Y')
        priority = self.priority_combobox.get()
        
        if not titulo:
            messagebox.showwarning("Aviso", "Título é obrigatório.")
            return
            
        if not desc:
            messagebox.showwarning("Aviso", "Descrição é obrigatória.")
            return
            
        task = Task(id=task_id, titulo=titulo, description=desc, status=status,
                   tag=tag if tag else None, due_date=due_date, priority=priority)
        if self.repo.update(task):
            messagebox.showinfo("Sucesso", f"Tarefa '{task_id}' atualizada.")
            self.load_tasks()
        else:
            messagebox.showerror("Erro", "Falha ao atualizar tarefa.")

    def delete_task(self):
        """Remove uma tarefa"""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para deletar.")
            return
        task_id = self.tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirmação", f"Remover tarefa '{task_id}'?"):
            if self.repo.delete(task_id):
                messagebox.showinfo("Sucesso", f"Tarefa '{task_id}' deletada.")
                self.load_tasks()
                self.clear_form()
            else:
                messagebox.showerror("Erro", "Falha ao deletar tarefa.")

    def _show_export_dialog(self):
        """Mostra diálogo de exportação CSV"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Salvar arquivo CSV"
        )
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['ID', 'Título', 'Descrição', 'Status', 'Tag', 'Data Limite', 'Prioridade'])
                    for task in self.repo.get_all():
                        writer.writerow([
                            task.id, task.titulo, task.description,
                            task.status, task.tag or '', task.due_date or '',
                            task.priority
                        ])
                messagebox.showinfo("Sucesso", "Tarefas exportadas com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")

    def _show_import_dialog(self):
        """Mostra diálogo de importação CSV"""
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Selecionar arquivo CSV"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        task = Task(
                            id=None,
                            titulo=row['Título'],
                            description=row['Descrição'],
                            status=row['Status'],
                            tag=row['Tag'] if row['Tag'] else None,
                            due_date=row['Data Limite'] if row['Data Limite'] else None,
                            priority=row['Prioridade']
                        )
                        self.repo.add(task)
                messagebox.showinfo("Sucesso", "Tarefas importadas com sucesso!")
                self.load_tasks()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao importar: {str(e)}")

    def _show_task_list_view(self):
        """Mostra a visualização em lista (atual)"""
        pass  # Já é a visualização padrão

    def _show_calendar_view(self):
        """Mostra a visualização em calendário com as tarefas"""
        calendar_window = tk.Toplevel(self.root)
        calendar_window.title("Calendário de Tarefas")
        calendar_window.geometry("800x600")
        
        # Frame principal
        main_frame = ttk.Frame(calendar_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Criar calendário
        cal = Calendar(main_frame, selectmode='day', 
                      date_pattern='dd/mm/yyyy',
                      showweeknumbers=False,
                      locale='pt_BR')
        cal.pack(fill=tk.BOTH, expand=True)
        
        # Marcar datas com tarefas
        tasks = self.repo.get_all()
        for task in tasks:
            if task.due_date:
                try:
                    date_obj = datetime.strptime(task.due_date, '%d/%m/%Y')
                    cal.calevent_create(date_obj, task.titulo, 'reminder')
                except ValueError:
                    continue

    def _apply_filters(self):
        """Aplica os filtros e ordenação na lista de tarefas"""
        tasks = self.repo.get_all()
        
        # Filtro de título
        title_search = self.search_title.get().lower().strip()
        if title_search:
            tasks = [t for t in tasks if title_search in t.titulo.lower()]
        
        # Filtro de tag
        tag_search = self.search_tag.get().lower().strip()
        if tag_search:
            tasks = [t for t in tasks if t.tag and tag_search in t.tag.lower()]
        
        # Filtro de status
        status_filter = self.filter_status.get()
        if status_filter != "Todos":
            tasks = [t for t in tasks if t.status == status_filter]
        
        # Ordenação
        sort_by = self.sort_by.get()
        if sort_by == "Data Limite":
            def get_date(task):
                if not task.due_date:
                    return datetime.max
                try:
                    return datetime.strptime(task.due_date, '%d/%m/%Y')
                except ValueError:
                    return datetime.max
            tasks.sort(key=get_date)
        elif sort_by == "Prioridade":
            priority_map = {"baixa": 0, "média": 1, "alta": 2}
            tasks.sort(key=lambda t: priority_map.get(t.priority, -1), reverse=True)
        elif sort_by == "Status":
            status_map = {"não iniciado": 0, "em andamento": 1, "concluído": 2}
            tasks.sort(key=lambda t: status_map.get(t.status, -1))
        
        # Atualizar a lista
        self.tree.delete(*self.tree.get_children())
        for t in tasks:
            self.tree.insert('', tk.END, values=(
                t.id, t.titulo, t.description, t.status, 
                t.tag or '', t.due_date or '', t.priority
            ))

    def _clear_filters(self):
        """Limpa todos os filtros e restaura a lista original"""
        self.search_title.delete(0, tk.END)
        self.search_tag.delete(0, tk.END)
        self.filter_status.set("Todos")
        self.sort_by.set("Data Limite")
        self.load_tasks()

    def on_closing(self):
        """Fecha a aplicação"""
        self.db_init.close()
        self.root.destroy() 
