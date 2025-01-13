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
def index(year_calendar):

    return render_template('index.html', year_calendar)

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
                if day == 0:  # Dias fora do mês
                    week_data.append("")
                elif day_index == 1:  # Segunda-feira
                    week_data.append(f"{day} - P-Day")
                elif 2 <= day_index <= 5:  # Terça a Sexta-feira, apenas dias válidos
                    week_data.append(f"{day} - Missão")
                elif day_index == 0 or day_index == 6:  # Sábado e Domingo
                    week_data.append(str(day))
            month_data.append(week_data)
        year_calendar[month] = month_data
    return year_calendar

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