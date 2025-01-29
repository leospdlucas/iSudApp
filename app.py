from flask import Flask, request, jsonify, render_template
from db_config import get_db_connection, close_db_connection
from datetime import datetime
import calendar
import locale
import os

app = Flask(__name__)

try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    print("Erro ao definir locale")

@app.route('/')
def index():
    year_calendar = generate_calendar()
    return render_template('index.html', months=year_calendar.items())

def generate_calendar():
    year = datetime.now().year
    cal = calendar.Calendar(firstweekday=6)  # Começa no domingo
    months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    year_calendar = {}
    for i, month in enumerate(months, start=1):
        month_data = []
        for week in cal.monthdayscalendar(year, i):
            week_data = []
            for day_index, day in enumerate(week):
                if day == 0:
                    week_data.append("")
                elif day_index == 1: # Segunda
                    week_data.append(f"{day} - P-Day ")
                elif day_index in [0, 6]:  # Sábado e Domingo
                    week_data.append(str(day))
                else:
                    week_data.append(f"{day} - Missão")
            month_data.append(week_data)
        year_calendar[month] = month_data
    return year_calendar

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        DROP TABLE IF EXISTS calendar_data;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendar_data (
            id SERIAL PRIMARY KEY,
            month VARCHAR(20),
            week INT,
            day INT,
            dupla_1 VARCHAR(100),
            dupla_2 VARCHAR(100),
            dupla_3 VARCHAR(100),
            dupla_4 VARCHAR(100),
            UNIQUE (month, week, day)
        );
        """)
        conn.commit()
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        cursor.close()
        close_db_connection(conn)

@app.route('/save', methods=['POST'])
def save_data():
    """
    Salva os dados recebidos do frontend no banco de dados PostgreSQL.
    Verifica se o campo já foi preenchido antes de salvar e valida uma senha se necessário.
    """
    data = request.get_json()
    senha_admin = os.getenv('ADMIN_PASSWORD', 'minhasenha')  # Define a senha padrão

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Verifica se o registro já existe
        query_check = """
        SELECT dupla_1, dupla_2, dupla_3, dupla_4 FROM calendar_data
        WHERE month = %s AND week = %s AND day = %s
        """
        cursor.execute(query_check, (data['month'], data['week'], data['day']))
        existing = cursor.fetchone()

        if existing:
            # Verifica se há campos já preenchidos e exige a senha para alterá-los
            if any(existing) and data.get('password') != senha_admin:
                return jsonify({"message": "Campo já preenchido. Alterações não permitidas sem a senha correta."}), 403

        # Atualiza ou insere os dados
        query = """
        INSERT INTO calendar_data (month, week, day, dupla_1, dupla_2, dupla_3, dupla_4)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (month, week, day)
        DO UPDATE SET
            dupla_1 = EXCLUDED.dupla_1,
            dupla_2 = EXCLUDED.dupla_2,
            dupla_3 = EXCLUDED.dupla_3,
            dupla_4 = EXCLUDED.dupla_4
        """
        values = (
            data['month'],
            data['week'],
            data['day'],
            data.get('dupla_1', existing[0] if existing else None),
            data.get('dupla_2', existing[1] if existing else None),
            data.get('dupla_3', existing[2] if existing else None),
            data.get('dupla_4', existing[3] if existing else None),
        )
        cursor.execute(query, values)
        conn.commit()

        return jsonify({"message": "Dados salvos com sucesso!"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

@app.route('/fetch', methods=['GET'])
def fetch_data():
    """
    Recupera os dados armazenados no banco de dados para exibição no frontend.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Query para buscar os dados
        query = "SELECT month, week, day, dupla_1, dupla_2, dupla_3, dupla_4 FROM calendar_data"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Convertendo os dados para JSON
        data = [
            {
                "month": row[0],
                "week": row[1],
                "day": row[2],
                "dupla_1": row[3],
                "dupla_2": row[4],
                "dupla_3": row[5],
                "dupla_4": row[6],
            }
            for row in rows
        ]

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

if __name__ == '__main__':
    create_table()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.getenv('FLASK_DEBUG', False))
