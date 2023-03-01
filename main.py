import sys
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5 import uic
from add_edit_coffee import AddEditForm


class CoffeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.edit_add_form = None
        self.InitUi()

    def InitUi(self):
        self.set_table()
        self.btn_edit.clicked.connect(self.edit)
        self.btn_add.clicked.connect(self.add)

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

    def edit(self):
        row_id = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        if row_id:
            coffee_id = self.tableWidget.item(row_id[0], 0).text()
            self.edit_add_form = AddEditForm(coffee_id, other=self)
            self.edit_add_form.show()

    def update_table(self):
        self.set_table()

    def add(self):
        self.edit_add_form = AddEditForm(other=self)
        self.edit_add_form.show()

    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeApp()
    ex.show()
    sys.exit(app.exec())