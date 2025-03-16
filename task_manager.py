import os, json
import tkinter as tk
from tkinter import messagebox, simpledialog

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
        print("DEBUG", self.tasks)
        
        
        self.label = tk.Label(root, text="Gerenciador de Tarefas", font=(
            "Arial", 14, "bold"
        ))
        self.label.pack(pady=10)
        
        # Lista de Tarefas
        self.task_listbox = tk.Listbox(root, width=50, height=15)
        self.task_listbox.pack(pady=10)
        
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)  

        # Botão para criar
        self.create_button = tk.Button(button_frame, text="Adicionar Tarefa", command=self.create_task_popup)
        self.create_button.pack(side=tk.LEFT, padx=10)
        
        # Botão para carregar
        self.load_button = tk.Button(button_frame, text="Carregar Tarefas", command=self.display_tasks)
        self.load_button.pack(side=tk.LEFT, padx=10)
        
        # Botão para atualizar tarefa
        self.update_button = tk.Button(button_frame, text="Atualizar Tarefa", command=self.update_task_popup)
        self.update_button.pack(side=tk.LEFT, padx=10)

    def load_tasks(self):
        if not os.path.exists(self.FILE_NAME):
            print("DEBUG - Arquivo tasks.txt não encontrado. Criando um novo...")
            with open(self.FILE_NAME, "w") as file:
                json.dump({}, file)  
        
        try:
            with open(self.FILE_NAME, "r") as file:
                content = file.read().strip()
                
                # Se o arquivo estiver vazio, inicializa com um dicionário vazio
                if not content:
                    print("DEBUG - Arquivo tasks.txt está vazio. Inicializando tarefas.")
                    self.tasks = {}
                else:
                    self.tasks = json.loads(content) 
                    print("DEBUG - Tarefas carregadas:", self.tasks)
                    
        except json.JSONDecodeError as e:
            print(f"ERRO - Falha ao carregar JSON: {e}. Criando um novo arquivo...")
            self.tasks = {}
            with open(self.FILE_NAME, "w") as file:
                json.dump(self.tasks, file)  # Recria o arquivo vazio
                
    def display_tasks(self):
        
        print("DEBUG - Tentando exibir tarefas:", self.tasks)  # Debugging
        self.task_listbox.delete(0, tk.END) # clear 
        
        if not self.tasks:
            print("DEBUG - Nenhuma tarefa encontrada.")  # Debugging
            return
        
        for task_id, task_desc in self.tasks.items():
            #DEBUG
            print("DEBUG - Tarefas carregadas: ", self.tasks)
            self.task_listbox.insert(tk.END, f"{task_id}: {task_desc}")
    
    def save_tasks(self):
        # salva as tarefas no arquivo
        with open(self.FILE_NAME, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def create_task_popup(self):
        task_id = simpledialog.askstring("ID da Tarefa", "Insira o ID da tarefa:")
        if not task_id or task_id in self.tasks:
            messagebox.showerror("Erro", "ID da tarefa não pode ser vazio ou repetido.")
            return
        
        task_desc = simpledialog.askstring("Descrição da Tarefa", "Insira a descrição da tarefa:")
        if not task_desc:
            messagebox.showerror("Erro", "Descrição da tarefa não pode ser vazia.")
            return

        self.tasks[task_id] = task_desc
        self.save_tasks()
        messagebox.showinfo("Sucesso", f"Tarefa '{task_id}' adicionada com sucesso.")
        self.display_tasks()
        
    def update_task_popup(self):
        # Janela nova
        update_window = tk.Toplevel(self.root)
        update_window.title("Atualizar Tarefa")
    
        task_id_label = tk.Label(update_window, text="ID da Tarefa:")
        task_id_label.pack(pady=5)
        task_id_entry = tk.Entry(update_window)
        task_id_entry.pack(pady=5)

        new_desc_label = tk.Label(update_window, text="Nova Descrição:")
        new_desc_label.pack(pady=5)
        new_desc_entry = tk.Entry(update_window)
        new_desc_entry.pack(pady=5)
    
        def update_task():
            task_id = task_id_entry.get().strip()
            new_desc = new_desc_entry.get().strip()

            if not task_id or task_id not in self.tasks:
                messagebox.showerror("Erro", "ID de tarefa não encontrado!")
                return
        
            if not new_desc:
                messagebox.showerror("Erro", "Descrição não pode ser vazia!")
                return
        
            self.tasks[task_id] = new_desc
            self.save_tasks()
            messagebox.showinfo("Sucesso", f"Tarefa '{task_id}' atualizada com sucesso!")
            
            self.display_tasks()
            update_window.destroy()  # Fecha janela

        # Update Button
        update_button = tk.Button(update_window, text="Atualizar", command=update_task)
        update_button.pack(pady=10)
    
    #def read_tasks(self):
        # Le as tarefas registradas no arquivo
        #if not self.tasks:
            #print("Nenhuma tarefa registrada / disponivel")
            #return

        #print("\n Tarefas Atuais: ")
        #for task_id, task_desc in self.tasks.items():
            #print(f" {task_id}: {task_desc} ")
        #print()

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
    root.mainloop()
