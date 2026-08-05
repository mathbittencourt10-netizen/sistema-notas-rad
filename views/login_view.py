import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import AuthController


class LoginView(tk.Tk):
    """Tela de login com tema escuro."""

    def __init__(self):
        super().__init__()
        self.auth = AuthController()
        self._configurar()
        self._criar_interface()

    def _configurar(self):
        self.title("Sistema de Notas — Login")
        self.resizable(False, False)
        self.configure(bg="#0B2545")
        self.update_idletasks()
        w, h = 380, 360
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _criar_interface(self):
        # Header
        tk.Label(self, text="📚", font=("Arial", 30),
                 bg="#0B2545", fg="#1D9E75").pack(pady=(30, 2))
        tk.Label(self, text="Sistema de Notas",
                 font=("Arial", 17, "bold"), fg="#DFF0E8", bg="#0B2545").pack()
        tk.Label(self, text="RAD com Python & Pandas",
                 font=("Arial", 9), fg="#5A8A9E", bg="#0B2545").pack(pady=(2, 22))

        # Card
        card = tk.Frame(self, bg="#0F2A45", padx=28, pady=24)
        card.pack(padx=28, fill="x")

        tk.Label(card, text="Usuário", font=("Arial", 9),
                 fg="#7AAABB", bg="#0F2A45").pack(anchor="w")
        self.entry_usuario = tk.Entry(card, font=("Arial", 11),
                                      bg="#1A3A55", fg="white",
                                      insertbackground="white",
                                      relief="flat", bd=5)
        self.entry_usuario.pack(fill="x", pady=(2, 12), ipady=5)

        tk.Label(card, text="Senha", font=("Arial", 9),
                 fg="#7AAABB", bg="#0F2A45").pack(anchor="w")
        self.entry_senha = tk.Entry(card, font=("Arial", 11), show="●",
                                    bg="#1A3A55", fg="white",
                                    insertbackground="white",
                                    relief="flat", bd=5)
        self.entry_senha.pack(fill="x", pady=(2, 22), ipady=5)
        self.entry_senha.bind("<Return>", lambda e: self._login())

        tk.Button(card, text="Entrar  →",
                  font=("Arial", 11, "bold"),
                  bg="#1D9E75", fg="white", relief="flat",
                  cursor="hand2", pady=9,
                  activebackground="#17856A", activeforeground="white",
                  command=self._login).pack(fill="x")

        self.entry_usuario.focus()

    def _login(self):
        usuario = self.entry_usuario.get().strip()
        senha   = self.entry_senha.get().strip()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos.", parent=self)
            return

        resultado = self.auth.autenticar(usuario, senha)

        if resultado:
            self.destroy()
            if resultado["tipo"] == "professor":
                from views.professor_view import ProfessorView
                ProfessorView(resultado).mainloop()
            else:
                from views.aluno_view import AlunoView
                AlunoView(resultado).mainloop()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.", parent=self)
            self.entry_senha.delete(0, "end")
            self.entry_senha.focus()
