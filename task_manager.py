import os, json
import tkinter as tk
from tkinter import messagebox

#TODO implementar visual
#TODO tag de progresso? não iniciado/ em andamento/ concluido 

class Planner:

    FILE_NAME = "tasks.txt"

    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Tarefas")
        self.root.geometry("400x500")
        
        
        self.tasks = {}
        self.load_tasks()
        
        self.label = tk.Label(root, text="Gerenciador de Tarefas", font=(
            "Arial", 14, "bold"
        ))
        
    #def clear_screen(self):
        # da um cls no terminal, quando for pro visual isso sai
        #os.system("cls" if os.name == "nt" else "clear")

    def load_tasks(self):
        # puxa o arquivo que salva as tarefas
        if os.path.exists(self.FILE_NAME):
            try:
                with open(self.FILE_NAME, "r") as file:
                    self.tasks = json.load(file)
            except json.JSONDecodeError:
                # se não conseguir abrir , cria um novo
                self.tasks = {}
    
    def save_tasks(self):
        # salva as tarefas no arquivo
        with open(self.FILE_NAME, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def create_task(self):
        # cria uma nova tarefa se o ID não for repetir, adiciona uma descrição
        task_id = input ("Entre o ID da tarefa: ").strip()
        if not task_id or task_id in self.tasks:
            print("ID da tarefa não pode ser vazio ou repetido")
            return

        task_desc = input("Insira a descrição da tarefa: ").strip()
        if not task_desc:
            print("Descrição da tarefa não pode ser vazia")
            return 
        
        self.tasks[task_id] = task_desc
        self.save_tasks()
        print(f"Tarefa {task_id} adicionada com sucesso")

    def read_tasks(self):
        # Le as tarefas registradas no arquivo
        if not self.tasks:
            print("Nenhuma tarefa registrada / disponivel")
            return

        print("\n Tarefas Atuais: ")
        for task_id, task_desc in self.tasks.items():
            print(f" {task_id}: {task_desc} ")
        print()

    def update_task(self):
        # Atualiza uma tarefa especificada no arquivo
        task_id = input("Insira o ID que sera atualizado: ").strip()
        if task_id not in self.tasks:
            print("ID de tarefa não encontrada")
            return
        
        new_desc = input("Insira a nova descrição: ").strip()
        if not new_desc:
            print("Descrição da tarefa não pode ser vazia")
            return
        
        self.tasks[task_id] = new_desc
        self.save_tasks()
        print(f"Tarefa '{task_id}' atualizada com sucesso")

    def delete_task(self):
        # deleta uma ID do arquivo
        # Adicionar segunda camada de confirmação / proteção pra não deixar deletar por erro
        task_id = input("Insira a ID para ser deletada: ").strip()
        if task_id not in self.tasks:
            print("ID de tarefa não encontrada")
            return
        
        del self.tasks[task_id]
        self.save_tasks()
        print(f"Tarefa '{task_id} deletada com sucesso'")
    
    def exit_program(self):
        self.clear_screen()
        print("Fechando o Planner")
        exit()

    def menu(self):
        options = {
            "1": self.create_task,
            "2": self.read_tasks,
            "3": self.update_task,
            "4": self.delete_task,
            "5": self.exit_program
        }

        while True:
            # self.clear_screen()
            print("\n Aplicativo Planner")
            print("1. Criar Tarefa")
            print("2. Ver Tarefas")
            print("3. Atualizar Tarefas")
            print("4. Deletar Tarefas")
            print("5. Sair")

            choice = input("Escolha uma opção: ").strip()
            action = options.get(choice)

            if action:
                self.clear_screen()
                action()
            else:
                print("Opção invalada tente novamente")
            

if __name__ == "__main__":
    root = tk.Tk()
    planner = Planner(root)
    #planner.menu()
    root.mainloop()
