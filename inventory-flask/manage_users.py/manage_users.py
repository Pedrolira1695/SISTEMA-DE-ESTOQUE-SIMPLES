import sqlite3

DATABASE = 'inventory.db'

def listar_usuarios():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM users')
        usuarios = cursor.fetchall()

        if not usuarios:
            print("Nenhum usuário encontrado.")
            return None

        print("\n--- Lista de Usuários ---")
        for user in usuarios:
            print(f"ID: {user['id']} | Nome: {user['name']} | Email: {user['email']}")

        return usuarios
    except sqlite3.OperationalError as e:
        print("Erro:", e)
        print("Verifique se a tabela 'users' existe e tem as colunas 'id', 'name', 'email'.")
        return None
    finally:
        conn.close()

def excluir_usuario_por_id(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    print(f"\n✅ Usuário com ID {user_id} excluído com sucesso.")

def main():
    usuarios = listar_usuarios()
    if not usuarios:
        return

    try:
        user_id = int(input("\nDigite o ID do usuário que deseja excluir: "))
    except ValueError:
        print("ID inválido. Encerrando.")
        return

    confirmar = input(f"Tem certeza que quer excluir o usuário com ID {user_id}? (s/n): ").lower()
    if confirmar == 's':
        excluir_usuario_por_id(user_id)
    else:
        print("❌ Operação cancelada.")

if __name__ == "__main__":
    main()
