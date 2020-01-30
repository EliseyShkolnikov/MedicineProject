import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
from PyQt5.QtCore import *
from selenium import webdriver
db = "ССМ.db"  # Название базы данных
con = sqlite3.connect(db)
cur = con.cursor()
result = []
dates = []
# man = ["Шмышенко Валерий Альбертович", "Россия Череповец Ленина 228 666", ]


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show_alarm()

    def show_alarm(self):
        # con.close()
        db = "notifications_list.db"  # Название базы данных
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute('SELECT * FROM notifications')
        while True:
            row = cur.fetchone()
            if row == None:
                break
            to_return = row[1]
            break
        return(to_return)

    def med(self):
        MEDCARD.show()
        ALARM.hide()
        MAIN.hide()

    def chat(self):
        driver = webdriver.Chrome("chromedriver.exe")
        cur.execute('SELECT * FROM dialog')
        while True:
            row = cur.fetchone()
            if row == None:
                break
            s = row[-1]
        driver.get(s)  # Из базы данных

    def alarm(self):
        MAIN.show()
        ALARM.show()

    def diagnoz(self):
        print("ddddddd")

    def initUI(self):
        self.setWindowTitle('Медицина')
        self.textbox = QLabel(f'Уведомления: {self.show_alarm()}', self)
        self.btn1 = QPushButton('Медкарта', self)
        self.btn1.clicked.connect(self.med)
        self.btn2 = QPushButton('Чат с доктором', self)
        self.btn2.clicked.connect(self.chat)
        self.btn3 = QPushButton('Напоминания', self)
        self.btn3.clicked.connect(self.alarm)
        self.btn4 = QPushButton('Первая помощь', self)
        self.btn4.clicked.connect(self.diagnoz)
        self.btn5 = QPushButton('Талончики', self)
        self.btn5.clicked.connect(self.talon)
        self.lo1 = QHBoxLayout(self)
        self.lo2 = QVBoxLayout()
        self.lo2.addWidget(self.textbox)
        self.lo2.addWidget(self.btn1)
        self.lo2.addWidget(self.btn2)
        self.lo2.addWidget(self.btn3)
        self.lo2.addWidget(self.btn4)
        self.lo2.addWidget(self.btn5)
        self.lo1.addLayout(self.lo2)

    def talon(self):
        TALON.show()
        MAIN.hide()


class Talon(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.talon = []
        self.setWindowTitle('Выбор талона')
        self.btn5 = QPushButton('Назад', self)
        self.btn5.clicked.connect(self.late)
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.move(20, 20)
        cal.clicked[QDate].connect(self.showDate)
        self.lbl = QLabel(self)
        date = cal.selectedDate()
        self.lbl.setText(date.toString())
        self.combo = QComboBox(self)
        self.combo.addItems(['7:05', '7:10', "..."])
        self.combo.activated[str].connect(self.onActivated)
        self.btn7 = QPushButton('Выбрать!', self)
        self.btn7.clicked.connect(self.this)
        lo3 = QHBoxLayout(self)
        lo4 = QVBoxLayout()
        lo4.addWidget(cal)
        lo4.addWidget(self.lbl)
        lo4.addWidget(self.combo)
        lo4.addWidget(self.btn7)
        lo4.addWidget(self.btn5)

        lo3.addLayout(lo4)

    def this(self):  # тут должен выбираться талон и добавляться в напоминания, а тут удаляться из списка
        print("aaa")

    def onActivated(self, text):
        print(text)

    def showDate(self, date):
        self.lbl.setText(date.toString())

    def late(self):
        MAIN.show()
        TALON.hide()


class MedCard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def baze(self, qcombo_date):
        result.clear()
        self.edit.clear()
        cur.execute('SELECT * FROM Baza WHERE Date=?', [qcombo_date])
        while True:
            row = cur.fetchone()
            if row == None:
                break
            s0, s1, s2, s3, s4, s5, s6, s7, s8 = row[0], row[1], row[
                2], row[3], row[4], row[5], row[6], row[7], row[8]
        result.append(s0)
        result.append(s1)
        result.append(s2)
        result.append(s3)
        result.append(s4)
        result.append(s5)
        result.append(s6)
        result.append(s7)
        result.append(s8)
        self.edit.appendPlainText('Дата: ' + str(result[0]))
        self.edit.appendPlainText('Симптомы ' + str(result[1]))
        self.edit.appendPlainText('Анализы: ' + str(result[2]))
        self.edit.appendPlainText('Диагноз: ' + str(result[3]))
        self.edit.appendPlainText('Направления: ' + str(result[4]))
        self.edit.appendPlainText('Справки: ' + str(result[5]))
        self.edit.appendPlainText('Доктор: ' + str(result[6]))
        self.edit.appendPlainText('ID пациента: ' + str(result[7]))

    def show_dates(self):
        dates.clear()
        cur.execute('SELECT * FROM Baza')
        while True:
            row = cur.fetchone()
            if row == None:
                break
            s0 = row[0]
            dates.append(s0)

    def initUI(self):
        self.show_dates()
        combo = QComboBox(self)
        combo.addItems(dates)
        combo.activated[str].connect(self.onActivated)

        self.setWindowTitle('Медкарта')
        self.btn5 = QPushButton('Назад', self)
        self.btn5.clicked.connect(self.late)
        self.edit = QPlainTextEdit(self)
        self.lo3 = QHBoxLayout(self)
        self.lo4 = QVBoxLayout()
        self.lo4.addWidget(combo)
        self.lo4.addWidget(self.edit)
        self.lo4.addWidget(self.btn5)
        self.lo3.addLayout(self.lo4)

    def late(self):
        MEDCARD.hide()
        MAIN.show()

    def onActivated(self, text):
        self.baze(text)


class Alarm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Панель уведомлений')
        self.btn5 = QPushButton('Назад', self)
        self.btn5.clicked.connect(self.late)
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.move(20, 20)
        cal.clicked[QDate].connect(self.showDate)
        self.lbl = QLabel(self)
        date = cal.selectedDate()
        self.lbl.setText(date.toString())
        lo3 = QHBoxLayout(self)
        lo4 = QVBoxLayout()
        lo4.addWidget(cal)
        lo4.addWidget(self.lbl)
        lo4.addWidget(self.btn5)
        lo3.addLayout(lo4)

    def showDate(self, date):
        MAIN.hide()
        self.lbl.setText(date.toString())

    def late(self):
        ALARM.hide()
        MAIN.show()


if __name__ == '__main__':
    app = QApplication([])
    font = app.font()
    font.setPointSize(32)
    app.setFont(font)
    MAIN = Main()
    MEDCARD = MedCard()
    ALARM = Alarm()
    TALON = Talon()
    MAIN.show()
    sys.exit(app.exec_())
con.close()
