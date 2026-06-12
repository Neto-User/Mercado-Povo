import tkinter as tk
from acessibilidade import fonte, contraste, voz
from config import FONTE, BRANCO, CINZA_CLARO, CINZA, CINZA_ESCURO, PRETO, VERMELHO, VERDE


class PainelAcessibilidade(tk.Toplevel):
    def __init__(self, pai, janela_raiz):
        super().__init__(pai)
        self.janela_raiz = janela_raiz
        self.title("Acessibilidade")
        self.resizable(False, False)
        self.configure(bg=CINZA_CLARO)
        self.grab_set()
        self._build()

    def _build(self):
        frame = tk.Frame(self, bg=CINZA_CLARO, padx=24, pady=20)
        frame.pack()

        tk.Label(frame, text="Acessibilidade", bg=CINZA_CLARO, fg=PRETO,
                 font=(FONTE, 13, "bold")).pack(anchor="w", pady=(0, 16))

        # --- Fonte ---
        tk.Label(frame, text="Tamanho da fonte", bg=CINZA_CLARO, fg=CINZA_ESCURO,
                 font=(FONTE, 10)).pack(anchor="w")

        fonte_row = tk.Frame(frame, bg=CINZA_CLARO)
        fonte_row.pack(fill="x", pady=(4, 14))

        tk.Button(fonte_row, text="A-", command=lambda: fonte.diminuir(self.janela_raiz),
                  bg=CINZA_ESCURO, fg=BRANCO, font=(FONTE, 12), bd=0,
                  cursor="hand2", width=4, activebackground=PRETO,
                  activeforeground=BRANCO).pack(side="left", ipady=4, padx=(0, 6))

        tk.Button(fonte_row, text="A+", command=lambda: fonte.aumentar(self.janela_raiz),
                  bg=CINZA_ESCURO, fg=BRANCO, font=(FONTE, 12), bd=0,
                  cursor="hand2", width=4, activebackground=PRETO,
                  activeforeground=BRANCO).pack(side="left", ipady=4, padx=(0, 6))

        tk.Button(fonte_row, text="Resetar", command=lambda: fonte.resetar(self.janela_raiz),
                  bg=CINZA, fg=PRETO, font=(FONTE, 10), bd=0,
                  cursor="hand2", activebackground=CINZA_ESCURO,
                  activeforeground=BRANCO).pack(side="left", ipady=4, ipadx=6)

        sep = lambda: tk.Frame(frame, bg=CINZA, height=1).pack(fill="x", pady=8)

        sep()

        # --- Contraste ---
        tk.Label(frame, text="Alto contraste", bg=CINZA_CLARO, fg=CINZA_ESCURO,
                 font=(FONTE, 10)).pack(anchor="w")
        tk.Label(frame, text="Troca para fundo preto com texto amarelo.",
                 bg=CINZA_CLARO, fg=CINZA, font=(FONTE, 8)).pack(anchor="w", pady=(0, 6))

        self.lbl_contraste = tk.Label(frame, text="Desativado", bg=CINZA_CLARO,
                                       fg=CINZA_ESCURO, font=(FONTE, 9))
        self.lbl_contraste.pack(anchor="w")

        tk.Button(frame, text="Alternar contraste",
                  command=self._alternar_contraste,
                  bg=CINZA_ESCURO, fg=BRANCO, font=(FONTE, 10), bd=0,
                  cursor="hand2", activebackground=PRETO,
                  activeforeground=BRANCO).pack(fill="x", ipady=6, pady=(4, 0))

        sep()

        # --- Voz ---
        tk.Label(frame, text="Leitura em voz alta", bg=CINZA_CLARO, fg=CINZA_ESCURO,
                 font=(FONTE, 10)).pack(anchor="w")
        tk.Label(frame, text="Fala o texto dos botoes ao passar o mouse.\nRequer: pip install pyttsx3",
                 bg=CINZA_CLARO, fg=CINZA, font=(FONTE, 8), justify="left").pack(anchor="w", pady=(0, 6))

        self.lbl_voz = tk.Label(frame, text="Desativada", bg=CINZA_CLARO,
                                 fg=CINZA_ESCURO, font=(FONTE, 9))
        self.lbl_voz.pack(anchor="w")

        tk.Button(frame, text="Alternar voz",
                  command=self._alternar_voz,
                  bg=CINZA_ESCURO, fg=BRANCO, font=(FONTE, 10), bd=0,
                  cursor="hand2", activebackground=PRETO,
                  activeforeground=BRANCO).pack(fill="x", ipady=6, pady=(4, 0))

        sep()

        tk.Button(frame, text="Fechar", command=self.destroy,
                  bg=CINZA, fg=PRETO, font=(FONTE, 10), bd=0,
                  cursor="hand2", activebackground=CINZA_ESCURO,
                  activeforeground=BRANCO).pack(fill="x", ipady=5)

    def _alternar_contraste(self):
        ativo = contraste.alternar(self.janela_raiz)
        self.lbl_contraste.configure(
            text="Ativado" if ativo else "Desativado",
            fg=VERDE if ativo else CINZA_ESCURO
        )

    def _alternar_voz(self):
        ok, msg = voz.alternar(self.janela_raiz)
        if not ok:
            self.lbl_voz.configure(text=msg, fg=VERMELHO)
            return
        ativo = voz.voz_ativa
        self.lbl_voz.configure(
            text="Ativada" if ativo else "Desativada",
            fg=VERDE if ativo else CINZA_ESCURO
        )
