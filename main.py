import tkinter as tk
from tkinter import ttk, messagebox, font
import sqlite3
import os
from datetime import datetime

# ─────────────────────────────────────────────
#  CONFIGURAÇÕES GLOBAIS
# ─────────────────────────────────────────────
COR_AZUL        = "#1565C0"
COR_AZUL_ESCURO = "#0D47A1"
COR_AZUL_CLARO  = "#1E88E5"
COR_LARANJA     = "#F57C00"
COR_LARANJA_VIF = "#FF9800"
COR_BRANCO      = "#FFFFFF"
COR_FUNDO       = "#E3F2FD"
COR_CINZA       = "#ECEFF1"
COR_TEXTO       = "#212121"
COR_VERDE       = "#2E7D32"
COR_VERMELHO    = "#C62828"

DB_PATH = "mercado_do_povo.db"

USUARIO_FIXO = "admin"
SENHA_FIXA   = "1234"

# ─────────────────────────────────────────────
#  BANCO DE DADOS
# ─────────────────────────────────────────────
def inicializar_banco():
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo      TEXT    NOT NULL UNIQUE,
            nome        TEXT    NOT NULL,
            preco       REAL    NOT NULL,
            estoque     INTEGER NOT NULL DEFAULT 0,
            cadastrado  TEXT    NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora   TEXT    NOT NULL,
            total       REAL    NOT NULL,
            pago        REAL    NOT NULL,
            troco       REAL    NOT NULL,
            itens       TEXT    NOT NULL
        )
    """)

    # Produtos de exemplo
    exemplos = [
        ("7891000315507", "Leite Integral 1L",   4.99,  50),
        ("7891910000244", "Arroz 5kg",           22.90,  30),
        ("7896004004922", "Feijão Carioca 1kg",   8.75,  40),
        ("7896016102055", "Açúcar Cristal 1kg",   4.50,  60),
        ("7891080040475", "Café Torrado 500g",   14.99,  25),
        ("7894321722016", "Óleo de Soja 900ml",   7.80,  35),
        ("7891000100103", "Macarrão Espaguete",   3.99,  70),
        ("7896523304038", "Sal Refinado 1kg",     2.29,  80),
    ]
    for cod, nome, preco, estoque in exemplos:
        cur.execute("""
            INSERT OR IGNORE INTO produtos (codigo, nome, preco, estoque, cadastrado)
            VALUES (?, ?, ?, ?, ?)
        """, (cod, nome, preco, estoque, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()

def buscar_produto_por_codigo(codigo):
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    cur.execute("SELECT id, codigo, nome, preco, estoque FROM produtos WHERE codigo = ?", (codigo,))
    row = cur.fetchone()
    conn.close()
    return row

def buscar_todos_produtos():
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    cur.execute("SELECT id, codigo, nome, preco, estoque, cadastrado FROM produtos ORDER BY nome")
    rows = cur.fetchall()
    conn.close()
    return rows

def cadastrar_produto(codigo, nome, preco, estoque):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur  = conn.cursor()
        cur.execute("""
            INSERT INTO produtos (codigo, nome, preco, estoque, cadastrado)
            VALUES (?, ?, ?, ?, ?)
        """, (codigo, nome, preco, estoque, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        return True, "Produto cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Código de barras já cadastrado."
    except Exception as e:
        return False, f"Erro: {e}"

def atualizar_produto(produto_id, nome, preco, estoque):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur  = conn.cursor()
        cur.execute("""
            UPDATE produtos SET nome=?, preco=?, estoque=? WHERE id=?
        """, (nome, preco, estoque, produto_id))
        conn.commit()
        conn.close()
        return True, "Produto atualizado!"
    except Exception as e:
        return False, f"Erro: {e}"

def excluir_produto(produto_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur  = conn.cursor()
        cur.execute("DELETE FROM produtos WHERE id=?", (produto_id,))
        conn.commit()
        conn.close()
        return True, "Produto excluído!"
    except Exception as e:
        return False, f"Erro: {e}"

def registrar_venda(total, pago, troco, itens_texto):
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    cur.execute("""
        INSERT INTO vendas (data_hora, total, pago, troco, itens)
        VALUES (?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total, pago, troco, itens_texto))
    conn.commit()
    conn.close()