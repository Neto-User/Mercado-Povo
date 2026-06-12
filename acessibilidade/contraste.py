import tkinter as tk

alto_contraste_ativo = False

TEMA_NORMAL = {
    "fundo":  "#f0f0f0",
    "widget": "#ffffff",
    "texto":  "#1a1a1a",
    "botao":  "#505050",
    "botao_texto": "#ffffff",
}

TEMA_CONTRASTE = {
    "fundo":  "#000000",
    "widget": "#1a1a1a",
    "texto":  "#ffff00",
    "botao":  "#ffff00",
    "botao_texto": "#000000",
}


def _aplicar_em_todos(widget, tema):
    tipo = widget.winfo_class()

    try:
        if tipo in ("Frame", "Labelframe", "Label", "Toplevel"):
            widget.configure(bg=tema["fundo"], fg=tema["texto"])
        elif tipo == "Button":
            widget.configure(bg=tema["botao"], fg=tema["botao_texto"],
                             activebackground=tema["texto"],
                             activeforeground=tema["fundo"])
        elif tipo == "Entry":
            widget.configure(bg=tema["widget"], fg=tema["texto"],
                             insertbackground=tema["texto"])
        elif tipo == "Listbox":
            widget.configure(bg=tema["widget"], fg=tema["texto"])
    except Exception:
        pass

    for filho in widget.winfo_children():
        _aplicar_em_todos(filho, tema)


def alternar(janela_raiz):
    global alto_contraste_ativo
    alto_contraste_ativo = not alto_contraste_ativo
    tema = TEMA_CONTRASTE if alto_contraste_ativo else TEMA_NORMAL
    janela_raiz.configure(bg=tema["fundo"])
    _aplicar_em_todos(janela_raiz, tema)
    return alto_contraste_ativo
