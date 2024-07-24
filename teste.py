import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pdfplumber

class PDFReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Reader and Search")
        
        self.label = tk.Label()
        self.directory = tk.StringVar()
        self.search_word = tk.StringVar()
        self.output_text = tk.StringVar()

        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.root, text="PDF Directory:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.directory, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Browse", command=self.browse_directory).grid(row=0, column=2, padx=10, pady=10)
        
        tk.Label(self.root, text="Search Word:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.search_word, width=50).grid(row=2, column=1, padx=10, pady=10)
        
        tk.Button(self.root, text="Read PDFs", command=self.read_pdfs).grid(row=1, column=0, columnspan=3, pady=20)
        self.label.grid(row=1, column=2, padx=10, pady=10)
        tk.Button(self.root, text="Search", command=self.buscar_palavra).grid(row=3, column=0, columnspan=3, pady=10)

        tk.Label(root, text="Saída:").grid(row=3, column=0, padx=10, pady=10)
        self.output_text = tk.Text(root, width=100, height=40)
        self.output_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
    

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory.set(directory)
    
    def listar_caminhos_completos(self, diretorio):
        arquivos = os.listdir(diretorio)
        caminhos_completos = [os.path.join(diretorio, arquivo) for arquivo in arquivos if arquivo.endswith('.pdf')]
        return caminhos_completos
    
    def ler_pdf(self, caminho_arquivo):
        textos = []
        for e, arquivo in enumerate(caminho_arquivo):
            try:
                self.label.config(text=f"{e+1}/{len(caminho_arquivo)}")
                self.root.update_idletasks()
                print(f"Lendo arquivo {e+1}/{len(caminho_arquivo)}: {arquivo}")
                with pdfplumber.open(arquivo) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:  # Verifica se a extração de texto não é None
                            textos.append(f'##%##{text}\n')
            except Exception as ex:
                print(f"Erro ao ler o PDF {arquivo}: {ex}")
        return '\n'.join(textos)
    
    def read_pdfs(self):
        diretorio = self.directory.get()
        if not diretorio:
            messagebox.showerror("Error", "Please select a directory")
            return
        
        lista_de_arquivos = self.listar_caminhos_completos(diretorio)
        if not lista_de_arquivos:
            messagebox.showerror("Error", "No PDF files found in the selected directory")
            return
        
        textos = self.ler_pdf(lista_de_arquivos)
        with open('tudo.txt', 'w', encoding='utf-8') as arq:
            arq.write(textos)
        
        messagebox.showinfo("Success", "PDF files read and content saved to tudo.txt")
    
    def buscar_palavra(self):
        try:
            with open('tudo.txt', 'r', encoding='utf-8') as arq:
                conteudo = arq.read()
            palavra = self.search_word.get()
            conteudo = conteudo.split('##%##')
            resultados = []
            for arquivo in conteudo:
                print(conteudo)
                if palavra.lower() in arquivo.lower():
                    lista = arquivo.split('\n')
                    for e, linha in enumerate(lista):
                        if 'REF:' in linha:
                            resultados.append(f'\nPalavra: {palavra} \nRef: {lista[e]}')
            print(palavra)
            with open('resposta.txt', 'w', encoding='utf-8') as arq:
                arq.write('\n\n'.join(resultados))
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, '\n\n'.join(resultados))
        except: 
            messagebox.showerror("Error", "Leia os pdfs antes de procurar a palavra")


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFReaderApp(root)
    root.mainloop()
