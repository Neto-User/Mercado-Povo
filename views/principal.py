import tkinter as tk
from tkinter import ttk, messagebox
from config import FONTE, BRANCO, CINZA_CLARO, CINZA_ESCURO, PRETO, VERMELHO
from acessibilidade.painel import PainelAcessibilidade
from database import buscar_por_codigo, salvar_venda

class TelaPrincipal(tk.Frame):
    def __init__(self, pai, app):
        super().__init__(pai, bg=CINZA_CLARO)
        self.app = app
        self._build()
        

    def _build(self):
        # barra do topo
        barra = tk.Frame(self, bg=CINZA_ESCURO, height=46)
        barra.pack(fill="x")
        barra.pack_propagate(False)

        tk.Label(barra, text="Mercado_Povo_FG - Caixa", bg=CINZA_ESCURO, fg=BRANCO,
                 font=(FONTE, 13, "bold")).pack(side="left", padx=14)

        tk.Button(barra, text="Sair", command=self.app.fazer_logout,
                  bg=VERMELHO, fg=BRANCO, font=(FONTE, 9), bd=0,
                  cursor="hand2").pack(side="right", pady=8, padx=4)

        tk.Button(barra, text="Produtos", command=lambda: self.app.mostrar_tela("TelaProdutos"),
                  bg=CINZA_ESCURO, fg=BRANCO, font=(FONTE, 9), bd=0,
                  cursor="hand2").pack(side="right", pady=8, padx=4)
        
        tk.Button(barra, text="Acessibilidade",
          command=lambda: PainelAcessibilidade(self, self.winfo_toplevel()),
          bg=CINZA_ESCURO, fg=BRANCO, font=(FONTE, 9), bd=0,
          cursor="hand2").pack(side="right", pady=8, padx=4)

        # campo de codigo e quantidade
        corpo = tk.Frame(self, bg=CINZA_CLARO)
        corpo.pack(fill="both", expand=True, padx=10, pady=8)

        tk.Label(corpo, text="Codigo do produto:", bg=CINZA_CLARO, fg=PRETO,
                 font=(FONTE, 10)).pack(anchor="w")
        self.ent_codigo = tk.Entry(corpo, font=(FONTE, 12), bd=1, relief="solid", width=24)
        self.ent_codigo.pack(anchor="w", ipady=4, pady=(2, 6))
        self.ent_codigo.bind("<Return>", lambda e: self._adicionar())

        tk.Label(corpo, text="Quantidade:", bg=CINZA_CLARO, fg=PRETO,
                 font=(FONTE, 10)).pack(anchor="w")
        self.ent_qtd = tk.Entry(corpo, font=(FONTE, 12), bd=1, relief="solid", width=8)
        self.ent_qtd.insert(0, "1")
        self.ent_qtd.pack(anchor="w", ipady=4, pady=(2, 6))

        tk.Button(corpo, text="Adicionar", command=self._adicionar,
                  bg=CINZA_ESCURO, fg=BRANCO, font=(FONTE, 10), bd=0,
                  cursor="hand2").pack(anchor="w", ipady=4, ipadx=10, pady=(0, 10))

        # lista de itens no carrinho
        cols = ("Produto", "Qtd", "Preco Unit.", "Subtotal")
        self.tree = ttk.Treeview(corpo, columns=cols, show="headings", height=10)
        for c, w in zip(cols, [260, 60, 100, 100]):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="center")
        self.tree.column("Produto", anchor="w")
        self.tree.pack(fill="x", pady=(0, 6))

        tk.Button(corpo, text="Remover item selecionado", command=self._remover,
                  bg=VERMELHO, fg=BRANCO, font=(FONTE, 9), bd=0,
                  cursor="hand2").pack(anchor="w", ipady=4, ipadx=6, pady=(0, 10))

        # total e pagamento
        self.lbl_total = tk.Label(corpo, text="Total: R$ 0,00", bg=CINZA_CLARO, fg=PRETO,
                                   font=(FONTE, 13, "bold"))
        self.lbl_total.pack(anchor="w", pady=(0, 6))

        tk.Label(corpo, text="Valor pago (R$):", bg=CINZA_CLARO, fg=PRETO,
                 font=(FONTE, 10)).pack(anchor="w")
        self.ent_pago = tk.Entry(corpo, font=(FONTE, 12), bd=1, relief="solid", width=14)
        self.ent_pago.pack(anchor="w", ipady=4, pady=(2, 6))

        self.lbl_troco = tk.Label(corpo, text="Troco: R$ 0,00", bg=CINZA_CLARO, fg=PRETO,
                                   font=(FONTE, 11))
        self.lbl_troco.pack(anchor="w", pady=(0, 8))

        tk.Button(corpo, text="Finalizar venda", command=self._finalizar,
                  bg=PRETO, fg=BRANCO, font=(FONTE, 11, "bold"), bd=0,
                  cursor="hand2").pack(anchor="w", ipady=6, ipadx=16)

    def ao_abrir(self):
        self.ent_codigo.focus()

    def _adicionar(self):
        codigo = self.ent_codigo.get().strip()
        if not codigo:
            return
        try:
            qtd = int(self.ent_qtd.get().strip())
            if qtd < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Quantidade invalida.")
            return

        p = buscar_por_codigo(codigo)
        if not p:
            messagebox.showerror("Nao encontrado", f"Codigo '{codigo}' nao cadastrado.")
            return

        _, cod, nome, preco, _ = p
        # se ja existe no carrinho, soma a quantidade
        for item in self.app.carrinho:
            if item["codigo"] == cod:
                item["qtd"] += qtd
                break
        else:
            self.app.carrinho.append({"codigo": cod, "nome": nome, "preco": preco, "qtd": qtd})

        self.ent_codigo.delete(0, "end")
        self.ent_qtd.delete(0, "end")
        self.ent_qtd.insert(0, "1")
        self._atualizar_tree()

    def _atualizar_tree(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        total = 0.0
        for item in self.app.carrinho:
            sub = item["preco"] * item["qtd"]
            total += sub
            self.tree.insert("", "end", values=(
                item["nome"], item["qtd"],
                f"{item['preco']:.2f}", f"{sub:.2f}"
            ))
        self.lbl_total.configure(text=f"Total: R$ {total:.2f}")

    def _remover(self):
        sel = self.tree.selection()
        if not sel:
            return
        del self.app.carrinho[self.tree.index(sel[0])]
        self._atualizar_tree()

    def _finalizar(self):
        if not self.app.carrinho:
            messagebox.showwarning("Aviso", "Carrinho vazio.")
            return
        total = sum(i["preco"] * i["qtd"] for i in self.app.carrinho)
        try:
            pago = float(self.ent_pago.get().strip().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Informe o valor pago.")
            return
        if pago < total:
            messagebox.showerror("Pagamento insuficiente",
                                 f"Pago R$ {pago:.2f} | Total R$ {total:.2f}")
            return

        troco = pago - total
        self.lbl_troco.configure(text=f"Troco: R$ {troco:.2f}")

        itens_txt = "\n".join(
            f"{i['nome']} x{i['qtd']} = R$ {i['preco'] * i['qtd']:.2f}"
            for i in self.app.carrinho
        )
        salvar_venda(total, pago, troco, itens_txt)
        messagebox.showinfo("Venda finalizada", f"Troco: R$ {troco:.2f}")

        self.app.carrinho.clear()
        self._atualizar_tree()
        self.ent_pago.delete(0, "end")
        self.lbl_troco.configure(text="Troco: R$ 0,00")