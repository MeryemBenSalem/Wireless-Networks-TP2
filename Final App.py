import subprocess
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
# selectBestNetwork: selects the Wi-Fi network with the highest signal strength (RSSI)
def selectBestNetwork(networks):
    best_network = max(networks, key=lambda x: x[1])
    return best_network

# connectToNetwork: connects to the specified Wi-Fi network
def connectToNetwork(ssid):
    try:
        cmd = f"netsh wlan connect name={ssid}"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        return True
    except Exception as e:
        print(f"Failed to connect to the network: {str(e)}")
        return False
    
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
        self.timer.start(1000)  # Update every 1 second

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
     # Select and connect to the best Wi-Fi network
        best_network = selectBestNetwork(m)
        if best_network:
            ssid = best_network[0]
            if connectToNetwork(ssid):
                print(f"Connected to the best network: {ssid}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
