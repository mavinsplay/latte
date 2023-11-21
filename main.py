import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton
from sqlite3 import connect
from ui import Ui_MainWindow

class CoffeeApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Эспрессо')
        self.butt = QPushButton(self, text='прочитать таблицу')
        self.butt.setGeometry(100, 100, 200, 100)
        self.butt.move(400, 500)
        self.butt.clicked.connect(self.sql)
        self.addButton.clicked.connect(self.addst)
        self.editButton.clicked.connect(self.editst)

    def sql(self):
        con = connect('coffee.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM cofee""").fetchall()
        con.commit()
        con.close()
        self.tableWidget.setRowCount(len(result))
        id = 1
        for i, j in enumerate(result):
            for h, k in enumerate(j):
                self.tableWidget.setItem(i, h, QTableWidgetItem(str(k)))
            id += 1

    def addst(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)

    def editst(self):
        num_rows = self.tableWidget.rowCount()
        items = [(self.tableWidget.item(row, 1).text(),
                  self.tableWidget.item(row, 2).text(),
                  self.tableWidget.item(row, 3).text(),
                  self.tableWidget.item(row, 4).text(),
                  self.tableWidget.item(row, 5).text(),
                  self.tableWidget.item(row, 6).text())
                 for row in range(num_rows) if all(self.tableWidget.item(row, col) for col in range(1, 7))]

        if not items:
            print("Новые значения не введены. Ничего не добавлено.")
            return

        con = connect('coffee.sqlite')
        cur = con.cursor()
        for i in items:
            print(i)
            cur.execute(
                'INSERT INTO cofee (sort_name, roasting, ground_grain, taste, price, value) VALUES (?, ?, ?, ?, ?, ?)', 
                i)
        print('Данные успешно добавлены')
        con.commit()
        con.close()
        self.sql()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = CoffeeApp()
    mainWindow.show()
    sys.exit(app.exec_())
