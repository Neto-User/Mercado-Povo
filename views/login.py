# importar bibliotecas
import tkinter as tk
from config import CINZA_CLARO, BRANCO, CINZA, PRETO, CINZA_ESCURO, FONTE

# criar classe de Telalogin
class TelaLogin(tk.Frame):
    def __init__(self, pai, app):
        super().__init__(pai, bg=CINZA_CLARO)
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="Mercado do Povo", bg=CINZA_CLARO, fg=PRETO,
                 font=(FONTE, 20, "bold")).pack(pady=(60, 4))
        tk.Label(self, text="Sistema de Caixa", bg=CINZA_CLARO, fg=CINZA_ESCURO,
                 font=(FONTE, 11)).pack(pady=(0, 30))

        card = tk.Frame(self, bg=BRANCO, bd=1, relief="solid", padx=40, pady=30)
        card.pack()

        tk.Label(card, text="Usuario", bg=BRANCO, fg=CINZA_ESCURO,
                 font=(FONTE, 10)).pack(anchor="w")
        self.ent_user = tk.Entry(card, font=(FONTE, 11), bd=1, relief="solid", width=26)
        self.ent_user.pack(pady=(2, 10), ipady=4)
        

        tk.Label(card, text="Senha", bg=BRANCO, fg=CINZA_ESCURO,
                 font=(FONTE, 10)).pack(anchor="w")
        self.ent_pass = tk.Entry(card, font=(FONTE, 11), bd=1, relief="solid",
                                  width=26, show="*")
        self.ent_pass.pack(pady=(2, 18), ipady=4)
        

        tk.Button(card, text="Entrar", command=self._login,
                  bg=CINZA_ESCURO, fg=BRANCO, font=(FONTE, 11),
                  bd=0, cursor="hand2", activebackground=PRETO,
                  activeforeground=BRANCO).pack(fill="x", ipady=6)


        self.ent_pass.bind("<Return>", lambda e: self._login())
        self.ent_user.bind("<Return>", lambda e: self.ent_pass.focus())

    def _login(self):
        self.app.fazer_login(self.ent_user.get().strip(), self.ent_pass.get().strip())