import tkinter as tk
from tkinter import filedialog, messagebox
from Lexical.Lexical import Lexical
from SymbolTable import SymbolTable
import os
import sys
from io import StringIO


class CompiladorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador 2019.1")
        self.root.geometry("800x600")

        # Criação do menu
        self.create_menu()

        # Frame para numeração de linhas e área de texto
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(fill="both", expand=True)

        # Text para numeração de linhas
        self.line_numbers = tk.Text(
            self.text_frame, width=4, padx=3, takefocus=0, border=0, background="#f0f0f0", state="disabled"
        )
        self.line_numbers.pack(side="left", fill="y")

        # Área de texto principal
        self.text_area = tk.Text(self.text_frame, wrap="none", undo=True)
        self.text_area.pack(side="right", fill="both", expand=True)

        # Vincula eventos para atualizar a numeração
        self.text_area.bind("<KeyRelease>", self.update_line_numbers)
        self.text_area.bind("<MouseWheel>", self.update_line_numbers)
        self.text_area.bind("<ButtonRelease>", self.update_line_numbers)

        # Área de mensagens
        self.message_area_frame = tk.Frame(self.root)
        self.message_area = tk.Text(
            self.message_area_frame, bg="#f0f0f0", relief="sunken", height=8
        )
        self.message_area.pack(fill="both", expand=True)
        self.message_area_frame.pack(fill="x")

        # Variáveis do compilador
        self.reset_compiler_state()

        # Atualiza numeração inicial
        self.update_line_numbers()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        # Menu principal
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Arquivo", menu=file_menu)

        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Salvar", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)

        compile_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Compilar", menu=compile_menu)

        compile_menu.add_command(label="Compilar", command=self.compile_code)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
                    self.update_line_numbers()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir o arquivo: {e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            try:
                with open(file_path, "w") as file:
                    content = self.get_assembly_output()
                    file.write(content)
                    messagebox.showinfo("Sucesso", "Arquivo salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}")

    def compile_code(self):
        code = self.text_area.get(1.0, tk.END).strip()
        if not code:
            self.update_message_area("Nenhum código para compilar.\n")
            return

        # Salva o código em um arquivo temporário para o compilador
        temp_file = "code.txt"
        with open(temp_file, "w") as file:
            file.write(code)

        # Redireciona stdout e stderr para capturar as mensagens
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

        try:
            # Inicializa o analisador léxico com o arquivo salvo
            self.lexer = Lexical(temp_file)

            # Aqui chamamos a lógica de compilação do seu código
            from main import main as compile_main
            compile_main()

            # Captura a saída padrão
            output = sys.stdout.getvalue()
            self.update_message_area(output)
        except Exception as e:
            # Captura a saída de erro
            error_output = sys.stderr.getvalue()
            self.update_message_area(f"Erro: {str(e)}\n{error_output}")
        finally:
            # Restaura stdout e stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            # Remove o arquivo temporário após a compilação
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def update_line_numbers(self, event=None):
        """
        Atualiza a numeração das linhas na área de texto.
        """
        self.line_numbers.config(state="normal")
        self.line_numbers.delete(1.0, tk.END)

        line_count = int(self.text_area.index("end-1c").split(".")[0])
        for line in range(1, line_count + 1):
            self.line_numbers.insert(tk.END, f"{line}\n")

        self.line_numbers.config(state="disabled")

    def reset_compiler_state(self):
        """
        Reseta as variáveis internas do compilador.
        """
        self.lexer = None
        self.symbol_table = SymbolTable()

    def update_message_area(self, message):
        """
        Atualiza a área de mensagens com o conteúdo fornecido.
        """
        self.message_area.delete(1.0, tk.END)
        self.message_area.insert(tk.END, message)

    def get_assembly_output(self):
        """
        Lê o arquivo assembly gerado e retorna o conteúdo como string.
        """
        assembly_file = "assembly.txt"
        if os.path.exists(assembly_file):
            with open(assembly_file, "r") as file:
                return file.read()
        return "Nenhum código assembly gerado."


if __name__ == "__main__":
    root = tk.Tk()
    app = CompiladorGUI(root)
    root.mainloop()
