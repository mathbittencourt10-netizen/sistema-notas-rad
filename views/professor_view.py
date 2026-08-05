import tkinter as tk
from tkinter import ttk, messagebox
from controllers.nota_controller import NotaController
from models.aluno import Aluno


class ProfessorView(tk.Tk):
    """Dashboard completo para o professor."""

    def __init__(self, usuario: dict):
        super().__init__()
        self.usuario    = usuario
        self.controller = NotaController()
        self.aluno_selecionado = None
        self.filtro_var   = tk.StringVar(value="Todos")
        self.btns_filtro  = {}
        self._configurar()
        self._criar_interface()
        self._carregar_tabela()

    def _configurar(self):
        self.title("Sistema de Notas — Professor")
        self.geometry("920x580")
        self.minsize(800, 500)
        self.configure(bg="#F0F4F8")
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - 920) // 2
        y = (self.winfo_screenheight() - 580) // 2
        self.geometry(f"920x580+{x}+{y}")

    # ── Layout ─────────────────────────────────────────────────────────────
    def _criar_interface(self):
        self._criar_topbar()
        corpo = tk.Frame(self, bg="#F0F4F8")
        corpo.pack(fill="both", expand=True, padx=14, pady=12)
        self._criar_formulario(corpo)
        self._criar_painel_tabela(corpo)
        self._criar_statusbar()

    def _criar_topbar(self):
        bar = tk.Frame(self, bg="#0B2545", pady=10)
        bar.pack(fill="x")
        tk.Label(bar, text="📚 Sistema de Notas",
                 font=("Arial", 14, "bold"), fg="#DFF0E8", bg="#0B2545").pack(side="left", padx=16)
        tk.Button(bar, text="⬡  Sair",
                  font=("Arial", 9), bg="#0B2545", fg="#7AAABB",
                  relief="flat", cursor="hand2",
                  activebackground="#0F2A45", activeforeground="white",
                  command=self._logout).pack(side="right", padx=16)
        tk.Label(bar, text=f"👤  {self.usuario['nome']}",
                 font=("Arial", 10), fg="#7AAABB", bg="#0B2545").pack(side="right", padx=4)

    def _criar_formulario(self, parent):
        frame = tk.LabelFrame(parent, text=" Dados do Aluno ",
                              font=("Arial", 10, "bold"),
                              bg="#F0F4F8", fg="#0B2545",
                              bd=1, relief="groove", padx=14, pady=12)
        frame.pack(side="left", fill="y", padx=(0, 10))
        frame.config(width=265)
        frame.pack_propagate(False)

        self.entry_nome  = self._campo(frame, "Nome do Aluno *")
        self.entry_nota1 = self._campo(frame, "Nota 1  (0 – 10) *")
        self.entry_nota2 = self._campo(frame, "Nota 2  (0 – 10) *")

        tk.Frame(frame, bg="#F0F4F8", height=6).pack()

        self.btn_adicionar = self._botao(frame, "✔  Adicionar",  "#1D9E75", self._adicionar)
        self.btn_atualizar = self._botao(frame, "✎  Salvar Alterações", "#1C7293", self._atualizar, state="disabled")
        self._botao(frame, "✕  Limpar", "#718096", self._limpar)

        # Legenda
        tk.Frame(frame, bg="#E2E8F0", height=1).pack(fill="x", pady=10)
        tk.Label(frame, text="SITUAÇÃO", font=("Arial", 8, "bold"),
                 fg="#888", bg="#F0F4F8").pack(anchor="w")
        for cor, txt in [("#27AE60", "≥ 7,0  —  Aprovado"),
                         ("#F39C12", "≥ 5,0  —  Em Recuperação"),
                         ("#E74C3C", "< 5,0  —  Reprovado")]:
            row = tk.Frame(frame, bg="#F0F4F8")
            row.pack(anchor="w", pady=2)
            tk.Label(row, bg=cor, width=2, height=1).pack(side="left", padx=(0, 6))
            tk.Label(row, text=txt, font=("Arial", 8), fg="#444", bg="#F0F4F8").pack(side="left")

    def _campo(self, parent, label: str) -> tk.Entry:
        tk.Label(parent, text=label, font=("Arial", 9),
                 fg="#555", bg="#F0F4F8").pack(anchor="w")
        e = tk.Entry(parent, font=("Arial", 11), relief="solid", bd=1)
        e.pack(fill="x", pady=(2, 10), ipady=4)
        return e

    def _botao(self, parent, texto, cor, cmd, state="normal"):
        btn = tk.Button(parent, text=texto, font=("Arial", 10, "bold"),
                        bg=cor, fg="white", relief="flat", cursor="hand2",
                        pady=7, state=state, command=cmd,
                        activeforeground="white")
        btn.pack(fill="x", pady=(0, 5))
        return btn

    def _criar_painel_tabela(self, parent):
        frame = tk.LabelFrame(parent, text=" Alunos Cadastrados ",
                              font=("Arial", 10, "bold"),
                              bg="#F0F4F8", fg="#0B2545",
                              bd=1, relief="groove")
        frame.pack(side="left", fill="both", expand=True)

        # Barra de busca
        barra = tk.Frame(frame, bg="#F0F4F8", pady=8, padx=10)
        barra.pack(fill="x")
        tk.Label(barra, text="🔍", bg="#F0F4F8", font=("Arial", 11)).pack(side="left")
        self.entry_busca = tk.Entry(barra, font=("Arial", 10), relief="solid", bd=1)
        self.entry_busca.pack(side="left", fill="x", expand=True, padx=(4, 10), ipady=3)
        self.entry_busca.bind("<KeyRelease>", lambda e: self._buscar())
        tk.Button(barra, text="🗑  Excluir Selecionado",
                  font=("Arial", 10, "bold"), bg="#C0392B", fg="white",
                  relief="flat", cursor="hand2",
                  activebackground="#A93226", activeforeground="white",
                  command=self._excluir).pack(side="right")

        # Filtro por situação
        filtro_frame = tk.Frame(frame, bg="#F0F4F8", padx=10, pady=2)
        filtro_frame.pack(fill="x")
        tk.Label(filtro_frame, text="Filtrar:", font=("Arial", 9),
                 fg="#555", bg="#F0F4F8").pack(side="left", padx=(0, 6))
        for label, cor_ativa, cor_inativa, fg_inativa in [
            ("Todos",          "#718096", "#E2E8F0", "#718096"),
            ("Aprovado",       "#27AE60", "#EAFAF1", "#27AE60"),
            ("Em Recuperação", "#F39C12", "#FEF9E7", "#F39C12"),
            ("Reprovado",      "#E74C3C", "#FDEDEC", "#E74C3C"),
        ]:
            btn = tk.Button(filtro_frame, text=label,
                            font=("Arial", 9), relief="flat", cursor="hand2",
                            padx=10, pady=3,
                            command=lambda l=label: self._aplicar_filtro(l))
            btn.pack(side="left", padx=2)
            self.btns_filtro[label] = (btn, cor_ativa, cor_inativa, fg_inativa)
        self._atualizar_botoes_filtro("Todos")

        # Treeview
        cols = ("Aluno", "Nota 1", "Nota 2", "Média", "Situação")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")

        s = ttk.Style()
        s.configure("Treeview.Heading",
                    background="#F0F4F8", foreground="black",
                    font=("Arial", 10, "bold"))
        s.configure("Treeview", rowheight=28, font=("Arial", 10))
        s.map("Treeview", background=[("selected", "#1C7293")])

        for col, w in zip(cols, [200, 80, 80, 80, 140]):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")
        self.tree.column("Aluno", anchor="w")

        self.tree.tag_configure("aprovado",    background="#EAFAF1")
        self.tree.tag_configure("recuperacao", background="#FEF9E7")
        self.tree.tag_configure("reprovado",   background="#FDEDEC")

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=(0, 8))
        sb.pack(side="right", fill="y", pady=(0, 8), padx=(0, 4))
        self.tree.bind("<<TreeviewSelect>>", self._selecionar)

    def _criar_statusbar(self):
        self.status_var = tk.StringVar(value="Pronto.")
        tk.Label(self, textvariable=self.status_var,
                 font=("Arial", 9), bg="#E2E8F0", fg="#555",
                 anchor="w", padx=10, pady=4).pack(fill="x", side="bottom")

    # ── Ações ──────────────────────────────────────────────────────────────
    def _status(self, msg: str):
        self.status_var.set(msg)

    def _carregar_tabela(self, dados=None):
        self.tree.delete(*self.tree.get_children())
        if dados is None:
            dados = self.controller.listar_todos()
        for row in dados:
            sit = str(row.get("Situação", ""))
            tag = ("aprovado" if sit == "Aprovado" else
                   "recuperacao" if sit == "Em Recuperação" else "reprovado")
            self.tree.insert("", "end",
                             values=(row["Aluno"], row["Nota1"],
                                     row["Nota2"], row["Média"], row["Situação"]),
                             tags=(tag,))

    def _selecionar(self, _event=None):
        sel = self.tree.selection()
        if sel:
            v = self.tree.item(sel[0])["values"]
            self.aluno_selecionado = str(v[0])
            for entry, val in zip(
                [self.entry_nome, self.entry_nota1, self.entry_nota2], v[:3]
            ):
                entry.delete(0, "end")
                entry.insert(0, val)
            self.btn_adicionar.config(state="disabled")
            self.btn_atualizar.config(state="normal")

    def _limpar(self):
        for e in (self.entry_nome, self.entry_nota1, self.entry_nota2, self.entry_busca):
            e.delete(0, "end")
        self.aluno_selecionado = None
        self.btn_adicionar.config(state="normal")
        self.btn_atualizar.config(state="disabled")
        self.tree.selection_remove(self.tree.selection())
        self._carregar_tabela()

    def _obter_form(self):
        return (self.entry_nome.get().strip(),
                self.entry_nota1.get().strip(),
                self.entry_nota2.get().strip())

    def _validar(self, nome, n1, n2):
        if not nome or not n1 or not n2:
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.", parent=self)
            return None, None, None
        try:
            nota1 = float(n1.replace(",", "."))
            nota2 = float(n2.replace(",", "."))
        except ValueError:
            messagebox.showwarning("Atenção", "As notas devem ser valores numéricos.", parent=self)
            return None, None, None
        if not (0 <= nota1 <= 10 and 0 <= nota2 <= 10):
            messagebox.showwarning("Atenção", "As notas devem estar entre 0 e 10.", parent=self)
            return None, None, None
        return nome, nota1, nota2

    def _adicionar(self):
        nome, nota1, nota2 = self._validar(*self._obter_form())
        if nome is None:
            return
        try:
            self.controller.adicionar(Aluno(nome=nome, nota1=nota1, nota2=nota2))
            self._carregar_tabela()
            self._limpar()
            self._status(f"✔  Aluno '{nome}' adicionado com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro", str(e), parent=self)

    def _atualizar(self):
        if not self.aluno_selecionado:
            return
        nome, nota1, nota2 = self._validar(*self._obter_form())
        if nome is None:
            return
        try:
            self.controller.atualizar(self.aluno_selecionado,
                                      Aluno(nome=nome, nota1=nota1, nota2=nota2))
            self._carregar_tabela()
            self._limpar()
            self._status(f"✔  Dados de '{nome}' atualizados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e), parent=self)

    def _excluir(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um aluno para excluir.", parent=self)
            return
        nome = str(self.tree.item(sel[0])["values"][0])
        if messagebox.askyesno("Confirmar", f"Excluir o aluno '{nome}'?", parent=self):
            self.controller.remover(nome)
            self._limpar()
            self._status(f"✔  Aluno '{nome}' removido com sucesso!")

    def _buscar(self):
        texto  = self.entry_busca.get().strip()
        filtro = self.filtro_var.get()
        dados  = self.controller.buscar_por_nome(texto) if texto else self.controller.listar_todos()
        if filtro != "Todos":
            dados = [d for d in dados if d.get("Situação") == filtro]
        self._carregar_tabela(dados)

    def _aplicar_filtro(self, situacao: str):
        self.filtro_var.set(situacao)
        self._atualizar_botoes_filtro(situacao)
        self._buscar()

    def _atualizar_botoes_filtro(self, ativo: str):
        for label, (btn, cor_ativa, cor_inativa, fg_inativa) in self.btns_filtro.items():
            if label == ativo:
                btn.config(bg=cor_ativa, fg="white")
            else:
                btn.config(bg=cor_inativa, fg=fg_inativa)

    def _logout(self):
        if messagebox.askyesno("Sair", "Deseja sair do sistema?", parent=self):
            self.destroy()
            from views.login_view import LoginView
            LoginView().mainloop()
