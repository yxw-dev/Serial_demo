from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Ui import *
from threading import Thread
from socket import *
import sys
import time
import binascii
import serial
import  serial.tools.list_ports
from queue import Queue,LifoQueue,PriorityQueue

class MyMainWindow(QMainWindow , Ui_MainWindow , QObject):
    def __init__(self ):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)
        self.AddItem_com()
        self.com = serial.Serial
        self.readflag = False
        self.pushButton.clicked.connect(self.connect)
        self.pushButton_send.clicked.connect(self.send_order)
        self.get_single.connect(self.recv)

    def AddItem_com(self):
        port_list = list(serial.tools.list_ports.comports())
        self.comboBox_2.addItems(['2400','4800','9600','19200','38400','57600','115200'])
        self.comboBox_3.addItems(['5' , '6' , '7' , '8'])
        self.comboBox_4.addItems(['None'])
        self.comboBox_2.setCurrentIndex(2)
        self.comboBox_3.setCurrentIndex(3)
        self.comboBox_4.setCurrentIndex(0)
        if len(port_list) != 0:
            for i in range(0, len(port_list)):
                self.comboBox.addItem(str(port_list[i])[0:4])
    def connect(self):
        if (self.pushButton.text() == "断开"):
            self.pushButton.setText('连接')
            self.pushButton_send.setEnabled(False)
            self.readflag = False
            self.com.close()
            self.textEdit.append("断开成功")
            return
        try:
            self.com = serial.Serial(str(self.comboBox.currentText()), int(self.comboBox_2.currentText()))
            if (self.com.isOpen() == True):
                self.readflag = True
                self.pushButton_send.setEnabled(True)
                self.textEdit.append("连接成功")
                self.pushButton.setText('断开')
                read = Thread(target=self.get_date)
                read.start()
            else:
                self.textEdit.appendPlainText("连接失败")
        except Exception as e:
            self.textEdit.append(str(e))

    def send_order(self):
        #字符串发送
        if(self.checkBox.isChecked()):
            if (self.com.isOpen() == True):
                t = '\b\r' + self.textEdit_2.toPlainText() +'\n'
                send_bytes = self.com.write(t.encode('utf-8'))
                self.textEdit.append("<font color=\"#FF0000\">{}</font> ".format(self.textEdit_2.toPlainText()))
            else:
                self.textEdit.appendPlainText('先连接串口')
        #十六进制发送
        else:
            if (self.com.isOpen() == True):
                self.textEdit.append("<font color=\"#FF0000\">{}</font> ".format(self.textEdit_2.toPlainText()))
                text = self.textEdit_2.toPlainText().replace(' ' , '')
                text = text.replace('\n' , '')
                t = binascii.unhexlify(str.encode(text))
                send_bytes = self.com.write(t)
            else:
                self.textEdit.append("<font color=\"#FF0000\">{}</font> ".format(self.textEdit_2.toPlainText()))

    get_single = pyqtSignal(str)

    def get_date(self):
        time.sleep(0.5)
        while self.readflag:
            if self.com.inWaiting():
                try:
                    data = self.com.read_all()
                    self.get_single.emit(str(data.hex()))
                except Exception as e:
                    print(str(e))
    def recv(self , text):
        self.textEdit.append("<font color=\"#00ff00\">{}</font> ".format(text))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyMainWindow()
    win.show()
    sys.exit(app.exec_())