
        # Salvar no banco
        registrar_venda(total, pago, troco, itens_txt)

        messagebox.showinfo("Venda Finalizada! ✅", cupom)

        # Limpar
        self.app.carrinho.clear()
        self._atualizar_carrinho()
        self.ent_pago.delete(0, "end")
        self.lbl_troco.configure(text="R$ 0,00")
        self.lbl_status.configure(text="")


# ─────────────────────────────────────────────
#  TELA 3 – CADASTRO DE PRODUTOS
# ─────────────────────────────────────────────
class TelaProdutos(tk.Frame):
    def __init__(self, pai, app):
        super().__init__(pai, bg=COR_FUNDO)
        self.app = app
        self._produto_selecionado_id = None
        self._construir()

    def _construir(self):
        # Barra superior
        barra = tk.Frame(self, bg=COR_AZUL_ESCURO, height=52)
        barra.pack(fill="x")
        barra.pack_propagate(False)

        tk.Label(barra, text="📦  CADASTRO DE PRODUTOS",
                 bg=COR_AZUL_ESCURO, fg=COR_BRANCO,
                 font=("Helvetica", 15, "bold")).pack(side="left", padx=18)

        btn_voltar = tk.Button(barra, text="← Voltar ao Caixa",
                                command=lambda: self.app.mostrar_tela("TelaPrincipal"),
                                bg=COR_LARANJA, fg=COR_BRANCO,
                                font=("Helvetica", 10, "bold"),
                                bd=0, relief="flat", cursor="hand2",
                                activebackground=COR_LARANJA_VIF, padx=12)
        btn_voltar.pack(side="right", pady=8, padx=10)

        # Corpo
        corpo = tk.Frame(self, bg=COR_FUNDO)
        corpo.pack(fill="both", expand=True, padx=12, pady=10)
        corpo.grid_columnconfigure(0, weight=1)
        corpo.grid_columnconfigure(1, weight=2)
        corpo.grid_rowconfigure(0, weight=1)

        # ── Coluna esquerda: formulário ──────
        form = tk.LabelFrame(corpo, text=" ✏ Cadastrar / Editar Produto ",
                              bg=COR_BRANCO, fg=COR_AZUL_ESCURO,
                              font=("Helvetica", 11, "bold"),
                              bd=2, relief="groove")
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        campos = [
            ("Código de Barras*:", "ent_cod"),
            ("Nome do Produto*:",  "ent_nome"),
            ("Preço (R$)*:",       "ent_preco"),
            ("Estoque*:",          "ent_estoque"),
        ]
        self._entradas = {}
        for i, (label, nome) in enumerate(campos):
            tk.Label(form, text=label, bg=COR_BRANCO,
                     font=("Helvetica", 10, "bold")).grid(
                row=i*2, column=0, columnspan=2, sticky="w", padx=18, pady=(12, 0))
            ent = tk.Entry(form, font=("Helvetica", 12),
                           bd=2, relief="solid", width=26)
            ent.grid(row=i*2+1, column=0, columnspan=2,
                     sticky="ew", padx=18, ipady=5)
            self._entradas[nome] = ent

        # Dica leitor de código
        tk.Label(form, text="💡 Com leitor USB: posicione o cursor em 'Código'\n"
                            "    e leia o código de barras normalmente.",
                 bg=COR_BRANCO, fg="#607D8B",
                 font=("Helvetica", 9), justify="left").grid(
            row=8, column=0, columnspan=2, padx=18, pady=10, sticky="w")

        # Botões do formulário
        bf = tk.Frame(form, bg=COR_BRANCO)
        bf.grid(row=9, column=0, columnspan=2, pady=12, padx=18, sticky="ew")

        btn_salvar = tk.Button(bf, text="💾 Salvar",
                                command=self._salvar_produto,
                                bg=COR_AZUL_CLARO, fg=COR_BRANCO,
                                font=("Helvetica", 11, "bold"),
                                bd=0, relief="flat", cursor="hand2",
                                activebackground=COR_AZUL, padx=12)
        btn_salvar.pack(side="left", padx=4, ipady=6, expand=True, fill="x")

        btn_novo = tk.Button(bf, text="🆕 Novo",
                              command=self._limpar_form,
                              bg="#546E7A", fg=COR_BRANCO,
                              font=("Helvetica", 11, "bold"),
                              bd=0, relief="flat", cursor="hand2",
                              activebackground="#37474F", padx=12)
        btn_novo.pack(side="left", padx=4, ipady=6, expand=True, fill="x")

        btn_excl = tk.Button(bf, text="🗑 Excluir",
                              command=self._excluir_produto,
                              bg=COR_VERMELHO, fg=COR_BRANCO,
                              font=("Helvetica", 11, "bold"),
                              bd=0, relief="flat", cursor="hand2",
                              activebackground="#B71C1C", padx=12)
        btn_excl.pack(side="left", padx=4, ipady=6, expand=True, fill="x")

        self.lbl_form_status = tk.Label(form, text="",
                                         bg=COR_BRANCO, fg=COR_VERDE,
                                         font=("Helvetica", 10, "bold"),
                                         wraplength=260)
        self.lbl_form_status.grid(row=10, column=0, columnspan=2, pady=6)

        # ── Coluna direita: tabela de produtos ──
        lista_frame = tk.LabelFrame(corpo, text=" 📋 Produtos Cadastrados ",
                                     bg=COR_FUNDO, fg=COR_AZUL_ESCURO,
                                     font=("Helvetica", 11, "bold"),
                                     bd=2, relief="groove")
        lista_frame.grid(row=0, column=1, sticky="nsew")

        # Busca
        busca_row = tk.Frame(lista_frame, bg=COR_FUNDO)
        busca_row.pack(fill="x", padx=8, pady=8)
        tk.Label(busca_row, text="🔍 Filtrar:", bg=COR_FUNDO,
                 font=("Helvetica", 10)).pack(side="left", padx=4)
        self.ent_filtro = tk.Entry(busca_row, font=("Helvetica", 11),
                                    bd=2, relief="solid", width=28)
        self.ent_filtro.pack(side="left", padx=4, ipady=4)
        self.ent_filtro.bind("<KeyRelease>", lambda e: self._carregar_tabela())

        self.lbl_qtd_prod = tk.Label(busca_row, text="", bg=COR_FUNDO,
                                      fg=COR_AZUL_CLARO,
                                      font=("Helvetica", 10, "bold"))
        self.lbl_qtd_prod.pack(side="right", padx=8)

        # Treeview
        cols = ("Código", "Nome", "Preço R$", "Estoque", "Cadastrado")
        self.tree_prod = ttk.Treeview(lista_frame, columns=cols,
                                       show="headings", height=20,
                                       selectmode="browse")
        larg = [130, 220, 80, 70, 130]
        for c, l in zip(cols, larg):
            self.tree_prod.heading(c, text=c,
                                   command=lambda col=c: self._ordenar(col))
            self.tree_prod.column(c, width=l, anchor="center")
        self.tree_prod.column("Nome", anchor="w")

        sb2 = ttk.Scrollbar(lista_frame, orient="vertical",
                             command=self.tree_prod.yview)
        self.tree_prod.configure(yscrollcommand=sb2.set)
        self.tree_prod.pack(side="left", fill="both", expand=True)
        sb2.pack(side="right", fill="y")

        self.tree_prod.bind("<<TreeviewSelect>>", self._ao_selecionar)

    # ── Ao abrir ─────────────────────────────
    def ao_abrir(self):
        self._carregar_tabela()
        self._limpar_form()
