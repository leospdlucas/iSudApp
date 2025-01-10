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
    year = datetime.now().year
    months = []
    for month in range(1, 13):
        month_name = calendar.month_name[month]
        month_calendar = calendar.monthcalendar(year, month)
        annotated_month = []
        for week in month_calendar:
            annotated_week = []
            for day in week:
                if day == 0:
                    annotated_week.append({"day": "", "message": ""})
                else:
                    day_message = "P-day" if (week.index(day) == 1) else "Almoço oferecido pela Missão" if 2 <= week.index(day) <= 5 else ""
                    annotated_week.append({"day": day, "message": day_message})
            annotated_month.append(annotated_week)
        months.append((month_name, annotated_month))

    return render_template('index.html', year=year, months=months)

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Criação da tabela caso ainda não exista
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendar_data (
            id SERIAL PRIMARY KEY,
            month VARCHAR(20),
            week INT,
            day INT,
            dupla_1 VARCHAR(100),
            dupla_2 VARCHAR(100),
            dupla_3 VARCHAR(100),
            dupla_4 VARCHAR(100)
        );
        """)
        conn.commit()
        print("Tabela 'calendar_data' criada (se não existia).")
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        cursor.close()
        close_db_connection(conn)

@app.route('/save', methods=['POST'])
def save_data():
    """
    Salva os dados recebidos do frontend no banco de dados PostgreSQL.
    """
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Query para inserir os dados no banco de dados
        query = """
        INSERT INTO calendar_data (month, week, day, dupla_1, dupla_2, dupla_3, dupla_4)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['month'],
            data['week'],
            data['day'],
            data['dupla_1'],
            data['dupla_2'],
            data['dupla_3'],
            data['dupla_4']
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
        query = "SELECT * FROM calendar_data"
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
    create_table()  # Criando a tabela se não existir
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.getenv('FLASK_DEBUG', False))