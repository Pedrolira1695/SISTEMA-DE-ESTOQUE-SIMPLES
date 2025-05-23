import sqlite3
from datetime import datetime

DATABASE = 'inventory.db'

class InventoryController:
    def __init__(self):
        self.init_db()

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

    def add_item(self, item_id, name, quantity, usuario):
        conn = self.get_db()
        conn.execute('''
            INSERT INTO inventory (item_id, name, quantity)
            VALUES (?, ?, ?)
            ON CONFLICT(item_id) DO UPDATE SET quantity = quantity + ?
        ''', (item_id, name, quantity, quantity))
        self.log_movimentacao(conn, item_id, usuario, 'adicionou', quantity)
        conn.commit()
        conn.close()

    def remove_item(self, item_id, usuario):
        conn = self.get_db()
        conn.execute('DELETE FROM inventory WHERE item_id = ?', (item_id,))
        self.log_movimentacao(conn, item_id, usuario, 'removeu', 0)
        conn.commit()
        conn.close()
        return True

    def update_quantity(self, item_id, amount, usuario):
        conn = self.get_db()
        cursor = conn.execute('SELECT quantity FROM inventory WHERE item_id = ?', (item_id,))
        result = cursor.fetchone()
        if result:
            new_quantity = result['quantity'] + amount
            conn.execute('UPDATE inventory SET quantity = ? WHERE item_id = ?', (new_quantity, item_id))
            self.log_movimentacao(conn, item_id, usuario, 'atualizou', amount)
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False

    def log_movimentacao(self, conn, item_id, usuario, acao, quantidade):
        conn.execute('''
            INSERT INTO movimentacao (item_id, usuario, acao, quantidade, data_hora)
            VALUES (?, ?, ?, ?, ?)
        ''', (item_id, usuario, acao, quantidade, datetime.now()))

    def get_movimentacoes(self):
        conn = self.get_db()
        logs = conn.execute('SELECT * FROM movimentacao ORDER BY data_hora DESC').fetchall()
        conn.close()
        return logs
