# Mercado Povo FG

Link do protótipo No Figma: [Mercado_povo_FG](https://www.figma.com/proto/e6AwozCcOKsREovYwLVqXs/Mercado-povo-fg?node-id=3-2&t=vixIcqTXLSHRKGl1-0&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=3%3A2)

Aplicação de gerenciamento de mercado desenvolvida em Python com interface gráfica utilizando Tkinter.

## Estrutura do Projeto

```
mercado_povo_FG/
│
├── views/                    # Módulos de visualização da aplicação
│   ├── login.py             # Módulo de autenticação de usuários
│   ├── principal.py         # Interface principal da aplicação
│   └── produtos.py          # Gerenciamento de produtos
│
├── config.py                 # Configurações do projeto
├── database.py               # Operações com banco de dados
├── main.py                   # Ponto de entrada da aplicação
├── mercado.db                # Banco de dados SQLite
└── README.md                 # Documentação do projeto
```

## Descrição dos Componentes

| Arquivo/Diretório | Descrição |
|---|---|
| views/ | Módulos que contêm as interfaces gráficas Tkinter da aplicação. |
| views/login.py | Implementa o sistema de autenticação e validação de usuários. |
| views/principal.py | Interface principal com o menu de navegação da aplicação. |
| views/produtos.py | Módulo responsável pela gestão do catálogo de produtos. |
| config.py | Arquivo de configuração centralizado da aplicação. |
| database.py | Módulo para operações e gerenciamento do banco de dados SQLite. |
| main.py | Arquivo executável que inicia a aplicação. |
| mercado.db | Arquivo de banco de dados SQLite. |

## Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/Neto-User/Mercado-Povo.git OU
git clone git@github.com:Neto-User/Mercado-Povo.git
cd Mercado-Povo
```

### 2. Crie um Ambiente Virtual

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

## Execução

### Windows

```bash
python main.py
```

### Linux

```bash
python3 main.py
```

### macOS

```bash
python3 main.py
```

## Dependências

O projeto utiliza as seguintes bibliotecas:

- tkinter - Interface gráfica (incluída no Python por padrão)
- sqlite3 - Gerenciamento de banco de dados (incluída no Python por padrão)

Caso precise de dependências adicionais, consulte o arquivo `requirements.txt`.

## Banco de Dados

A aplicação utiliza SQLite como sistema de gerenciamento de banco de dados. O arquivo `mercado.db` será criado automaticamente na primeira execução.

Para reinicializar o banco de dados, remova o arquivo `mercado.db` e execute a aplicação novamente.

## Resolução de Problemas

**Erro: ModuleNotFoundError**
- Verifique se o ambiente virtual está ativado
- Reinstale as dependências: `pip install -r requirements.txt`

**Erro: No module named 'tkinter'**
- No Linux, instale: `sudo apt-get install python3-tk`
- No macOS, o Tkinter geralmente está incluído

**Banco de dados corrompido**
- Delete o arquivo `mercado.db` e reinicie a aplicação

## Autores

Desenvolvido por Neto-User
