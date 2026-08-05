import tkinter as tk
from tkinter import ttk
from controllers.nota_controller import NotaController


class AlunoView(tk.Tk):
    """Tela de visualização de notas para o aluno (somente leitura)."""

    def __init__(self, usuario: dict):
        super().__init__()
        self.usuario    = usuario
        self.controller = NotaController()
        self._configurar()
        self._criar_interface()
        self._carregar_dados()

    def _configurar(self):
        self.title(f"Sistema de Notas — {self.usuario['nome']}")
        self.geometry("640x400")
        self.resizable(False, False)
        self.configure(bg="#F0F4F8")
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - 640) // 2
        y = (self.winfo_screenheight() - 400) // 2
        self.geometry(f"640x400+{x}+{y}")

    def _criar_interface(self):
        # Top bar
        bar = tk.Frame(self, bg="#0B2545", pady=10)
        bar.pack(fill="x")
        tk.Label(bar, text="📚 Sistema de Notas",
                 font=("Arial", 13, "bold"), fg="#DFF0E8", bg="#0B2545").pack(side="left", padx=16)
        tk.Button(bar, text="⬡  Sair",
                  font=("Arial", 9), bg="#0B2545", fg="#7AAABB",
                  relief="flat", cursor="hand2",
                  activebackground="#0F2A45", activeforeground="white",
                  command=self._logout).pack(side="right", padx=16)
        tk.Label(bar, text=f"👤  {self.usuario['nome']}",
                 font=("Arial", 10), fg="#7AAABB", bg="#0B2545").pack(side="right", padx=4)

        # Aviso somente leitura
        aviso = tk.Frame(self, bg="#EBF8F2", pady=5)
        aviso.pack(fill="x")
        tk.Label(aviso, text="🔒  Modo de visualização — somente leitura",
                 font=("Arial", 9), fg="#1D9E75", bg="#EBF8F2").pack()

        # Tabela de notas
        frame = tk.LabelFrame(self, text=f" Notas de {self.usuario['nome']} ",
                              font=("Arial", 11, "bold"),
                              bg="#F0F4F8", fg="#0B2545",
                              bd=1, relief="groove")
        frame.pack(fill="both", expand=True, padx=14, pady=12)

        cols = ("Aluno", "Nota 1", "Nota 2", "Média", "Situação")
        self.tree = ttk.Treeview(frame, columns=cols,
                                  show="headings", selectmode="none")

        s = ttk.Style()
        s.configure("Treeview.Heading",
                    background="#0B2545", foreground="white",
                    font=("Arial", 10, "bold"))
        s.configure("Treeview", rowheight=32, font=("Arial", 11))

        for col, w in zip(cols, [200, 90, 90, 90, 140]):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")
        self.tree.column("Aluno", anchor="w")

        self.tree.tag_configure("aprovado",    background="#EAFAF1", foreground="#1D6A3E")
        self.tree.tag_configure("recuperacao", background="#FEF9E7", foreground="#7D6608")
        self.tree.tag_configure("reprovado",   background="#FDEDEC", foreground="#922B21")

        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        # Status bar
        self.status_var = tk.StringVar(value="Carregando...")
        tk.Label(self, textvariable=self.status_var,
                 font=("Arial", 9), bg="#E2E8F0", fg="#555",
                 anchor="w", padx=10, pady=4).pack(fill="x", side="bottom")

    def _carregar_dados(self):
        dados = self.controller.obter_dados_aluno(self.usuario["nome"])
        if dados:
            for row in dados:
                sit = str(row.get("Situação", ""))
                tag = ("aprovado" if sit == "Aprovado" else
                       "recuperacao" if sit == "Em Recuperação" else "reprovado")
                self.tree.insert("", "end",
                                 values=(row["Aluno"], row["Nota1"],
                                         row["Nota2"], row["Média"], row["Situação"]),
                                 tags=(tag,))
            self.status_var.set(f"Exibindo notas de {self.usuario['nome']}.")
        else:
            self.status_var.set("Nenhuma nota cadastrada ainda para este aluno.")

    def _logout(self):
        self.destroy()
        from views.login_view import LoginView
        LoginView().mainloop()
