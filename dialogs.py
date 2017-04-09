# -*- coding: utf-8 -*-
# QT
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#moje
import models
#others
from datetime import datetime


# ----------------  PALIWO  ---------------------------

class DG_paliwo_dodaj(QDialog):
    def __init__(self, session, parent = None):
        super(DG_paliwo_dodaj, self).__init__(parent)
        #self.resize(650, 400)
        #self.move(300, 250)
        self.setWindowTitle("Dodaj tankowanie")
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.session = session
        
        # auto
        self.layout.addWidget(QLabel("Auto"),0,0)
        self.auto = QComboBox()
        for i in self.session.query(models.Car).all():
            self.auto.addItem(i.name, i.id)
        self.layout.addWidget(self.auto,0,1)
        
        # data
        self.data = QCalendarWidget()
        self.data.setFirstDayOfWeek(1)
        self.data.setVerticalHeaderFormat(0)
        self.layout.addWidget(self.data, 0,2,5,3)
        
        # ilość
        self.layout.addWidget(QLabel(u"Ilość [litr]"),1,0)
        self.ilosc = QDoubleSpinBox()
        self.ilosc.setRange(0, 99999);
        self.layout.addWidget(self.ilosc, 1,1)
        # cena
        self.layout.addWidget(QLabel(u"Cena litra [zł]"), 2, 0)
        self.cena = QDoubleSpinBox()
        self.cena.setRange(0, 99999);
        self.layout.addWidget(self.cena,2,1)
        # wartosc
        '''self.layout.addWidget(QLabel(u"Wartość [zł]"), 3, 0)
        self.wartosc = QDoubleSpinBox()
        self.wartosc.setRange(0, 99999);
        self.layout.addWidget(self.wartosc,3,1)'''
        # przebieg
        self.layout.addWidget(QLabel("Przebieg [km]"),3,0)
        self.przebieg = QSpinBox()
        self.przebieg.setRange(0, 9999999);
        self.layout.addWidget(self.przebieg,3,1)

        # OK
        self.ok = QPushButton("Zapisz")
        self.layout.addWidget(self.ok, 5,0)
        self.ok.clicked.connect(self.click_ok)
        # Anuluj
        self.anuluj = QPushButton("Anuluj")
        self.layout.addWidget(self.anuluj, 5,1)
        self.anuluj.clicked.connect(self.click_anuluj)

    def click_ok(self):
        if self.auto.currentText() == None or self.ilosc.value() == 0.0 or self.cena.value() == 0.0 or \
        	self.data.selectedDate().toPyDate()>datetime.now().date():
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle(u"Błąd danych")
            msg.setText(u"Wszystkie pola muszą być uzupełnione.\nData nie może być przyszła.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        self.accept()

    def click_anuluj(self):
        self.reject()


class DG_paliwo_edytuj(QDialog):
    def __init__(self, session, parent = None):
        super(DG_paliwo_edytuj, self).__init__(parent)
        #self.resize(650, 400)
        #self.move(300, 250)
        self.setWindowTitle("Edytuj tankowanie")
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.session = session
        
        # ID
        self.layout.addWidget(QLabel("Identyfikator"),0,0)
        self.id = QComboBox()
        self.id.addItems([QString(str(i.id)) for i in self.session.query(models.Fuel).all()])
        self.layout.addWidget(self.id,0,1)

        self.id.currentIndexChanged.connect(self.zmianaID) # podlaczenie do listenera
        
        # data
        self.data = QCalendarWidget()
        self.data.setFirstDayOfWeek(1)
        self.data.setVerticalHeaderFormat(0)
        self.layout.addWidget(self.data, 1,2,4,3)
        
        # ilość
        self.layout.addWidget(QLabel(u"Ilość [litr]"),1,0)
        self.ilosc = QDoubleSpinBox()
        self.ilosc.setRange(0, 99999);
        self.layout.addWidget(self.ilosc, 1,1)
        # cena
        self.layout.addWidget(QLabel(u"Cena litra [zł]"), 2, 0)
        self.cena = QDoubleSpinBox()
        self.cena.setRange(0, 99999);
        self.layout.addWidget(self.cena,2,1)
        '''
        # wartosc
        self.layout.addWidget(QLabel(u"Wartość [zł]"), 3, 0)
        self.wartosc = QDoubleSpinBox()
        self.wartosc.setRange(0, 99999);
        self.layout.addWidget(self.wartosc,3,1)
        '''
        # przebieg
        self.layout.addWidget(QLabel("Przebieg [km]"),3,0)
        self.przebieg = QSpinBox()
        self.przebieg.setRange(0, 9999999);
        self.layout.addWidget(self.przebieg,3,1)

        # OK
        self.ok = QPushButton("Aktualizuj")
        self.layout.addWidget(self.ok, 5,0)
        self.ok.clicked.connect(self.click_ok)
        # Anuluj
        self.anuluj = QPushButton("Anuluj")
        self.layout.addWidget(self.anuluj, 5,1)
        self.anuluj.clicked.connect(self.click_anuluj)
        # Usun
        self.usun = QPushButton(u"Usuń")
        self.layout.addWidget(self.usun, 0,2)
        self.usun.clicked.connect(self.click_usun)

        self.zmianaID()

    def zmianaID(self):
        res=self.session.query(models.Fuel).filter_by(id=int(self.id.currentText())).first()
        self.ilosc.setValue(res.quantity)
        self.cena.setValue(res.price)
        self.przebieg.setValue(res.mileage)

    def click_ok(self):
        if self.id.currentText() == None or self.ilosc.value() == 0.0 or self.cena.value() == 0.0 or \
        	self.data.selectedDate().toPyDate()>datetime.now().date():
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle(u"Błąd danych")
            msg.setText(u"Wszystkie pola muszą być uzupełnione.\nData nie może być przyszła.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle(u"Operacja udana")
            msg.setText(u"Poprawnie zaktualizowano wpis.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.accept()

    def click_anuluj(self):
        self.reject()

    def click_usun(self):
        obj=self.session.query(models.Fuel).get(int(self.id.currentText()))
        self.session.delete(obj)
        self.session.commit()
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(u"Operacja udana")
        msg.setText(u"Poprawnie usunięto wpis.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.reject()

# ------------  NAPRAWA   -------------
class DG_naprawa_dodaj(QDialog):
    def __init__(self, session, parent = None):
        super(DG_naprawa_dodaj, self).__init__(parent)
        #self.resize(650, 400)
        #self.move(300, 250)
        self.setWindowTitle(u"Dodaj naprawę")
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.session = session
        
        # auto
        self.layout.addWidget(QLabel("Auto"),0,0)
        self.auto = QComboBox()
        for i in self.session.query(models.Car).all():
            self.auto.addItem(i.name, i.id)
        self.layout.addWidget(self.auto,0,1)

        # cena
        self.layout.addWidget(QLabel(u"Wartość [zł]"), 0, 2)
        self.cena = QDoubleSpinBox()
        self.cena.setRange(0, 99999);
        self.layout.addWidget(self.cena,0,3)

        # opis
        self.layout.addWidget(QLabel("Opis"),1,0)
        self.opis = QTextEdit()
        self.layout.addWidget(self.opis,2,0,1,2)
        
        # data
        self.data = QCalendarWidget()
        self.data.setFirstDayOfWeek(1)
        self.data.setVerticalHeaderFormat(0)
        self.layout.addWidget(self.data, 2,2,1,2)
        
        # OK
        self.ok = QPushButton("Zapisz")
        self.layout.addWidget(self.ok, 3,0)
        self.ok.clicked.connect(self.click_ok)
        # Anuluj
        self.anuluj = QPushButton("Anuluj")
        self.layout.addWidget(self.anuluj, 3,1)
        self.anuluj.clicked.connect(self.click_anuluj)

    def click_ok(self):
        if self.auto.currentText() == None or self.cena.value() == 0.0 or self.opis.toPlainText() == "" or \
        	self.data.selectedDate().toPyDate()>datetime.now().date():
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle(u"Błąd danych")
            msg.setText(u"Wszystkie pola muszą być uzupełnione.\nData nie może być przyszła.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        self.accept()

    def click_anuluj(self):
        self.reject()


class DG_naprawa_edytuj(QDialog):
    def __init__(self, session, parent = None):
        super(DG_naprawa_edytuj, self).__init__(parent)
        #self.resize(650, 400)
        #self.move(300, 250)
        self.setWindowTitle(u"Edytuj naprawę")
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.session = session
        
        # ID
        self.layout.addWidget(QLabel("Identyfikator"),0,0)
        self.id = QComboBox()
        self.id.addItems([QString(str(i.id)) for i in self.session.query(models.Reparation).all()])
        self.layout.addWidget(self.id,0,1)

        self.id.currentIndexChanged.connect(self.zmianaID) # podlaczenie do listenera

        # Usun
        self.usun = QPushButton(u"Usuń")
        self.layout.addWidget(self.usun, 0,2,1,2)
        self.usun.clicked.connect(self.click_usun)

        # cena
        self.layout.addWidget(QLabel(u"Wartość [zł]"), 1, 2)
        self.cena = QDoubleSpinBox()
        self.cena.setRange(0, 99999);
        self.layout.addWidget(self.cena,1,3)

        # opis
        self.layout.addWidget(QLabel("Opis"),1,0)
        self.opis = QTextEdit()
        self.layout.addWidget(self.opis,2,0,1,2)
        
        # data
        self.data = QCalendarWidget()
        self.data.setFirstDayOfWeek(1)
        self.data.setVerticalHeaderFormat(0)
        self.layout.addWidget(self.data, 2,2,1,2)
           

        # OK
        self.ok = QPushButton("Aktualizuj")
        self.layout.addWidget(self.ok, 3,0)
        self.ok.clicked.connect(self.click_ok)
        # Anuluj
        self.anuluj = QPushButton("Anuluj")
        self.layout.addWidget(self.anuluj, 3,1)
        self.anuluj.clicked.connect(self.click_anuluj)

        self.zmianaID()

    def zmianaID(self):
        res=self.session.query(models.Reparation).filter_by(id=int(self.id.currentText())).first()
        self.cena.setValue(res.price)
        self.opis.setText(res.description)
        

    def click_ok(self):
        if self.cena.value() == 0.0 or self.opis.toPlainText() == "" or self.data.selectedDate().toPyDate()>datetime.now().date():
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle(u"Błąd danych")
            msg.setText(u"Wszystkie pola muszą być uzupełnione.\nData nie może być przyszła.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle(u"Operacja udana")
            msg.setText(u"Poprawnie zaktualizowano wpis.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.accept()

    def click_anuluj(self):
        self.reject()

    def click_usun(self):
        obj=self.session.query(models.Reparation).get(int(self.id.currentText()))
        self.session.delete(obj)
        self.session.commit()
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(u"Operacja udana")
        msg.setText(u"Poprawnie usunięto wpis.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.reject()



# --------------------   WYMIANA  ----------------------------
class DG_wymiana_dodaj(QDialog):
    def __init__(self, session, parent = None):
        super(DG_wymiana_dodaj, self).__init__(parent)
        #self.resize(650, 400)
        #self.move(300, 250)
        self.setWindowTitle(u"Dodaj wymianę")
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.session = session
        
        # auto
        self.layout.addWidget(QLabel("Auto"),0,0)
        self.auto = QComboBox()
        for i in self.session.query(models.Car).all():
            self.auto.addItem(i.name, i.id)
        self.layout.addWidget(self.auto,0,1)

        # cena
        self.layout.addWidget(QLabel(u"Wartość [zł]"), 1, 0)
        self.cena = QDoubleSpinBox()
        self.cena.setRange(0, 99999);
        self.layout.addWidget(self.cena,1,1)

        # przebieg
        self.layout.addWidget(QLabel(u"Przebieg [km]"), 1, 2)
        self.przebieg = QDoubleSpinBox()
        self.przebieg.setRange(0, 9999999);
        self.layout.addWidget(self.przebieg,1,3)
        
        # data
        self.layout.addWidget(QLabel("Data wymiany:"),2,0)
        self.data = QCalendarWidget()
        self.data.setFirstDayOfWeek(1)
        self.data.setVerticalHeaderFormat(0)
        self.layout.addWidget(self.data, 3,0,1,2)

        # data nastepnej wymiany
        self.layout.addWidget(QLabel(u"Data następnej wymiany:"),2,2)
        self.data_next = QCalendarWidget()
        self.data_next.setFirstDayOfWeek(1)
        self.data_next.setVerticalHeaderFormat(0)
        self.layout.addWidget(self.data_next, 3,2,1,2)
        
        
        # opis
        self.layout.addWidget(QLabel("Opis"),4,0)
        self.opis = QTextEdit()
        self.layout.addWidget(self.opis,5,0,1,4)
        

        # OK
        self.ok = QPushButton("Zapisz")
        self.layout.addWidget(self.ok, 6,0)
        self.ok.clicked.connect(self.click_ok)
        # Anuluj
        self.anuluj = QPushButton("Anuluj")
        self.layout.addWidget(self.anuluj, 6,1)
        self.anuluj.clicked.connect(self.click_anuluj)

    def click_ok(self):
        if self.auto.currentText() == None or self.cena.value() == 0.0 or self.opis.toPlainText() == "" or \
        	self.data.selectedDate().toPyDate()>datetime.now().date() or self.przebieg.value() == 0.0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle(u"Błąd danych")
            msg.setText(u"Wszystkie pola muszą być uzupełnione.\nData nie może być przyszła.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        self.accept()

    def click_anuluj(self):
        self.reject()


class DG_wymiana_edytuj(QDialog):
    def __init__(self, session, parent = None):
        super(DG_wymiana_edytuj, self).__init__(parent)
        #self.resize(650, 400)
        #self.move(300, 250)
        self.setWindowTitle(u"Edytuj wymianę")
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.session = session
        
        # ID
        self.layout.addWidget(QLabel("Identyfikator"),0,0)
        self.id = QComboBox()
        self.id.addItems([QString(str(i.id)) for i in self.session.query(models.Replecement).all()])
        self.layout.addWidget(self.id,0,1)

        self.id.currentIndexChanged.connect(self.zmianaID) # podlaczenie do listenera

        # Usun
        self.usun = QPushButton(u"Usuń")
        self.layout.addWidget(self.usun, 0,2)
        self.usun.clicked.connect(self.click_usun)

        # cena
        self.layout.addWidget(QLabel(u"Wartość [zł]"), 1, 0)
        self.cena = QDoubleSpinBox()
        self.cena.setRange(0, 99999);
        self.layout.addWidget(self.cena,1,1)

        # przebieg
        self.layout.addWidget(QLabel(u"Przebieg [km]"), 1, 2)
        self.przebieg = QDoubleSpinBox()
        self.przebieg.setRange(0, 9999999);
        self.layout.addWidget(self.przebieg,1,3)
        
        # data
        self.layout.addWidget(QLabel("Data wymiany:"),2,0)
        self.data = QCalendarWidget()
        self.data.setFirstDayOfWeek(1)
        self.data.setVerticalHeaderFormat(0)
        self.layout.addWidget(self.data, 3,0,1,2)

        # data nastepnej wymiany
        self.layout.addWidget(QLabel(u"Data następnej wymiany:"),2,2)
        self.data_next = QCalendarWidget()
        self.data_next.setFirstDayOfWeek(1)
        self.data_next.setVerticalHeaderFormat(0)
        self.layout.addWidget(self.data_next, 3,2,1,2)
        
        
        # opis
        self.layout.addWidget(QLabel("Opis"),4,0)
        self.opis = QTextEdit()
        self.layout.addWidget(self.opis,5,0,1,4)
        

        # OK
        self.ok = QPushButton("Aktualizuj")
        self.layout.addWidget(self.ok, 6,0)
        self.ok.clicked.connect(self.click_ok)
        # Anuluj
        self.anuluj = QPushButton("Anuluj")
        self.layout.addWidget(self.anuluj, 6,1)
        self.anuluj.clicked.connect(self.click_anuluj)

        self.zmianaID()

    def zmianaID(self):
        res=self.session.query(models.Replecement).filter_by(id=int(self.id.currentText())).first()
        self.cena.setValue(res.price)
        self.przebieg.setValue(res.mileage)
        self.opis.setText(res.description)
        

    def click_ok(self):
        if self.cena.value() == 0.0 or self.opis.toPlainText() == "" or self.data.selectedDate().toPyDate()>datetime.now().date() or \
        		self.przebieg.value() == 0.0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle(u"Błąd danych")
            msg.setText(u"Wszystkie pola muszą być uzupełnione.\nData nie może być przyszła.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle(u"Operacja udana")
            msg.setText(u"Poprawnie zaktualizowano wpis.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.accept()

    def click_anuluj(self):
        self.reject()

    def click_usun(self):
        obj=self.session.query(models.Replecement).get(int(self.id.currentText()))
        self.session.delete(obj)
        self.session.commit()
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(u"Operacja udana")
        msg.setText(u"Poprawnie usunięto wpis.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.reject()




# --------------------   PRZEGLAD  ----------------------------
class DG_przeglad_dodaj(QDialog):
    def __init__(self, session, parent = None):
        super(DG_przeglad_dodaj, self).__init__(parent)
        #self.resize(650, 400)
        #self.move(300, 250)
        self.setWindowTitle(u"Dodaj przegląd")
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.session = session
        
        # auto
        l1 = QLabel("Auto")
        l1.setMaximumWidth(40)
        self.layout.addWidget(l1,0,0)
        self.auto = QComboBox()
        for i in self.session.query(models.Car).all():
            self.auto.addItem(i.name, i.id)
        self.layout.addWidget(self.auto,0,1)

        # cena
        l2 = QLabel(u"Wartość [zł]")
        l2.setMaximumWidth(80)
        self.layout.addWidget(l2, 0, 2)
        self.cena = QDoubleSpinBox()
        self.cena.setRange(0, 99999);
        self.layout.addWidget(self.cena,0,3)
        
        # data
        l3 = QLabel(u"Data przeglądu:")
        self.layout.addWidget(l3, 1,0,1,2)

        self.data = QCalendarWidget()
        self.data.setFirstDayOfWeek(1)
        self.data.setVerticalHeaderFormat(0)
        self.layout.addWidget(self.data, 2,0,1,2)
        # data nastepnego
        l4 = QLabel(u"Data następnego przeglądu:")
        self.layout.addWidget(l4, 1,2,1,2)

        self.data_next = QCalendarWidget()
        self.data_next.setFirstDayOfWeek(1)
        self.data_next.setVerticalHeaderFormat(0)
        self.layout.addWidget(self.data_next, 2,2,1,2)
        
        #uwagi
        self.layout.addWidget(QLabel(u"Uwagi"),3,0)
        self.uwagi = QTextEdit()
        self.layout.addWidget(self.uwagi,4,0,1,4)

        # OK
        self.ok = QPushButton("Zapisz")
        self.layout.addWidget(self.ok, 5,0)
        self.ok.clicked.connect(self.click_ok)
        # Anuluj
        self.anuluj = QPushButton("Anuluj")
        self.layout.addWidget(self.anuluj, 5,1)
        self.anuluj.clicked.connect(self.click_anuluj)

    def click_ok(self):
        if self.auto.currentText() == None or self.cena.value() == 0.0 or \
        	self.data.selectedDate().toPyDate()>datetime.now().date() or \
        	self.data_next.selectedDate().toPyDate()<=datetime.now().date():
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle(u"Błąd danych")
            msg.setText(u"Wszystkie pola muszą być uzupełnione.\nSprawdź poprawność.\nData następnego przeglądu nie może być wcześniejsza niż aktualna.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        self.accept()

    def click_anuluj(self):
        self.reject()


class DG_przeglad_edytuj(QDialog):
    def __init__(self, session, parent = None):
        super(DG_przeglad_edytuj, self).__init__(parent)
        #self.resize(650, 400)
        #self.move(300, 250)
        self.setWindowTitle(u"Edytuj przegląd")
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.session = session
        
        # ID
        l0 = QLabel("Identyfikator")
        l0.setMaximumWidth(80)
        self.layout.addWidget(l0,0,0)
        self.id = QComboBox()
        self.id.addItems([QString(str(i.id)) for i in self.session.query(models.TechnicalReview).all()])
        self.layout.addWidget(self.id,0,1)

        self.id.currentIndexChanged.connect(self.zmianaID) # podlaczenie do listenera


        # cena
        l2 = QLabel(u"Wartość [zł]")
        self.layout.addWidget(l2, 1, 2)
        l2.setMaximumWidth(150)
        self.cena = QDoubleSpinBox()
        self.cena.setRange(0, 99999);
        self.layout.addWidget(self.cena,1,3)
        
        # data
        l3 = QLabel(u"Data przeglądu:")
        self.layout.addWidget(l3, 2,0,1,2)

        self.data = QCalendarWidget()
        self.data.setFirstDayOfWeek(1)
        self.data.setVerticalHeaderFormat(0)
        self.layout.addWidget(self.data, 3,0,1,2)
        # data nastepnego
        l4 = QLabel(u"Data następnego przeglądu:")
        self.layout.addWidget(l4, 2,2,1,2)

        self.data_next = QCalendarWidget()
        self.data_next.setFirstDayOfWeek(1)
        self.data_next.setVerticalHeaderFormat(0)
        self.layout.addWidget(self.data_next, 3,2,1,2)

        #uwagi
        self.layout.addWidget(QLabel(u"Uwagi"),4,0)
        self.uwagi = QTextEdit()
        self.layout.addWidget(self.uwagi,5,0,1,4)

        # OK
        self.ok = QPushButton("Aktualizuj")
        self.layout.addWidget(self.ok, 6,0)
        self.ok.clicked.connect(self.click_ok)
        # Anuluj
        self.anuluj = QPushButton("Anuluj")
        self.layout.addWidget(self.anuluj, 6,1)
        self.anuluj.clicked.connect(self.click_anuluj)
        # Usun
        self.usun = QPushButton(u"Usuń")
        self.layout.addWidget(self.usun, 0,2)
        self.usun.clicked.connect(self.click_usun)

        self.zmianaID()

    def zmianaID(self):
        res=self.session.query(models.TechnicalReview).filter_by(id=int(self.id.currentText())).first()
        self.cena.setValue(res.price)
        self.uwagi.setText(res.comments)

    def click_ok(self):
        if self.auto.currentText() == None or self.cena.value() == 0.0 or \
        	self.data.selectedDate().toPyDate()>datetime.now().date() or \
        	self.data_next.selectedDate().toPyDate()<=datetime.now().date():
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle(u"Błąd danych")
            msg.setText(u"Wszystkie pola muszą być uzupełnione.\nSprawdź poprawność.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle(u"Operacja udana")
            msg.setText(u"Poprawnie zaktualizowano wpis.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.accept()

    def click_anuluj(self):
        self.reject()

    def click_usun(self):
        obj=self.session.query(models.TechnicalReview).get(int(self.id.currentText()))
        self.session.delete(obj)
        self.session.commit()
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(u"Operacja udana")
        msg.setText(u"Poprawnie usunięto wpis.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.reject()



# --------------------   UBEZPIECZENIE  ----------------------------
class DG_ubezpieczenie_dodaj(QDialog):
    def __init__(self, session, parent = None):
        super(DG_ubezpieczenie_dodaj, self).__init__(parent)
        #self.resize(650, 400)
        #self.move(300, 250)
        self.setWindowTitle(u"Dodaj ubezpieczenie")
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.session = session
        
        # auto
        l1 = QLabel("Auto")
        l1.setMaximumWidth(40)
        self.layout.addWidget(l1,0,0)
        self.auto = QComboBox()
        for i in self.session.query(models.Car).all():
            self.auto.addItem(i.name, i.id)
        self.layout.addWidget(self.auto,0,1)

        # cena
        l2 = QLabel(u"Wartość [zł]")
        l2.setMaximumWidth(100)
        self.layout.addWidget(l2, 0, 2)
        self.cena = QDoubleSpinBox()
        self.cena.setRange(0, 99999);
        self.layout.addWidget(self.cena,0,3)
        
        # data
        l5 = QLabel("Data ubezpieczenia:")
        self.layout.addWidget(l5,1,0,1,2)
        self.data = QCalendarWidget()
        self.data.setFirstDayOfWeek(1)
        self.data.setVerticalHeaderFormat(0)
        self.layout.addWidget(self.data, 2,0,1,2)
        # data nastepnego
        l6 = QLabel(u"Data następnego ubezpieczenia:")
        self.layout.addWidget(l6,1,2,1,2)
        self.data_next = QCalendarWidget()
        self.data_next.setFirstDayOfWeek(1)
        self.data_next.setVerticalHeaderFormat(0)
        self.layout.addWidget(self.data_next, 2,2,1,2)

        # firma
        l3 = QLabel("Firma")
        l3.setMaximumWidth(40)
        self.layout.addWidget(l3,3,0)
        self.firma = QTextEdit()
        self.firma.setMaximumHeight(40)
        self.layout.addWidget(self.firma,3,1,1,4)

        # auto
        l4 = QLabel("Typ")
        l4.setMaximumWidth(40)
        self.layout.addWidget(l4,4,0)
        self.typ = QComboBox()
        self.typ.addItems(["OC","OC+AC"])
        self.layout.addWidget(self.typ,4,1)

        #uwagi
        self.layout.addWidget(QLabel(u"Uwagi"),5,0)
        self.uwagi = QTextEdit()
        self.layout.addWidget(self.uwagi,6,0,1,4)
        
        # OK
        self.ok = QPushButton("Zapisz")
        self.layout.addWidget(self.ok, 7,0)
        self.ok.clicked.connect(self.click_ok)
        # Anuluj
        self.anuluj = QPushButton("Anuluj")
        self.layout.addWidget(self.anuluj, 7,1)
        self.anuluj.clicked.connect(self.click_anuluj)

    def click_ok(self):
        if self.auto.currentText() == None or self.cena.value() == 0.0 or \
        	self.data.selectedDate().toPyDate()>datetime.now().date() or \
        	self.data_next.selectedDate().toPyDate()<=datetime.now().date() or self.firma.toPlainText() == "":
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle(u"Błąd danych")
            msg.setText(u"Wszystkie pola muszą być uzupełnione.\nSprawdź poprawność.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        self.accept()

    def click_anuluj(self):
        self.reject()


class DG_ubezpieczenie_edytuj(QDialog):
    def __init__(self, session, parent = None):
        super(DG_ubezpieczenie_edytuj, self).__init__(parent)
        #self.resize(650, 400)
        #self.move(300, 250)
        self.setWindowTitle(u"Edytuj ubezpieczenie")
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.session = session
        
        # ID
        l0 = QLabel("Identyfikator")
        l0.setMaximumWidth(80)
        self.layout.addWidget(l0,0,0)
        self.id = QComboBox()
        self.id.addItems([QString(str(i.id)) for i in self.session.query(models.Insurance).all()])
        self.layout.addWidget(self.id,0,1)

        self.id.currentIndexChanged.connect(self.zmianaID) # podlaczenie do listenera

        # cena
        l2 = QLabel(u"Wartość [zł]")
        l2.setMaximumWidth(100)
        self.layout.addWidget(l2, 1, 2)
        self.cena = QDoubleSpinBox()
        self.cena.setRange(0, 99999);
        self.layout.addWidget(self.cena,1,3)
        
        # data
        l5 = QLabel("Data ubezpieczenia:")
        self.layout.addWidget(l5,2,0,1,2)
        self.data = QCalendarWidget()
        self.data.setFirstDayOfWeek(1)
        self.data.setVerticalHeaderFormat(0)
        self.layout.addWidget(self.data, 3,0,1,2)
        # data nastepnego
        l5 = QLabel(u"Data następnego ubezpieczenia:")
        self.layout.addWidget(l5,2,2,1,2)
        self.data_next = QCalendarWidget()
        self.data_next.setFirstDayOfWeek(1)
        self.data_next.setVerticalHeaderFormat(0)
        self.layout.addWidget(self.data_next, 3,2,1,2)

        # firma
        l3 = QLabel("Firma")
        l3.setMaximumWidth(60)
        self.layout.addWidget(l3,4,0)

        self.firma = QTextEdit()
        self.firma.setMaximumHeight(40)
        self.layout.addWidget(self.firma,4,1,1,4)

        # auto
        l4 = QLabel("Typ")
        l4.setMaximumWidth(40)
        self.layout.addWidget(l4,5,0)
        self.typ = QComboBox()
        self.typ.addItems(["OC","OC+AC"])
        self.layout.addWidget(self.typ,5,1)

        #uwagi
        self.layout.addWidget(QLabel(u"Uwagi"),6,0)
        self.uwagi = QTextEdit()
        self.layout.addWidget(self.uwagi,7,0,1,4)

        # OK
        self.ok = QPushButton("Aktualizuj")
        self.layout.addWidget(self.ok, 8,0)
        self.ok.clicked.connect(self.click_ok)
        # Anuluj
        self.anuluj = QPushButton("Anuluj")
        self.layout.addWidget(self.anuluj, 8,1)
        self.anuluj.clicked.connect(self.click_anuluj)
        # Usun
        self.usun = QPushButton(u"Usuń")
        self.layout.addWidget(self.usun, 0,2)
        self.usun.clicked.connect(self.click_usun)

        self.zmianaID()

    def zmianaID(self):
        res=self.session.query(models.Insurance).filter_by(id=int(self.id.currentText())).first()
        self.cena.setValue(res.price)
        self.firma.setText(res.firm)
        self.uwagi.setText(res.comments)
        self.typ.setCurrentIndex(self.typ.findText(QString(res.type_of)))

    def click_ok(self):
        if self.auto.currentText() == None or self.cena.value() == 0.0 or \
        	self.data.selectedDate().toPyDate()>datetime.now().date() or \
        	self.data_next.selectedDate().toPyDate()<=datetime.now().date() or self.firma.toPlainText() == "":
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle(u"Błąd danych")
            msg.setText(u"Wszystkie pola muszą być uzupełnione.\nSprawdź poprawność.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle(u"Operacja udana")
            msg.setText(u"Poprawnie zaktualizowano wpis.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.accept()

    def click_anuluj(self):
        self.reject()

    def click_usun(self):
        obj=self.session.query(models.Insurance).get(int(self.id.currentText()))
        self.session.delete(obj)
        self.session.commit()
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(u"Operacja udana")
        msg.setText(u"Poprawnie usunięto wpis.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.reject()

# -------------------------    SAMOCHODY    ----------------------------
class DG_samochody_dodaj(QDialog):
    def __init__(self, session, parent = None):
        super(DG_samochody_dodaj, self).__init__(parent)
        #self.resize(650, 400)
        #self.move(300, 250)
        self.setWindowTitle(u"Dodaj pojazd")
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.session = session
        
        # auto
        l1 = QLabel("Nazwa")
        #l1.setMaximumWidth(40)
        self.layout.addWidget(l1,0,0)
        self.auto_nazwa = QLineEdit()
        self.layout.addWidget(self.auto_nazwa,0,1)

        
        # numer rejestracji
        l2 = QLabel(u"Numer rejestracyjny")
        #l2.setMaximumWidth(50)
        self.layout.addWidget(l2, 0, 2)
        self.auto_rejestracja = QLineEdit()
        self.layout.addWidget(self.auto_rejestracja,0,3)

        # pelna nazwa
        l3 = QLabel(u"Opis")
        #l3.setMaximumWidth(50)
        self.layout.addWidget(l3, 1, 0)
        self.auto_pelnanazwa = QLineEdit()
        self.layout.addWidget(self.auto_pelnanazwa,1,1,1,3)

        # vin
        l4 = QLabel(u"Numer VIN")
        #l3.setMaximumWidth(50)
        self.layout.addWidget(l4, 2, 0)
        self.auto_vin = QLineEdit()
        self.layout.addWidget(self.auto_vin,2,1,1,3)

        # OK
        self.ok = QPushButton("Zapisz")
        self.layout.addWidget(self.ok, 3,0)
        self.ok.clicked.connect(self.click_ok)
        # Anuluj
        self.anuluj = QPushButton("Anuluj")
        self.layout.addWidget(self.anuluj, 3,1)
        self.anuluj.clicked.connect(self.click_anuluj)

    def click_ok(self):
        if self.auto_nazwa == None or self.auto_pelnanazwa == None or self.auto_rejestracja == None or self.auto_vin == None:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle(u"Błąd danych")
            msg.setText(u"Wszystkie pola muszą być uzupełnione.\nSprawdź poprawność.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        self.accept()

    def click_anuluj(self):
        self.reject()


class DG_samochody_edytuj(QDialog):
    def __init__(self, session, parent = None):
        super(DG_samochody_edytuj, self).__init__(parent)
        #self.resize(650, 400)
        #self.move(300, 250)
        self.setWindowTitle(u"Edytuj przegląd")
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.session = session
        
        # ID
        l0 = QLabel("Identyfikator")
        self.layout.addWidget(l0,0,0)
        self.id = QComboBox()
        self.id.addItems([QString(str(i.id)) for i in self.session.query(models.Car).all()])
        self.layout.addWidget(self.id,0,1)

        self.id.currentIndexChanged.connect(self.zmianaID) # podlaczenie do listenera

        # auto
        l1 = QLabel("Nazwa")
        #l1.setMaximumWidth(40)
        self.layout.addWidget(l1,1,0)
        self.auto_nazwa = QLineEdit()
        self.layout.addWidget(self.auto_nazwa,1,1)

        # numer rejestracji
        l2 = QLabel(u"Numer rejestracyjny")
        #l2.setMaximumWidth(50)
        self.layout.addWidget(l2, 1, 2)
        self.auto_rejestracja = QLineEdit()
        self.layout.addWidget(self.auto_rejestracja,1,3)

        # pelna nazwa
        l3 = QLabel(u"Pełna nazwa")
        #l3.setMaximumWidth(50)
        self.layout.addWidget(l3, 2, 0)
        self.auto_pelnanazwa = QLineEdit()
        self.layout.addWidget(self.auto_pelnanazwa,2,1,1,3)

        # vin
        l4 = QLabel(u"Numer VIN")
        #l3.setMaximumWidth(50)
        self.layout.addWidget(l4, 3, 0)
        self.auto_vin = QLineEdit()
        self.layout.addWidget(self.auto_vin,3,1,1,3)

        # OK
        self.ok = QPushButton("Aktualizuj")
        self.layout.addWidget(self.ok, 4,0)
        self.ok.clicked.connect(self.click_ok)
        # Anuluj
        self.anuluj = QPushButton("Anuluj")
        self.layout.addWidget(self.anuluj, 4,1)
        self.anuluj.clicked.connect(self.click_anuluj)
        # Usun
        self.usun = QPushButton(u"Usuń")
        self.layout.addWidget(self.usun, 0,2)
        self.usun.clicked.connect(self.click_usun)

        self.zmianaID()

    def zmianaID(self):
        res=self.session.query(models.Car).filter_by(id=int(self.id.currentText())).first()
        self.auto_nazwa.setText(res.name)
        self.auto_rejestracja.setText(res.registration_num)
        self.auto_pelnanazwa.setText(res.full_name)
        self.auto_vin.setText(res.vin)

    def click_ok(self):
        if self.auto_nazwa == None or self.auto_pelnanazwa == None or self.auto_rejestracja == None or self.auto_vin == None:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle(u"Błąd danych")
            msg.setText(u"Wszystkie pola muszą być uzupełnione.\nSprawdź poprawność.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle(u"Operacja udana")
            msg.setText(u"Poprawnie zaktualizowano wpis.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.accept()

    def click_anuluj(self):
        self.reject()

    def click_usun(self):
        obj=self.session.query(models.Car).get(int(self.id.currentText()))
        self.session.delete(obj)
        self.session.commit()
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(u"Operacja udana")
        msg.setText(u"Poprawnie usunięto wpis.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.reject()
