import tkinter as tk
from tkinter import ttk, messagebox
from config import FONTE, BRANCO, CINZA_CLARO, CINZA_ESCURO, PRETO, VERMELHO, VERDE
from database import listar_produtos, cadastrar, atualizar, excluir

class TelaProdutos(tk.Frame):
    def __init__(self, pai, app):
        super().__init__(pai, bg=CINZA_CLARO)
        self.app = app
        self._id_selecionado = None
        self._build()

    def _build(self):
        # barra do topo
        barra = tk.Frame(self, bg=CINZA_ESCURO, height=46)
        barra.pack(fill="x")
        barra.pack_propagate(False)

        tk.Label(barra, text="Produtos", bg=CINZA_ESCURO, fg=BRANCO,
                 font=(FONTE, 13, "bold")).pack(side="left", padx=14)

        tk.Button(barra, text="Voltar", command=lambda: self.app.mostrar_tela("TelaPrincipal"),
                  bg=CINZA_ESCURO, fg=BRANCO, font=(FONTE, 9), bd=0,
                  cursor="hand2").pack(side="right", pady=8, padx=10)

        corpo = tk.Frame(self, bg=CINZA_CLARO)
        corpo.pack(fill="both", expand=True, padx=10, pady=8)

        # formulario
        form = tk.Frame(corpo, bg=BRANCO, bd=1, relief="solid", padx=16, pady=14)
        form.pack(fill="x", pady=(0, 10))

        tk.Label(form, text="Cadastrar / Editar produto", bg=BRANCO, fg=PRETO,
                 font=(FONTE, 11, "bold")).pack(anchor="w", pady=(0, 10))

        campos = [("Codigo de barras", "ent_cod"), ("Nome", "ent_nome"),
                  ("Preco (R$)", "ent_preco"), ("Estoque", "ent_est")]
        self._ents = {}
        for label, key in campos:
            tk.Label(form, text=label, bg=BRANCO, fg=CINZA_ESCURO,
                     font=(FONTE, 9)).pack(anchor="w")
            e = tk.Entry(form, font=(FONTE, 11), bd=1, relief="solid")
            e.pack(fill="x", ipady=4, pady=(2, 6))
            self._ents[key] = e

        # botoes salvar / novo / excluir
        bf = tk.Frame(form, bg=BRANCO)
        bf.pack(fill="x", pady=(4, 0))

        tk.Button(bf, text="Salvar", command=self._salvar,
                  bg=CINZA_ESCURO, fg=BRANCO, font=(FONTE, 10), bd=0,
                  cursor="hand2").pack(side="left", ipady=5, ipadx=14, padx=(0, 6))

        tk.Button(bf, text="Novo", command=self._limpar,
                  bg=CINZA_ESCURO, fg=BRANCO, font=(FONTE, 10), bd=0,
                  cursor="hand2").pack(side="left", ipady=5, ipadx=14, padx=(0, 6))

        tk.Button(bf, text="Excluir", command=self._excluir,
                  bg=VERMELHO, fg=BRANCO, font=(FONTE, 10), bd=0,
                  cursor="hand2").pack(side="left", ipady=5, ipadx=14)

        self.lbl_msg = tk.Label(form, text="", bg=BRANCO, fg=VERDE, font=(FONTE, 9))
        self.lbl_msg.pack(anchor="w", pady=(6, 0))

        # lista de produtos
        cols = ("Codigo", "Nome", "Preco", "Estoque")
        self.tree = ttk.Treeview(corpo, columns=cols, show="headings",
                                  height=12, selectmode="browse")
        for c, w in zip(cols, [150, 260, 80, 80]):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="center")
        self.tree.column("Nome", anchor="w")
        self.tree.pack(fill="x")
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar)

    def ao_abrir(self):
        self._carregar()
        self._limpar()

    def _carregar(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for p in listar_produtos():
            self.tree.insert("", "end", iid=str(p[0]),
                             values=(p[1], p[2], f"{p[3]:.2f}", p[4]))

    def _ao_selecionar(self, e=None):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        self._id_selecionado = int(sel[0])
        for e in self._ents.values():
            e.configure(state="normal")
            e.delete(0, "end")
        self._ents["ent_cod"].insert(0, vals[0])
        self._ents["ent_cod"].configure(state="disabled")
        self._ents["ent_nome"].insert(0, vals[1])
        self._ents["ent_preco"].insert(0, vals[2])
        self._ents["ent_est"].insert(0, vals[3])
        self.lbl_msg.configure(text="")

    def _limpar(self):
        self._id_selecionado = None
        for e in self._ents.values():
            e.configure(state="normal")
            e.delete(0, "end")
        self.lbl_msg.configure(text="")

    def _salvar(self):
        cod  = self._ents["ent_cod"].get().strip()
        nome = self._ents["ent_nome"].get().strip()
        preco = self._ents["ent_preco"].get().strip().replace(",", ".")
        est  = self._ents["ent_est"].get().strip()

        if not all([cod, nome, preco, est]):
            self.lbl_msg.configure(text="Preencha todos os campos.", fg=VERMELHO)
            return
        try:
            pf = float(preco)
            ei = int(est)
            if pf <= 0 or ei < 0:
                raise ValueError
        except ValueError:
            self.lbl_msg.configure(text="Preco ou estoque invalido.", fg=VERMELHO)
            return

        if self._id_selecionado:
            ok, msg = atualizar(self._id_selecionado, nome, pf, ei)
        else:
            ok, msg = cadastrar(cod, nome, pf, ei)

        self.lbl_msg.configure(text=msg, fg=VERDE if ok else VERMELHO)
        if ok:
            self._limpar()
            self._carregar()

    def _excluir(self):
        if not self._id_selecionado:
            messagebox.showinfo("Aviso", "Selecione um produto na lista.")
            return
        if messagebox.askyesno("Excluir", "Confirmar exclusao?"):
            ok, msg = excluir(self._id_selecionado)
            self.lbl_msg.configure(text=msg, fg=VERDE if ok else VERMELHO)
            if ok:
                self._limpar()
                self._carregar()