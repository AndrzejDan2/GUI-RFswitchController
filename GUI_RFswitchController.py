import sys
import serial.tools.list_ports
import serial
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QComboBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.serial_port = VirtualCOMPort()

        self.setGeometry(int((screen.size().width()-screen_width)/2), int((screen.size().height()-screen_height)/2), screen_width, screen_height)
        self.setWindowTitle("RF Switch Controller :>")
        self.setFixedSize(self.size())

        self.connect_button = QtWidgets.QPushButton("Connect")
        self.reload_button = QtWidgets.QPushButton("reload")
        self.devices = QComboBox()
        self.rf1_button = QtWidgets.QPushButton("RF_1")
        self.rf2_button = QtWidgets.QPushButton("RF_2")
        self.rf3_button = QtWidgets.QPushButton("RF_3")
        self.rf4_button = QtWidgets.QPushButton("RF_4")
        self.config_widgets()
        
    def config_widgets(self):
        merged_layout = QtWidgets.QVBoxLayout()
        
        top_layout = QtWidgets.QHBoxLayout()

        self.connect_button.setFixedSize(90,40)
        self.connect_button.setObjectName('connect')
        self.connect_button.clicked.connect(self.button_clicked)

        self.reload_button.setFixedSize(70,40)
        self.reload_button.setObjectName('reload')
        self.reload_button.clicked.connect(self.button_clicked)

        self.get_ports(self.serial_port.list_of_ports)
        

        top_layout.addWidget(self.connect_button)
        top_layout.addWidget(self.devices)
        top_layout.addWidget(self.reload_button)
        
        bottom_layout = QtWidgets.QHBoxLayout()

        self.rf1_button.setFixedHeight(60)
        self.rf1_button.setObjectName('rf1')
        self.rf1_button.setEnabled(False)
        self.rf1_button.clicked.connect(self.button_clicked)

        self.rf2_button.setFixedHeight(60)
        self.rf2_button.setObjectName('rf2')
        self.rf2_button.setEnabled(False)
        self.rf2_button.clicked.connect(self.button_clicked)

        self.rf3_button.setFixedHeight(60)
        self.rf3_button.setObjectName('rf3')
        self.rf3_button.setEnabled(False)
        self.rf3_button.clicked.connect(self.button_clicked)

        self.rf4_button.setFixedHeight(60)
        self.rf4_button.setObjectName('rf4')
        self.rf4_button.setEnabled(False)
        self.rf4_button.clicked.connect(self.button_clicked)

        bottom_layout.addWidget(self.rf1_button)
        bottom_layout.addWidget(self.rf2_button)
        bottom_layout.addWidget(self.rf3_button)
        bottom_layout.addWidget(self.rf4_button)

        merged_layout.addLayout(top_layout)
        merged_layout.addLayout(bottom_layout)
        
        widget = QWidget()
        widget.setLayout(merged_layout)
        self.setCentralWidget(widget)

    def get_ports(self, arg):
        if isinstance(arg, list):
            self.devices.clear()
            for i in self.serial_port.list_of_ports:
                self.devices.addItem(str(i[0]))
            self.devices.setCurrentIndex(0)

    def button_clicked(self):
        sender = self.sender()
        id = sender.objectName()
        if id == 'rf1':
            self.serial_port.write_data('1')
            print("rf1")
        elif id == 'rf2':
            print("rf2")
        elif id == 'rf3':
            print("rf3")
        elif id == 'rf4':
            print("rf4")
        elif id == 'reload':
            self.serial_port.update_list()
            self.get_ports(self.serial_port.list_of_ports)
            print("reload")
        elif id == 'connect':
            if self.serial_port.is_connected == False:
                for i in self.serial_port.list_of_ports:
                    if i[0] == self.devices.currentText():
                        self.serial_port.port = i[1]
                self.serial_port.open_port()
                self.reload_button.setEnabled(False)
                self.rf1_button.setEnabled(True)
                self.rf2_button.setEnabled(True)
                self.rf3_button.setEnabled(True)
                self.rf4_button.setEnabled(True)
                self.connect_button.setText("Disconnect")
            else:
                self.serial_port.close_port()
                self.connect_button.setText("Connect")
                self.reload_button.setEnabled(True)
                self.rf1_button.setEnabled(False)
                self.rf2_button.setEnabled(False)
                self.rf3_button.setEnabled(False)
                self.rf4_button.setEnabled(False)
        

class VirtualCOMPort():
    def __init__(self):
        self.port = None
        self.dev = None
        self.is_connected = False
        self.list_of_ports = list()
        self.update_list()
    def update_list(self):
        self.list_of_ports.clear()
        self.ports = serial.tools.list_ports.comports()
        for p in self.ports:
            self.list_of_ports.append([p.description, p.device, p.pid, p.vid])
        print(self.list_of_ports)
    def open_port(self):
        self.dev = serial.Serial(self.port, baudrate= 115200)
        print(self.dev)
        self.is_connected = True
    def close_port(self):
        if self.dev is not None:
            self.dev.close()
            self.is_connected = False
    def write_data(self, data):
        self.dev.write(bytes(data, 'utf-8'))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    screen_width = 640
    screen_height = 320
    window = MainWindow()
    window.show()
    app.exec()
