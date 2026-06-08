
    # ── Remover item selecionado ─────────────
    def _remover_item(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Aviso", "Selecione um item para remover.")
            return
        idx = self.tree.index(sel[0])
        del self.app.carrinho[idx]
        self._atualizar_carrinho()

    def _limpar_carrinho(self):
        if not self.app.carrinho:
            return
        if messagebox.askyesno("Limpar", "Deseja remover todos os itens?"):
            self.app.carrinho.clear()
            self._atualizar_carrinho()
            self.lbl_troco.configure(text="R$ 0,00")
            self.ent_pago.delete(0, "end")

    # ── Nota rápida ─────────────────────────
    def _nota_rapida(self, valor):
        self.ent_pago.delete(0, "end")
        self.ent_pago.insert(0, str(valor))

    # ── Calcular troco ───────────────────────
    def _calcular_troco(self):
        if not self.app.carrinho:
            messagebox.showwarning("Aviso", "Carrinho vazio.")
            return

        total = sum(i["preco"] * i["qtd"] for i in self.app.carrinho)

        pago_txt = self.ent_pago.get().strip().replace(",", ".")
        try:
            pago = float(pago_txt)
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor de pagamento válido.")
            return

        if pago < total:
            falta = total - pago
            self.lbl_status.configure(
                text=f"⚠ Valor insuficiente!\nFaltam R$ {falta:.2f}",
                fg=COR_VERMELHO)
            self.lbl_troco.configure(text="R$ 0,00")
            return

        troco = pago - total
        self.lbl_troco.configure(
            text=f"R$ {troco:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        self.lbl_status.configure(
            text=f"✔ Total: R$ {total:.2f}  |  Pago: R$ {pago:.2f}",
            fg=COR_VERDE)

    # ── Finalizar venda ──────────────────────
    def _finalizar_venda(self):
        if not self.app.carrinho:
            messagebox.showwarning("Aviso", "Carrinho vazio.")
            return

        total = sum(i["preco"] * i["qtd"] for i in self.app.carrinho)

        pago_txt = self.ent_pago.get().strip().replace(",", ".")
        try:
            pago = float(pago_txt)
        except ValueError:
            messagebox.showerror("Erro", "Informe o valor pago antes de finalizar.")
            return

        if pago < total:
            messagebox.showerror("Pagamento insuficiente",
                                 f"O valor pago (R$ {pago:.2f}) é menor que o total (R$ {total:.2f}).")
            return

        troco = pago - total

        # Cupom
        itens_txt = "\n".join(
            f"{i['nome']} x{i['qtd']} = R$ {i['preco']*i['qtd']:.2f}"
            for i in self.app.carrinho
        )

        cupom = (
            "=" * 40 + "\n"
            "       MERCADO DO POVO\n"
            f"  {datetime.now().strftime('%d/%m/%Y  %H:%M:%S')}\n"
            "=" * 40 + "\n"
            + itens_txt + "\n"
            "–" * 40 + "\n"
            f"  TOTAL:   R$ {total:>10.2f}\n"
            f"  PAGO:    R$ {pago:>10.2f}\n"
            f"  TROCO:   R$ {troco:>10.2f}\n"
            "=" * 40 + "\n"
            "   Obrigado pela preferência!\n"
            "=" * 40
        )
