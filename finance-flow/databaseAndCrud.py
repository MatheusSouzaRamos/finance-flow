import pandas as pd
import sqlite3

# ==================== DATABASE ====================
def obterConexao():
    return sqlite3.connect('database.db')

def montarBanco():
    try:
        conexao = obterConexao()
        cursor = conexao.cursor()
        conexao.execute("PRAGMA foreign_keys = ON")

        cursor.execute('''CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT               
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS pagamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT               
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS movimentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT,
        valor REAL,
        categoria_id INTEGER,       
        pagamento_id INTEGER,
        status TEXT,
        data TEXT,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id),
        FOREIGN KEY (pagamento_id) REFERENCES pagamentos(id)
        )''')
        conexao.commit()
    except Exception as erro:
        #st.error(f'Erro: {erro}')
        return None
    finally:
        conexao.close()

# ==================== CRUD ====================
# ----------- CATEGGORIA -----------
def selectCategorias():
    try:
        conexao = obterConexao()
        consulta = pd.read_sql('SELECT * FROM categorias', conexao)
        return consulta
    except Exception as erro:
        return None
    finally:
        conexao.close()

def insertCategorias(nome):
    try:
        conexao = obterConexao()
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO categorias (nome) VALUES (?)', (nome,))
        conexao.commit()
    except:
        conexao.rollback()
    finally:
        conexao.close()

def updateCategorias(id, nome):
    try:
        conexao = obterConexao()
        cursor = conexao.cursor()
        cursor.execute('UPDATE categorias set nome = ? WHERE id = ?', (nome, id))
        conexao.commit()
    except:
        conexao.rollback()
    finally:
        conexao.close()

def deleteCategorias(id):
    try:
        conexao = obterConexao()
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM categorias WHERE id = ?', (id,))
        conexao.commit()
    except:
        conexao.rollback()
    finally:
        conexao.close()

# ----------- PAGAMENTO -----------
def selectPagamentos():
    try:
        conexao = obterConexao()
        consulta = pd.read_sql('SELECT * FROM pagamentos', conexao)
        return consulta
    except:
        return None
    finally:
        conexao.close()

def insertPagamentos(nome):
    try:
        conexao = obterConexao()
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO pagamentos (nome) VALUES (?)', (nome,))
        conexao.commit()
    except:
        conexao.rollback()
    finally:
        conexao.close()

def updatePagamentos(id, nome):
    try:
        conexao = obterConexao()
        cursor = conexao.cursor()
        cursor.execute('UPDATE pagamentos SET nome = ? WHERE id = ?', (nome, id))
        conexao.commit()
    except:
        conexao.rollback()
    finally:
        conexao.close()

def deletePagamentos(id):
    try:
        conexao = obterConexao()
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM pagamentos WHERE id = ?', (id,))
        conexao.commit()
    except:
        conexao.rollback()
    finally:
        conexao.close()

# ----------- MOVIMENTO -----------
def selectMovimentos():
    try:
        conexao = obterConexao()
        consulta = pd.read_sql('SELECT * FROM movimentos', conexao)
        return consulta
    except:
        return None
    finally:
        conexao.close()

def insertMovimentos(descricao, valor, categoria_id, pagamento_id, status, data):
    try:
        conexao = obterConexao()
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO movimentos (descricao, valor, categoria_id, pagamento_id, status, data) VALUES (?,?,?,?,?,?)', (descricao, valor, categoria_id, pagamento_id, status, data))
        conexao.commit()
    except:
        conexao.rollback()
    finally:
        conexao.close()

def updateMovimentos(id, descricao, valor, categoria_id, pagamento_id, status, data):
    try:
        conexao = obterConexao()
        cursor = conexao.cursor()
        cursor.execute('UPDATE movimentos SET descricao = ?, valor = ?, categoria_id = ?, pagamento_id = ?, status = ?, data = ? WHERE id = ?', (descricao, valor, categoria_id, pagamento_id, status, data, id))
        conexao.commit()
    except:
        conexao.rollback()
    finally:
        conexao.close()

def deleteMovimentos(id):
    try:
        conexao = obterConexao()
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM movimentos WHERE id = ?', (id,))
        conexao.commit()
    except:
        conexao.rollback()
    finally:
        conexao.close()

        