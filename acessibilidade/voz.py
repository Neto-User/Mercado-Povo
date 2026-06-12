import threading
import tkinter as tk

voz_ativa = False
_engine = None


def _carregar_engine():
    global _engine
    try:
        import pyttsx3
        _engine = pyttsx3.init()
        _engine.setProperty("rate", 160)
        voices = _engine.getProperty("voices")
        for v in voices:
            if "brazil" in v.id.lower() or "brazil" in v.name.lower():
                _engine.setProperty("voice", v.id)
                break
        return True
    except Exception:
        return False


def _falar(texto):
    if _engine is None:
        return
    try:
        _engine.say(texto)
        _engine.runAndWait()
    except Exception:
        pass


def falar_em_thread(texto):
    if not voz_ativa or not texto:
        return
    t = threading.Thread(target=_falar, args=(texto,), daemon=True)
    t.start()


def _pegar_texto(widget):
    try:
        return widget.cget("text")
    except Exception:
        return ""


def _vincular_widget(widget):
    texto = _pegar_texto(widget)
    if texto:
        widget.bind("<Enter>", lambda e, t=texto: falar_em_thread(t))

    for filho in widget.winfo_children():
        _vincular_widget(filho)


def alternar(janela_raiz):
    global voz_ativa
    if not voz_ativa and _engine is None:
        ok = _carregar_engine()
        if not ok:
            return False, "erro ao carregar voz (Por favor verifique se pyttsx3 está instalado)"

    voz_ativa = not voz_ativa

    if voz_ativa:
        _vincular_widget(janela_raiz)

    return True, "ativada" if voz_ativa else "desativada"