import sys
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from addEditCoffeeForm import Ui_MainWindow


class AddEditForm(QMainWindow, Ui_MainWindow):
    def __init__(self, id=None, other=None):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.id = id
        self.other = other
        if id:
            self.set_table(id)
        else:
            self.set_empty_table()

        self.InitUi()

    def InitUi(self):
        self.btn_save.clicked.connect(self.save_data_to_table)
        self.btn_exit.clicked.connect(self.exit)

    def set_empty_table(self):
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Название сорта',
                                                    'Степень обжарки', 'Молотый/В зернах',
                                                    "Описание вкуса", "Цена", "Объем"])
        self.tableWidget.setRowCount(1)

    def save_data_to_table(self):
        try:
            cur = self.connection.cursor()
            row = [self.tableWidget.item(0, i).text() if self.tableWidget.item(0, i) else " " for i in range(7)]
            if self.id:
                row[0] = self.id
                cur.execute(f"""UPDATE coffee
                                SET sort='{row[1]}', roast='{row[2]}', type='{row[3]}',
                                    description='{row[4]}', price='{row[5]}', amount='{row[6]}'
                                WHERE id='{row[0]}'""")
                self.connection.commit()
            else:
                cur.execute(f"""INSERT INTO coffee
                                VALUES ('{row[0]}', '{row[1]}', '{row[2]}',
                                '{row[3]}', '{row[4]}', {row[5]}, {row[6]})""")
                self.connection.commit()
            if self.other:
                self.other.update_table()
            self.exit()
        except Exception as ex:
            pass

    def exit(self):
        self.close()

    def set_table(self, id):
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Название сорта',
                                                    'Степень обжарки', 'Молотый/В зернах',
                                                    "Описание вкуса", "Цена", "Объем"])
        res = self.connection.cursor().execute(f"SELECT * FROM coffee WHERE id={id}").fetchall()
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.connection.close()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AddEditForm()
    ex.show()
    sys.exit(app.exec())