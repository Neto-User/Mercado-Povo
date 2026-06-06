# import libraries
import sqlite3
from config import DB_PATH

# import de data e hora
from datetime import datetime

# Função para criar inicializar o banco de dados e criar as tabelas necessárias kk
def inicializar():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo    TEXT NOT NULL UNIQUE,
            nome      TEXT NOT NULL,
            preco     REAL NOT NULL,
            estoque   INTEGER NOT NULL DEFAULT 0,
            criado_em TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL,
            total     REAL NOT NULL,
            pago      REAL NOT NULL,
            troco     REAL NOT NULL,
            itens     TEXT NOT NULL
        )
    """)

    #Adicionando Exemplo de Produto
    exemplos = [
        ("7891000315507", "Leite Integral 1L",  4.99, 50),
        ("7891910000244", "Arroz 5kg",          22.90, 30),
        ("7896004004922", "Feijao Carioca 1kg",  8.75, 40),
        ("7896016102055", "Acucar Cristal 1kg",  4.50, 60),
        ("7891080040475", "Cafe Torrado 500g",  14.99, 25),
        ("7894321722016", "Oleo de Soja 900ml",  7.80, 35),
        ("7891000100103", "Macarrao Espaguete",  3.99, 70),
        ("7896523304038", "Sal Refinado 1kg",    2.29, 80),
    ]
    for cod, nome, preco, estoque in exemplos:
        cur.execute(
            "INSERT OR IGNORE INTO produtos (codigo,nome,preco,estoque,criado_em) VALUES (?,?,?,?,?)",
            (cod, nome, preco, estoque, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

    con.commit()
    con.close()

# Função para Buscar Produtos
def buscar_por_codigo(codigo):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT id,codigo,nome,preco,estoque FROM produtos WHERE codigo=?", (codigo,))
    row = cur.fetchone()
    con.close()
    return row

# Função para Listar Produtos
def listar_produtos():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT id,codigo,nome,preco,estoque,criado_em FROM produtos ORDER BY nome")
    rows = cur.fetchall()
    con.close()
    return rows

# Função para Cadastrar Produto
def cadastrar(codigo, nome, preco, estoque):
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute(
            "INSERT INTO produtos (codigo,nome,preco,estoque,criado_em) VALUES (?,?,?,?,?)",
            (codigo, nome, preco, estoque, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        con.commit()
        con.close()
        return True, "Cadastrado com sucesso."
    except sqlite3.IntegrityError:
        return False, "Codigo ja cadastrado."
    except Exception as e:
        return False, str(e)
    
# Função para Atualizar Produto
def atualizar(pid, nome, preco, estoque):
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("UPDATE produtos SET nome=?,preco=?,estoque=? WHERE id=?",
                    (nome, preco, estoque, pid))
        con.commit()
        con.close()
        return True, "Atualizado."
    except Exception as e:
        return False, str(e)
    
    # Função para Deletar Produto
def excluir(pid):
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("DELETE FROM produtos WHERE id=?", (pid,))
        con.commit()
        con.close()
        return True, "Excluido."
    except Exception as e:
        return False, str(e)

# Função para Registrar Venda
def salvar_venda(total, pago, troco, itens_txt):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO vendas (data_hora,total,pago,troco,itens) VALUES (?,?,?,?,?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total, pago, troco, itens_txt)
    )
    con.commit()
    con.close()
