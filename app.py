from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Senha administrativa
ADMIN_PASSWORD = "sua_senha_segura"  # Defina uma senha segura

# Banco de dados
DB_NAME = "calendar.db"

# Criação da tabela se não existir
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendar_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT,
            week TEXT,
            day TEXT,
            key TEXT,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Rota para buscar os dados salvos
@app.route('/fetch', methods=['GET'])
def fetch_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT month, week, day, key, value FROM calendar_data")
    rows = cursor.fetchall()
    conn.close()
    data = [{"month": row[0], "week": row[1], "day": row[2], "key": row[3], "value": row[4]} for row in rows]
    return jsonify(data)

# Rota para salvar ou atualizar dados
@app.route('/save', methods=['POST'])
def save_data():
    data = request.json
    month = data.get('month')
    week = data.get('week')
    day = data.get('day')
    key = data.get('key')
    value = data.get('value')
    password = data.get('password')

    if not month or not week or not day or not key or value is None:
        return jsonify({"error": "Dados inválidos."}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Verifica se o registro já existe
    cursor.execute('''
        SELECT value FROM calendar_data WHERE month = ? AND week = ? AND day = ? AND key = ?
    ''', (month, week, day, key))
    existing_entry = cursor.fetchone()

    # Se o valor já existir e for diferente, valida a senha
    if existing_entry:
        if existing_entry[0] != value:
            if password != ADMIN_PASSWORD:
                conn.close()
                return jsonify({"error": "Senha incorreta para atualizar o campo."}), 403

            # Atualiza o valor existente
            cursor.execute('''
                UPDATE calendar_data SET value = ? WHERE month = ? AND week = ? AND day = ? AND key = ?
            ''', (value, month, week, day, key))
            conn.commit()
            conn.close()
            return jsonify({"message": "Campo atualizado com sucesso."})
        else:
            conn.close()
            return jsonify({"message": "Nenhuma alteração necessária."})

    # Insere novo registro
    cursor.execute('''
        INSERT INTO calendar_data (month, week, day, key, value)
        VALUES (?, ?, ?, ?, ?)
    ''', (month, week, day, key, value))
    conn.commit()
    conn.close()
    return jsonify({"message": "Dados salvos com sucesso."})

if __name__ == '__main__':
    app.run(debug=True)
