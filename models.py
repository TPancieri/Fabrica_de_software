from dataclasses import dataclass

@dataclass
class Task:
    """
    Classe que representa uma tarefa no sistema.
    Utiliza dataclass para simplificar a criação de objetos.
    """
    id: int | None
    titulo: str
    description: str
    status: str = "não iniciado"
    tag: str | None = None
    due_date: str | None = None
    priority: str = "média" 
