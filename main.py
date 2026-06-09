import tkinter as tk
from tkinter import messagebox
from config import CINZA_CLARO, USUARIO, SENHA
from database import inicializar
from views.login import TelaLogin
from views.principal import TelaPrincipal
from views.produtos import TelaProdutos

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mercado do Povo - FG")
        self.geometry("1050x680")
        self.configure(bg=CINZA_CLARO)
        self.carrinho = []
        self.usuario_logado = None

        container = tk.Frame(self, bg=CINZA_CLARO)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.telas = {}
        for Tela in (TelaLogin, TelaPrincipal, TelaProdutos):
            nome = Tela.__name__
            t = Tela(container, self)
            self.telas[nome] = t
            t.grid(row=0, column=0, sticky="nsew")

        self.mostrar_tela("TelaLogin")

    def mostrar_tela(self, nome):
        t = self.telas[nome]
        t.tkraise()
        if hasattr(t, "ao_abrir"):
            t.ao_abrir()

    def fazer_login(self, usuario, senha):
        if usuario == USUARIO and senha == SENHA:
            self.usuario_logado = usuario
            self.mostrar_tela("TelaPrincipal")
        else:
            messagebox.showerror("Erro", "Usuario ou senha incorretos.")

    def fazer_logout(self):
        if messagebox.askyesno("Sair", "Deseja sair?"):
            self.carrinho.clear()
            self.usuario_logado = None
            self.mostrar_tela("TelaLogin")

if __name__ == "__main__":
    inicializar()
    app = App()
    app.mainloop()