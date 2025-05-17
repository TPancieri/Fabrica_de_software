import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from datetime import datetime
import csv
from config import COLOR_SCHEME, TASK_STATUS
from models import Task

def create_menu(root, gui):
    """Creates the main menu bar"""
    menubar = tk.Menu(root, bg=COLOR_SCHEME['menubar_bg'], fg='white')
    root.config(menu=menubar)
    
    # Menu Arquivo
    file_menu = tk.Menu(menubar, tearoff=0, bg=COLOR_SCHEME['menu_bg'], 
                      fg=COLOR_SCHEME['menu_fg'], 
                      activebackground=COLOR_SCHEME['menu_hover_bg'],
                      activeforeground=COLOR_SCHEME['menu_fg'])
    menubar.add_cascade(label="Arquivo", menu=file_menu, background=COLOR_SCHEME['menubar_bg'])
    file_menu.add_command(label="Exportar CSV", command=gui._show_export_dialog)
    file_menu.add_command(label="Importar CSV", command=gui._show_import_dialog)
    
    # Menu Visualizar
    view_menu = tk.Menu(menubar, tearoff=0, bg=COLOR_SCHEME['menu_bg'], 
                      fg=COLOR_SCHEME['menu_fg'], 
                      activebackground=COLOR_SCHEME['menu_hover_bg'],
                      activeforeground=COLOR_SCHEME['menu_fg'])
    menubar.add_cascade(label="Visualizar", menu=view_menu, background=COLOR_SCHEME['menubar_bg'])
    view_menu.add_command(label="Lista de Tarefas", command=gui._show_task_list_view)
    view_menu.add_command(label="Calendário", command=gui._show_calendar_view)

def create_task_list(parent, gui):
    """Creates the task list with Treeview"""
    frame_list = ttk.Frame(parent)
    parent.add(frame_list, weight=3)

    # Controles
    controls_frame = ttk.Frame(frame_list)
    controls_frame.pack(fill=tk.X, padx=5, pady=5)
    
    # Busca
    search_frame = ttk.LabelFrame(controls_frame, text="Buscar", padding=(5, 5, 5, 5))
    search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    ttk.Label(search_frame, text="Título:").pack(side=tk.LEFT, padx=(0, 5))
    gui.search_title = ttk.Entry(search_frame, width=20)
    gui.search_title.pack(side=tk.LEFT, padx=(0, 10))
    
    ttk.Label(search_frame, text="Tag:").pack(side=tk.LEFT, padx=(0, 5))
    gui.search_tag = ttk.Entry(search_frame, width=15)
    gui.search_tag.pack(side=tk.LEFT, padx=(0, 10))
    
    # Filtro
    filter_frame = ttk.LabelFrame(controls_frame, text="Filtros", padding=(5, 5, 5, 5))
    filter_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    ttk.Label(filter_frame, text="Status:").pack(side=tk.LEFT, padx=(0, 5))
    gui.filter_status = ttk.Combobox(filter_frame, values=["Todos"] + TASK_STATUS,
                                    state="readonly", width=15)
    gui.filter_status.set("Todos")
    gui.filter_status.pack(side=tk.LEFT, padx=(0, 10))
    
    # Sort
    sort_frame = ttk.LabelFrame(controls_frame, text="Ordenar por", padding=(5, 5, 5, 5))
    sort_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    gui.sort_by = ttk.Combobox(sort_frame, 
                               values=["Data Limite", "Prioridade", "Status"],
                               state="readonly", width=15)
    gui.sort_by.set("Data Limite")
    gui.sort_by.pack(side=tk.LEFT, padx=5)

    # Aplicar
    apply_btn = create_button(controls_frame, "Aplicar", gui._apply_filters)
    apply_btn.pack(side=tk.LEFT, padx=5)
    
    # Limpar 
    clear_btn = create_button(controls_frame, "Limpar", gui._clear_filters)
    clear_btn.pack(side=tk.LEFT, padx=5)

    # Treeview 
    tree_container = ttk.Frame(frame_list)
    tree_container.pack(fill=tk.BOTH, expand=True)
    
    cols = ('ID', 'Título', 'Descrição', 'Status', 'Tag', 'Data Limite', 'Prioridade')
    gui.tree = ttk.Treeview(tree_container, columns=cols, show='headings')
    
    column_config = {
        'ID': {'width': 80, 'minwidth': 80, 'anchor': tk.CENTER},
        'Título': {'width': 250, 'minwidth': 200, 'anchor': tk.W},
        'Descrição': {'width': 400, 'minwidth': 300, 'anchor': tk.W},
        'Status': {'width': 150, 'minwidth': 150, 'anchor': tk.CENTER},
        'Tag': {'width': 150, 'minwidth': 150, 'anchor': tk.CENTER},
        'Data Limite': {'width': 150, 'minwidth': 150, 'anchor': tk.CENTER},
        'Prioridade': {'width': 150, 'minwidth': 150, 'anchor': tk.CENTER}
    }
    
    for col, config in column_config.items():
        gui.tree.column(col, **config)
        gui.tree.heading(col, text=col)

    # Scrollbars
    y_scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, 
                              command=gui.tree.yview,
                              style="Custom.Vertical.TScrollbar")
    x_scrollbar = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL, 
                              command=gui.tree.xview,
                              style="Custom.Horizontal.TScrollbar")
    
    gui.tree.configure(yscroll=y_scrollbar.set, xscroll=x_scrollbar.set)
    
    gui.tree.grid(row=0, column=0, sticky='nsew')
    y_scrollbar.grid(row=0, column=1, sticky='ns')
    x_scrollbar.grid(row=1, column=0, sticky='ew')
    
    tree_container.grid_rowconfigure(0, weight=1)
    tree_container.grid_columnconfigure(0, weight=1)
    
    gui.tree.bind('<<TreeviewSelect>>', gui.on_select)

    return frame_list

def create_task_form(parent, gui):
    """Creates the task form"""
    frame_form = ttk.LabelFrame(parent, text="Detalhes da Tarefa", padding=(20, 10))
    parent.add(frame_form, weight=1)

    frame_form.grid_columnconfigure(1, weight=1)
    
    # Form fields
    ttk.Label(frame_form, text="Título:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=8)
    gui.titulo_entry = ttk.Entry(frame_form, width=30)
    gui.titulo_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=8)
    
    ttk.Label(frame_form, text="Descrição:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=8)
    gui.desc_entry = ttk.Entry(frame_form, width=30)
    gui.desc_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=8)
    
    ttk.Label(frame_form, text="Tag:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=8)
    gui.tag_entry = ttk.Entry(frame_form, width=30)
    gui.tag_entry.grid(row=2, column=1, sticky='ew', padx=10, pady=8)
    
    ttk.Label(frame_form, text="Status:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=8)
    gui.status_combobox = ttk.Combobox(frame_form, values=TASK_STATUS, state="readonly", width=28)
    gui.status_combobox.current(0)
    gui.status_combobox.grid(row=3, column=1, sticky='ew', padx=10, pady=8)
    
    ttk.Label(frame_form, text="Data Limite:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=8)
    gui.due_date_entry = DateEntry(frame_form, width=27, background='darkblue',
                                  foreground='white', borderwidth=2,
                                  locale='pt_BR', date_pattern='dd/mm/yyyy')
    gui.due_date_entry.grid(row=4, column=1, sticky='ew', padx=10, pady=8)
    
    ttk.Label(frame_form, text="Prioridade:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=8)
    gui.priority_combobox = ttk.Combobox(frame_form, values=["baixa", "média", "alta"],
                                         state="readonly", width=28)
    gui.priority_combobox.current(1)
    gui.priority_combobox.grid(row=5, column=1, sticky='ew', padx=10, pady=8)

    create_form_buttons(frame_form, gui)
    return frame_form

def create_form_buttons(parent, gui):
    """Creates the form buttons"""
    btn_frame = ttk.Frame(parent)
    btn_frame.grid(row=6, column=0, columnspan=2, pady=20, sticky='ew')
    
    btn_frame.grid_columnconfigure(0, weight=1)
    
    buttons = [
        ("Adicionar", gui.add_task),
        ("Salvar", gui.update_task),
        ("Deletar", gui.delete_task),
        ("Sair", lambda: gui.on_closing())
    ]
    
    for idx, (text, command) in enumerate(buttons):
        btn = create_button(btn_frame, text, command)
        btn.grid(row=idx, column=0, padx=5, pady=3, sticky='ew')

def create_button(parent, text, command):
    """Creates a styled button"""
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=('Segoe UI', 10),
        bg=COLOR_SCHEME['accent'],
        fg='white',
        activebackground=COLOR_SCHEME['accent_dark'],
        activeforeground='white',
        relief='flat',
        borderwidth=0,
        padx=15,
        pady=8,
        cursor='hand2'
    )
    
    # Hover effects
    btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=COLOR_SCHEME['accent_dark']))
    btn.bind('<Leave>', lambda e, b=btn: b.configure(bg=COLOR_SCHEME['accent']))
    
    return btn 
