import tkinter as tk

tamanho_atual = 10
tamanho_minimo = 8
tamanho_maximo = 18


def _aplicar_em_todos(widget, tamanho):
    try:
        fonte_atual = widget.cget("font")
        if fonte_atual:
            if isinstance(fonte_atual, str):
                widget.configure(font=(fonte_atual, tamanho))
            elif isinstance(fonte_atual, tuple):
                familia = fonte_atual[0]
                estilo = fonte_atual[2] if len(fonte_atual) > 2 else ""
                if estilo:
                    widget.configure(font=(familia, tamanho, estilo))
                else:
                    widget.configure(font=(familia, tamanho))
    except Exception:
        pass

    for filho in widget.winfo_children():
        _aplicar_em_todos(filho, tamanho)


def aumentar(janela_raiz):
    global tamanho_atual
    if tamanho_atual < tamanho_maximo:
        tamanho_atual += 2
        _aplicar_em_todos(janela_raiz, tamanho_atual)


def diminuir(janela_raiz):
    global tamanho_atual
    if tamanho_atual > tamanho_minimo:
        tamanho_atual -= 2
        _aplicar_em_todos(janela_raiz, tamanho_atual)


def resetar(janela_raiz):
    global tamanho_atual
    tamanho_atual = 10
    _aplicar_em_todos(janela_raiz, tamanho_atual)
