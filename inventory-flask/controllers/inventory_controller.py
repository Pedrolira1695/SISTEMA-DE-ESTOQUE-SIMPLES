# controllers/inventory_controller.py

import sqlite3
from datetime import datetime

DATABASE = 'inventory.db'

def create_users_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabela 'users' criada com sucesso.")

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def delete_user(user_id):
    conn = get_db()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    print(f"Usuário com ID {user_id} deletado.")

class InventoryController:
    def __init__(self):
        self.init_db()

    def get_movimentacoes(self):
        conn = self.get_db()
        logs = conn.execute('SELECT * FROM movimentacao ORDER BY data_hora DESC').fetchall()
        conn.close()
        return logs

    def get_db(self):
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        conn = self.get_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                item_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS movimentacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                usuario TEXT NOT NULL,
                acao TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                data_hora TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def get_all_items(self):
        conn = self.get_db()
        items = conn.execute('SELECT * FROM inventory').fetchall()
        conn.close()
        return items