import sys
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5 import uic


class CoffeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.InitUi()

    def InitUi(self):
        self.set_table()

    def set_table(self):
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Название сорта',
                                                    'Степень обжарки', 'Молотый/В зернах',
                                                    "Описание вкуса", "Цена", "Объем"])
        res = self.connection.cursor().execute("SELECT * FROM coffee").fetchall()
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeApp()
    ex.show()
    sys.exit(app.exec())