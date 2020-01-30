from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A6, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import date
import sqlite3


def gt(data, pac_id):
    print(pac_id)
    db = "ССМ.db"  # Название базы данных
    con = sqlite3.connect(db)
    cur = con.cursor()
    results_ill = []
    results_patient = []
    print(data)

    def about_ill():
        results_ill.clear()
        cur.execute('SELECT * FROM Baza')
        while True:
            row = cur.fetchone()
            if row == None:
                break
            s0, s1, s2, s3, s4, s5, s6, s7, s8 = row[0], row[1], row[
                2], row[3], row[4], row[5], row[6], row[7], row[8]

        results_ill.append(s2)
        results_ill.append(s5)
        results_ill.append(s6)

    def about_patient():
        results_patient.clear()
        cur.execute('SELECT * FROM Patient WHERE ID = ?', [int(pac_id)])
        print(pac_id)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            s0, s1, s2, s3, s4 = row[0], row[1], row[2], row[3], row[4]

        results_patient.append(s1)
        results_patient.append(s2)
        results_patient.append(s4)

    about_ill()
    about_patient()
    year, month, day = str(date.today()).split("-")
    month_dictionary = ["", "января", "февраля", "марта", "апреля", "мая",
                        "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]

    canvas = Canvas("canvas.pdf")
    canvas.setPageSize(landscape(A6))
    pdfmetrics.registerFont(TTFont('arial', 'arial.ttf'))
    canvas.setFont('arial', 14)
    canvas.drawString(280, 280, f'«{day}» {month_dictionary[int(month)]} {year}г.')
    f = open('num_spravk.txt', 'r')
    num_spravk_to_write = f.read()
    f = open('num_spravk.txt', 'w')
    f.write(str(int(num_spravk_to_write) + 1))
    f = open('num_spravk.txt', 'r')
    canvas.setFont('arial', 18)
    canvas.drawString(150, 250, f"Справка №{f.read()}")
    canvas.setFont('arial', 14)
    canvas.drawString(15, 220, f"Выдана гр. {results_patient[0]}")
    canvas.drawString(15, 200, f"год рождения {results_patient[2]}")
    canvas.drawString(15, 180, f"проживающий (ая) по адресу:")
    canvas.drawString(15, 160, f"{results_patient[1]}")
    canvas.drawString(15, 140, f"Диагноз: {results_ill[0]}")
    canvas.drawString(15, 120, "")
    canvas.drawString(15, 100, f"Заключение: {results_ill[1]}")
    canvas.drawString(15, 80, "")
    canvas.setFont('arial', 10)
    canvas.drawString(15, 30, f"Имя доктора:")
    canvas.drawString(15, 15, f"{data[0]}")
    canvas.setFont('arial', 18)
    canvas.drawString(280, 30, f"Врач.......................")
    canvas.drawImage(data[1], 310, 25, width=90, height=45, mask='auto')
    canvas.drawImage(data[2], 165, 5, width=125, height=125, mask='auto')
    canvas.showPage()
    canvas.save()
    f.close()
