import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pdf_generator
import sqlite3
from datetime import date
from time import sleep
from selenium import webdriver
db = "ССМ.db"  # Название базы данных
con = sqlite3.connect(db)
cur = con.cursor()
passwd_s = []
names = []
fio_s = []
all_Data = []
names.clear()
cur.execute('SELECT * FROM Reg')
while True:
    row = cur.fetchone()
    if row == None:
        break
    s0 = row[0]
    names.append(s0)

# pac_id = 0


class Avto(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Авторизация')
        self.initUI()

    def initUI(self):
        textbox1 = QLabel(f'Если вы уже зарегестрированы: ', self)
        textbox2 = QLabel(f'Если ещё не регестрировались: ', self)
        self.qle1 = QLineEdit(self)
        self.qle1.setPlaceholderText('Введите пароль')
        self.bt0 = QPushButton('Регистрация', self)
        self.bt0.clicked.connect(self.new1)
        self.bt2 = QPushButton('Войти', self)
        self.bt2.clicked.connect(self.onactive)
        self.combo = QComboBox(self)
        self.combo.addItems(names)
        self.combo.activated[str].connect(self.onActivated)
        lo3 = QHBoxLayout(self)
        lo4 = QVBoxLayout()
        lo4.addWidget(textbox1)
        lo4.addWidget(self.combo)
        lo4.addWidget(self.qle1)
        lo4.addWidget(self.bt2)
        lo4.addWidget(textbox2)
        lo4.addWidget(self.bt0)
        lo3.addLayout(lo4)

    def onactive(self):
        passwd_s.clear()
        cur.execute('SELECT * FROM Reg')
        while True:
            row = cur.fetchone()
            if row == None:
                break
            s0 = f"{row[0]} + {row[4]}"
            fio_s.append(s0)
        if self.choised_name == "Выберите пользователя" or self.choised_name == '':
            self.qle1.setPlaceholderText(
                'Выберите пользователя или зарегестрируйтесь')
        if f"{self.choised_name} + {self.qle1.text()}" in fio_s:
            cur.execute(
                'SELECT * FROM Reg WHERE FIO = ? AND Passwd = ?', [self.choised_name, str(self.qle1.text())])
            while True:
                row = cur.fetchone()
                if row == None:
                    break
                else:
                    all_Data.extend(row[:4])
            EX.show()
            AVTO.hide()
        else:
            self.qle1.clear()
            self.qle1.setPlaceholderText('Пароль или логин не верен!')

    def onActivated(self, text):
        self.choised_name = text
        print(self.choised_name)

    def new1(self):
        CHECK.show()
        AVTO.hide()


class Check(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Регестрация')
        self.petcat = None
        self.podpic = None
        self.initUI()

    def initUI(self):
        self.textbox1 = QLabel(f'Регистрация врача ', self)
        self.textbox2 = QLabel(f'*Картинки только в .png!', self)
        self.qle1 = QLineEdit(self)
        self.qle1.setPlaceholderText('Назовитесь (ФИО)')
        self.qle2 = QLineEdit(self)
        self.qle2.setPlaceholderText('Придумайте пароль')
        self.btn1 = QPushButton('Выбрать печать..', self)
        self.btn1.clicked.connect(self.pech)
        self.btn2 = QPushButton('Выбрать подпись..', self)
        self.btn2.clicked.connect(self.podp)
        self.btn3 = QPushButton('Войти', self)
        self.btn3.clicked.connect(self.entrance)
        lo1 = QHBoxLayout(self)
        lo2 = QVBoxLayout()
        lo2.addWidget(self.textbox1)
        lo2.addWidget(self.qle1)
        lo2.addWidget(self.qle2)
        lo2.addWidget(self.btn1)
        lo2.addWidget(self.btn2)
        lo2.addWidget(self.btn3)
        lo2.addWidget(self.textbox2)
        lo1.addLayout(lo2)

    def pech(self):
        self.petcat = QFileDialog.getOpenFileName(
            self, "Open Image", "C:/", "Image Files (*.png)")

    def podp(self):
        self.podpic = QFileDialog.getOpenFileName(
            self, "Open Image", "C:/", "Image Files (*.png)")

    def entrance(self):
        if self.qle1.text() == '' or self.qle2.text() == '' or self.podpic == None or self.petcat == None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Ошибка")
            msg.setText(f"Ошибка ввода данных или файлов")
            okButton = msg.addButton('Ок', QMessageBox.AcceptRole)
            msg.exec()
            if msg.clickedButton() == okButton:
                self.qle1.clear()
                self.qle2.clear()

        else:
            name = str(self.qle1.text())
            password = str(self.qle2.text())
            cur.execute("INSERT INTO Reg(FIO) VALUES(?)",
                        ["TODEL"])
            con.commit()
            doc_id = cur.lastrowid
            print(doc_id)
            cur.execute("DELETE FROM Reg WHERE FIO = ?", ["TODEL"])
            cur.execute("INSERT INTO Reg(FIO, Passwd, Podpisb, Pechatb, Id) VALUES(?, ?, ?, ?, ?)",
                        [name, str(password), self.podpic[0], self.petcat[0], doc_id])
            cur.execute(
                'SELECT * FROM Reg WHERE FIO = ? AND Passwd = ?', [name, str(password)])
            while True:
                row = cur.fetchone()
                if row == None:
                    break
                else:
                    all_Data.extend(row[:4])
            con.commit()
            EX.show()
            CHECK.hide()


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Медицина 2.0')
        self.initUI()

    def med(self):
        MEDCARD.show()
        EX.hide()

    def chat(self):
        if self.btn2.text() == "Чат с пациентом":
            self.btn2.setText("Закрыть Чат")
            driver = webdriver.Chrome("chromedriver.exe")
            driver.get('https://talkrooms.ru/#+')
            driver.find_element_by_class_name("hall-create").click()
            search_form1 = driver.find_element_by_xpath(
                '//*[@id="main"]/div[4]/form/div[2]/div[4]/textarea')
            search_form1.send_keys(f'Здравствуйте, с Вами доктор {all_Data[0]}')
            search_form1.submit()
            driver.implicitly_wait(2)  # Если будут вылеты, сделать больше
            driver.find_element_by_class_name('toolbar-tools').click()
            driver.find_element_by_class_name('send-arrow').click()
            driver.find_element_by_class_name('nickname').click()
            driver.find_element_by_id('my-nickname').click()
            search_form2 = driver.find_element_by_id('my-nickname')
            search_form2.submit()
            driver.implicitly_wait(2)  # Если будут вылеты, сделать больше
            self.ur = driver.current_url  # URL Врача, поместить в базу данных!
            print(self.ur)
            cur.execute("INSERT INTO dialog(url) VALUES(?)", [self.ur])
            con.commit()
        else:
            self.btn2.setText('Чат с пациентом')
            cur.execute("DELETE FROM dialog WHERE url = ?", [self.ur])

    def alarm(self):
        PRIEM.show()

    def text_read(self):
        f = open(r'TestCOM\Example.txt')
        pac_id = f.read()
        return(str(pac_id))

    def spravka(self):
        print(all_Data)
        print(self.text_read())
        pdf_generator.gt(all_Data, self.text_read())

    def initUI(self):
        self.textbox = QLabel('Пациент:')
        self.btn1 = QPushButton('Медкарта', self)
        self.btn1.clicked.connect(self.med)
        self.btn2 = QPushButton('Чат с пациентом', self)
        self.btn2.clicked.connect(self.chat)
        self.btn3 = QPushButton('Записи клиентов', self)
        self.btn3.clicked.connect(self.alarm)
        self.btn4 = QPushButton('Генерация справок', self)
        self.btn4.clicked.connect(self.spravka)

        lo1 = QHBoxLayout(self)
        lo2 = QVBoxLayout()

        lo2.addWidget(self.textbox)
        lo2.addWidget(self.btn1)
        lo2.addWidget(self.btn2)
        lo2.addWidget(self.btn3)
        lo2.addWidget(self.btn4)
        lo1.addLayout(lo2)

        timer = QTimer(self)
        timer.timeout.connect(self.textbox_update)
        timer.start(10)

    def textbox_update(self):
        cur.execute('SELECT * FROM Patient WHERE ID = ?', [self.text_read()])
        while True:
            row = cur.fetchone()
            if row == None:
                break
            self.textbox.setText(f"Пациент:\n{row[1]}")  # оптимизировать


class Medcard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Медкарта пациента')
        self.initUI()

    def initUI(self):
        self.qle1 = QLineEdit(self)
        self.qle1.setPlaceholderText('Дата заболевания:')
        self.qle2 = QLineEdit(self)
        self.qle2.setPlaceholderText('Симтомы:')
        self.qle3 = QLineEdit(self)
        self.qle3.setPlaceholderText('Анализы:')
        self.qle4 = QLineEdit(self)
        self.qle4.setPlaceholderText('Диагноз:')
        self.qle5 = QLineEdit(self)
        self.qle5.setPlaceholderText('Направление:')
        self.qle6 = QLineEdit(self)
        self.qle6.setPlaceholderText('Справки:')
        self.qle7 = QLineEdit(self)
        self.qle7.setPlaceholderText('Доктор:')
        self.btn1 = QPushButton('Занести пациенту', self)
        self.btn1.clicked.connect(self.med)
        self.btn2 = QPushButton('Назад', self)
        self.btn2.clicked.connect(self.backout)

        lo1 = QHBoxLayout(self)
        lo2 = QVBoxLayout()
        lo3 = QVBoxLayout()

        lo2.addWidget(self.qle1)
        lo2.addWidget(self.qle2)
        lo2.addWidget(self.qle3)
        lo2.addWidget(self.qle4)
        lo2.addWidget(self.qle5)
        lo2.addWidget(self.qle6)
        lo2.addWidget(self.qle7)
        lo2.addWidget(self.btn1)
        lo2.addWidget(self.btn2)

        lo1.addLayout(lo2)

    def med(self):
        patient = 1
        Case = 2
        caseid = 3
        cur.execute("INSERT INTO Baza(Date, Problems, Diagnosis, Analyses, Direction, Referencess, Doctor, Patient_ID, Casee, Case_ID) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [self.qle1.text(), self.qle2.text(), self.qle3.text(), self.qle4.text(), self.qle5.text(), self.qle6.text(), self.qle7.text(), patient, Case, caseid])
        con.commit()

    def backout(self):
        EX.show()
        MEDCARD.hide()


class Priem(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.l = QLabel('Запись на сегодня', self)
        self.edit1 = QPlainTextEdit(self)
        self.edit1.appendPlainText('Приём в 8:35')
        self.edit2 = QPlainTextEdit(self)
        self.edit2.appendPlainText('')
        self.talon = []
        self.setWindowTitle('Выбор талона')
        self.btn3 = QPushButton('Найти на..', self)
        self.btn3.clicked.connect(self.this)
        self.btn5 = QPushButton('Назад', self)
        self.btn5.clicked.connect(self.late)
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.move(20, 20)
        cal.clicked[QDate].connect(self.showDate)
        self.lbl = QLabel(self)
        self.date = cal.selectedDate()
        self.lbl.setText(self.date.toString())

        lo3 = QHBoxLayout(self)
        lo4 = QVBoxLayout()
        lo5 = QVBoxLayout()
        lo6 = QVBoxLayout()

        lo4.addWidget(cal)
        lo4.addWidget(self.btn3)
        lo4.addWidget(self.btn5)
        lo5.addWidget(self.l)
        lo5.addWidget(self.edit1)
        lo6.addWidget(self.lbl)
        lo6.addWidget(self.edit2)

        lo3.addLayout(lo5)
        lo3.addLayout(lo4)
        lo3.addLayout(lo6)

    def this(self):  # тут должен выбираться талон и добавляться в напоминания, а тут удаляться из списка
        self.lbl.setText(self.date.toString())

    def onActivated(self, text):
        print(text)

    def showDate(self, date):
        self.lbl.setText(date.toString())

    def late(self):
        EX.show()
        PRIEM.hide()


if __name__ == '__main__':
    app = QApplication([])
    font = app.font()
    font.setPointSize(32)
    app.setFont(font)
    EX = Example()
    CHECK = Check()
    AVTO = Avto()
    MEDCARD = Medcard()
    PRIEM = Priem()
    AVTO.show()
    sys.exit(app.exec_())
con.close()
