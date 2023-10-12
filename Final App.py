import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from Wlan1 import Ui_MainWindow
from capture_WLANs import capture_WLAN

# convertTo_db: converts the RSSI from the quality value (in %) to the decibel value (in dBm)
def convertTo_db(quality):
    if quality <= 0:
        dBm = -100
    elif quality >= 100:
        dBm = -50
    else:
        dBm = (quality / 2) - 100
    return dBm

# creating the MainWindow class: the one from which we will generate the window for the app
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.table = self.ui.tableWidget
        self.table.setSortingEnabled(False)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTable)
        self.timer.start(2000)  # Update every 2 seconds

    def updateTable(self):
        m = capture_WLAN()
        self.table.setSortingEnabled(True)
        self.table.setRowCount(0)  # Clear existing data

        for row in m:
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            self.table.setItem(rowPosition, 0, QTableWidgetItem(row[0]))
            self.table.setItem(rowPosition, 1, QTableWidgetItem("{}dBm ({}%)  ".format(convertTo_db(row[1]), row[1])))
            item = QTableWidgetItem()
            item.setData(Qt.DisplayRole, row[2])
            self.table.setItem(rowPosition, 2, item)
            self.table.setItem(rowPosition, 3, QTableWidgetItem(row[3]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
