from flask import Flask, render_template

import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", calendar_data=generate_calendar())

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
def log(month, week, day):
    print(f"Log: {month} {week} - Day {day} marked as Missão")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)