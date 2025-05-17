import locale

# Configurar localização para português
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Configurações globais
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 600
WINDOW_DEFAULT_WIDTH = 1400
WINDOW_DEFAULT_HEIGHT = 700

# Esquema de cores do aplicativo
COLOR_SCHEME = {
    'bg': '#EBF5FB',           # Cor de fundo principal (azul muito claro)
    'fg': '#2C3E50',           # Cor do texto (azul escuro)
    'accent': '#2980B9',       # Cor de destaque (azul médio)
    'accent_dark': '#1F618D',  # Cor de destaque para hover
    'success': '#27AE60',      # Cor de sucesso (verde)
    'warning': '#E74C3C',      # Cor de aviso (vermelho)
    'scrollbar': '#c1c9d2',    # Cor da barra de rolagem (cinza claro)
    'scrollbar_hover': '#a3adb8',  # Cinza médio para hover
    'scrollbar_active': '#8895a3',  # Cinza escuro para active
    'menubar_bg': '#2980B9',   # Cor de fundo da barra de menu (azul médio)
    'menu_bg': '#f0f0f0',      # Cor de fundo do menu dropdown (cinza claro)
    'menu_fg': 'black',        # Cor do texto do menu
    'menu_hover_bg': '#e0e0e0', # Cor de hover do menu (cinza mais escuro)
    'form_bg': '#F5F8FA'       # Cor de fundo do formulário (azul mais claro que o bg)
}

# Status possíveis para as tarefas
TASK_STATUS = ["não iniciado", "em andamento", "concluído"] 
