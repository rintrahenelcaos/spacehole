import sys
#from random import randint 
#import time
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLCDNumber, QVBoxLayout 
from PyQt5 import QtGui, QtCore 


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.InitIU()
#        self.show()

    def InitIU(self):
        self.lcd = QLCDNumber()
        self.button = QPushButton("Cuenta Regresiva")
        self.button.clicked.connect(self.LCDHander)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.lcd)
        vbox.addWidget(self.button)
        self.setLayout(vbox)
        
        self.timer = QtCore.QTimer(self)                            
        self.timer.timeout.connect(self.showTime)                   
        self.timer.setInterval(500)
        self.time = 60

    def showTime(self):  
        self.lcd.display(self.time)
        self.time -= 1
        if self.time < 0:
            self.timer.stop()

    def LCDHander(self):
        self.time = 60
        self.timer.start()
        
#        for i in range(60):
#            self.lcd.display(i)
#            time.sleep(1)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec_())