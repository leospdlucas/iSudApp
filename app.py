from flask import Flask, render_template

import os
import sqlite3

app = Flask(__name__)

DATABASE = 'data.db'



def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month TEXT NOT NULL,
                week INTEGER NOT NULL,
                day INTEGER NOT NULL,
                mission1 TEXT,
                mission2 TEXT,
                mission3 TEXT,
                mission4 TEXT
            )
        ''')

init_db()  # Inicializa o banco de dados se não existir

@app.route("/")
def index():
    return render_template("index.html", calendar_data=generate_calendar())

@app.route("/save", methods=["POST"])
def save():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO entries (month, week, day, mission1, mission2, mission3, mission4)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data['month'], data['week'], data['day'], 
          data['mission1'], data['mission2'], data['mission3'], data['mission4']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

def generate_calendar():
    import calendar
    year = 2025
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



if __name__ == "__main__":
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)