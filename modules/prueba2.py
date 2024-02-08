from PyQt5 import QtWidgets, QtCore,QtGui
import sys
import sqlite3
import random

from cards import cardextraction, massiveloader, tableconstructor, tabledropper
from dbcontrol import DBControl, identifierextractor
from ui import Main_window, LabelFrames, add_label, hand_grid,hand_grid_positions

from phases import DeckMixer, DrawCardPhase, SpaceKarmaPhase, EventPhase, Buildphase, PowerPhase, IncomePhase



app = QtWidgets.QApplication(sys.argv)
ui = Main_window()
button=QtWidgets.QPushButton(ui.hand_frame)
button.setGeometry(QtCore.QRect(100,200,30,30))
button.clicked.connect(lambda:gameplay)

def gameplay():
    hand_grid(ui.handlayout, ui.hand_frame)
    add_label(ui.handlayout, hand_grid_positions(),0, "label1", ui.information_frame,color="pink")
    add_label(ui.handlayout, hand_grid_positions(),1, "label2", ui.information_frame,color="pink")

"""def gameplay(frame = ui.hand_frame):
    frame.hide()
    LabelFrames(frame,0, 0 ,"placing", ui.information_frame, color="red") 
    frame.show()"""




ui.show()
    

    
    


    

sys.exit(app.exec_())