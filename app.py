import tkinter as tk
import PyPDF2 
from tkinter import filedialog, messagebox
import os

class SearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Search Application")

        tk.Label(root, text="Palavra de Pesquisa:").grid(row=0, column=0, padx=10, pady=10)
        self.search_entry = tk.Entry(root, width=50)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Local da Pesquisa:").grid(row=1, column=0, padx=10, pady=10)
        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.grid(row=1, column=1, padx=10, pady=10)
        self.path_button = tk.Button(root, text="Selecionar Pasta", command=self.select_folder)
        self.path_button.grid(row=1, column=2, padx=10, pady=10)

        self.search_button = tk.Button(root, text="Iniciar Pesquisa", command=self.start_search)
        self.search_button.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(root, text="Saída:").grid(row=3, column=0, padx=10, pady=10)
        self.output_text = tk.Text(root, width=80, height=20)
        self.output_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.save_button = tk.Button(root, text="Salvar Saída", command=self.save_output)
        self.save_button.grid(row=5, column=1, padx=10, pady=10)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.insert(0, folder_selected)

    def start_search(self):
        search_word = self.search_entry.get().lower()
        search_path = self.path_entry.get()
        if not search_word or not search_path:
            messagebox.showwarning("Aviso", "Por favor, insira a palavra de pesquisa e selecione um local.")
            return
        self.output_text.delete(1.0, tk.END)
        for i in os.listdir(search_path):
            with open(f'{search_path}/{i}', 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                texto = ''
                for page in reader.pages:
                    texto += page.extract_text()

            if search_word in texto.lower():
                lista = texto.split('\n')
                for e, linha in enumerate(lista):
                    if 'REF:' in linha:
                        self.output_text.insert(tk.END, f'\n\npalavra: {search_word} \narquivo: {i} \n{lista[e]}')

    def save_output(self):
        output_content = self.output_text.get(1.0, tk.END)
        if not output_content.strip():
            messagebox.showwarning("Aviso", "Não há saída para salvar.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
            messagebox.showinfo("Sucesso", "Saída salva com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()
