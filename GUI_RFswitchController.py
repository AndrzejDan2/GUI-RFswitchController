import sys
import serial.tools.list_ports
from usb import core
from usb import util
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QComboBox
from PyQt5.QtGui import QScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(int((screen.size().width()-screen_width)/2), int((screen.size().height()-screen_height)/2), screen_width, screen_height)
        self.setWindowTitle("RF Switch Controller :>")
        self.setFixedSize(self.size())
        self.avaliable_ports = list()
        self.init_widgets()
    def init_widgets(self):
        merged_layout = QtWidgets.QVBoxLayout()
        
        top_layout = QtWidgets.QHBoxLayout()
        connect_button = QtWidgets.QPushButton("Connect")
        connect_button.setFixedSize(90,40)
        refresh_button = QtWidgets.QPushButton("refresh")
        refresh_button.setFixedSize(70,40)
        devices = QComboBox()
        for i in self.avaliable_ports:
            devices.addItem(str(i[0]))



        top_layout.addWidget(connect_button)
        top_layout.addWidget(devices)
        top_layout.addWidget(refresh_button)
        
        bottom_layout = QtWidgets.QHBoxLayout()
        rf1_button = QtWidgets.QPushButton("RF-1")
        rf1_button.setFixedHeight(60)
        rf2_button = QtWidgets.QPushButton("RF-2")
        rf2_button.setFixedHeight(60)
        rf3_button = QtWidgets.QPushButton("RF-3")
        rf3_button.setFixedHeight(60)
        rf4_button = QtWidgets.QPushButton("RF-4")
        rf4_button.setFixedHeight(60)
        bottom_layout.addWidget(rf1_button)
        bottom_layout.addWidget(rf2_button)
        bottom_layout.addWidget(rf3_button)
        bottom_layout.addWidget(rf4_button)

        merged_layout.addLayout(top_layout)
        merged_layout.addLayout(bottom_layout)
        
        widget = QWidget()
        widget.setLayout(merged_layout)
        self.setCentralWidget(widget)

    def update_available_ports(self, arg):
        if isinstance(arg, list):
            self.avaliable_ports = arg


if __name__ == "__main__":
    #tu wrzucic obsluge portów :>
    ports = serial.tools.list_ports.comports()
    list_of_ports = list()
    for p in ports:
        list_of_ports.append([p.description, p.device, p.pid, p.vid])
    #print(len(ports), 'ports found')   <---------------------------------len(ports) to sie moze przydac
    print(list_of_ports)
    #

    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    screen_width = 640
    screen_height = 320
    window = MainWindow()
    window.update_available_ports(list_of_ports)
    #TODO reload combobox
    window.show()
    
    app.exec()
