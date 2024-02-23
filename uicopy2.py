import functools
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QPushButton,
    QScrollArea,
    QLabel,
    QDialog,
    QGraphicsView,
    QGraphicsScene,
    QFrame,
    QGridLayout,
    
)

from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen, QMouseEvent, QHoverEvent, QFont, QColor,QPalette
from PyQt5.QtCore import Qt, QLine, QPointF, QRectF, QLine, QEvent, QPropertyAnimation, pyqtProperty
import sqlite3
import random
import sys
import time

from control2 import Control
from modules.cards import cardextraction, massiveloader, tableconstructor, tabledropper
from modules.dbcontrol import DBControl, identifierextractor
from modules.phases import DeckMixer, DrawCardPhase, SpaceKarmaPhase, EventPhase, Buildphase, PowerPhase, IncomePhase


class Main_window(QMainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        
        
        
        
        self.conector = sqlite3.connect("currentgame.db")
        self.pointer = self.conector.cursor()
        cardpath = "modules\cards.csv"
        
        
        #tabledropper(self.conector)
        #tableconstructor(self.conector)
        #self.deck = cardextraction(cardpath)
        #massiveloader(self.conector, self.deck)
        self.db = DBControl(self.conector)
        
        self.setObjectName("MainWindow")
        self.resize(1250, 980)
        self.setWindowTitle("MainWindow")
        self.setStyleSheet("QWidget { background-color: black}")
        self.setWindowTitle("SPACEHOLE")
        
        self.control = Control("modules\cards.csv")
        self.counterturn = 0
        
        self.invadersgrid = [[4,10],[4,100],[4,190],[4,280],[4,370],[4,460],[4,550],[4,640],[4,730],[4,820],
                             [94,10],[94,100],[94,190],[94,280],[94,370],[94,460],[94,550],[94,640],[94,730],[94,820]]
        
        self.defendersgrid = [[10,20],[10,120],[10,220],[10,320],[10,420],[10,520],[10,620],[10,720],[10,820],[10,920],[10,1020]]
        
        self.handgrid = [[6,6], [6,116], [116,6], [116,116], [226,6], [226,116], [336,6], [336,116], [446,6], [446,116]]
        
        self.buildgrid = [[2, 108, "Laser_Turret0"],
                          [2, 214, "Laser_Turret1"],
                          [2, 320, "Force_Dome0"],
                          [2, 426, "Laser_Turret2"],
                          [2, 532, "Force_Dome1"],
                          [2, 638, "Laser_Turret3"],
                          [108, 2, "Mine0"],
                          [108, 108, "Solar_Array0"],
                          [108, 214, "Solar_Array1"],
                          [108, 320, "Solar_Array2"],
                          [108, 426, "Solar_Array3"],
                          [108, 532, "Solar_Array4"],
                          [108, 638, "Solar_Array5"],
                          [108, 744, "Solar_Array6"],
                          [108, 850, "Mine1"],
                          [214, 2, "Mine2"],
                          [214, 108, "Agrodome0"],
                          [214, 214, "Starport0"],
                          [214, 320, "Stargate0"],
                          [214, 426, "Research_Labs0"],
                          [214, 532, "Research_Labs1"],
                          [214, 638, "Refinery0"],
                          [214, 744, "Agrodome1"],
                          [214, 850, "Mine3"],
                          [320, 2, "Mine4"],
                          [320, 108, "Agrodome2"],
                          [320, 214, "Colony0"],
                          [320, 320, "Colony1"],
                          [320, 426, "Command_Center0"],
                          [320, 532, "Refinery1"],
                          [320, 638, "Refinery2"],
                          [320, 744, "Agrodome3"],
                          [320, 850, "Mine5"],
                          [426, 2, "Mine6"],
                          [426, 108, "Agrodome4"],
                          [426, 214, "Colony2"],
                          [426, 320, "Colony3"],
                          [426, 426, "Base0"],
                          [426, 532, "Factory0"],
                          [426, 638, "Refinery3"],
                          [426, 744, "Agrodome5"],
                          [426, 850, "Mine7"]]

        self.initUI()
        
    """def conection_sql(self):
        global conector
        conector = sqlite3.connect("currentgame.db")
        return conector  """

    def initUI(self):

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1250, 21))
        self.file_menu = self.menubar.addMenu("Game")
        self.menubar.setStyleSheet("color: white ;background-color: #1E1E1E")

        self.new_game = QtWidgets.QAction(self)
        self.file_menu.addAction(self.new_game)
        self.new_game.setText("New Game")
        self.new_game.triggered.connect(lambda: self.restart())
        
        self.megacredits_label = QLabel(self)
        self.megacredits_label.setGeometry(QtCore.QRect(940, 20 ,150, 15))
        self.megacredits_label.setText("Megacredits: $"+str(self.control.megacredits))
        self.megacredits_label.setStyleSheet("color: lightgreen")
        
        
        
        """self.action_new_map = QtWidgets.QAction()
        self.file_menu.addAction(self.action_new_map)
        self.action_new_map.setText("New Map")
      
        self.action_clear_map = QtWidgets.QAction()
        self.file_menu.addAction(self.action_clear_map)
        self.action_clear_map.setText("Clear Map")"""

        self.info_phase_label = QtWidgets.QLabel(self)
        self.info_phase_label.setGeometry(QtCore.QRect(15, 45, 900, 15))
        self.info_phase_label.setText("Press New Game button or select New Game in menu to start. Your objective is to earn as much megacredits as possible")
        self.info_phase_label.setObjectName("info_phase_label")
        self.info_phase_label.setStyleSheet("color: white")

        self.passturn_button = QPushButton(self)
        self.passturn_button.setGeometry(QtCore.QRect(800, 920, 100, 50))
        self.passturn_button.setStyleSheet("QWidget { background-color: white}")
        self.passturn_button.setText("New Game")
        self.passturn_button.clicked.connect(lambda:self.gameplay())
        self.passturn_button.setShortcut("Space")
        
        

        self.invaders_frame = QFrame(self)
        self.invaders_frame.setGeometry(QtCore.QRect(10, 80, 910, 178))
        self.invaders_frame.setStyleSheet("QWidget { background-color: #1E1E1E}")
        self.invaders_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.invaders_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.invaders_frame.setLineWidth(2)
        
        self.invaders_info = QLabel(self)
        self.invaders_info.setGeometry(QtCore.QRect(15, 65, 900, 10))
        self.invaders_info.setText("Invaders")
        self.invaders_info.setStyleSheet("color: red")
        

        self.information_frame = QFrame(self)
        self.information_frame.setGeometry(QtCore.QRect(930, 40, 310, 218))
        self.information_frame.setStyleSheet("color: white; background-color: #1E1E1E")
        self.information_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.information_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.information_frame.setLineWidth(2)
        
        
        self.info_pict = QtWidgets.QLabel(self.information_frame)
        self.info_pict.setGeometry(QtCore.QRect(10, 10, 110, 110))
        self.info_pict.setPixmap(QtGui.QPixmap(""))
        self.info_pict.setScaledContents(True)
        
        self.cardname_label = QLabel(self.information_frame)
        self.cardname_label.setGeometry(QtCore.QRect(10, 122, 110, 20))
        self.cardname_label.setText("Card: "+"")
        
        self.cardtype_label = QLabel(self.information_frame)
        self.cardtype_label.setGeometry(QtCore.QRect(10, 142, 110, 20))
        self.cardtype_label.setText("Type: "+"")
        
        self.cardforce_label = QLabel(self.information_frame)
        self.cardforce_label.setGeometry(QtCore.QRect(10, 162, 110, 20))
        self.cardforce_label.setText("Force: "+"")
        
        self.cardhits_label = QLabel(self.information_frame)
        self.cardhits_label.setGeometry(QtCore.QRect(10, 182, 110, 20))
        self.cardhits_label.setText("Hits: "+"")
        
        self.cardattr_label = QLabel(self.information_frame)
        self.cardattr_label.setGeometry(QtCore.QRect(130, 10, 180, 110))
        self.cardattr_label.setText("Attr: "+"")
        self.cardattr_label.setAlignment(Qt.AlignTop)
        self.cardattr_label.setWordWrap(True)
        #self.cardattr_label.setStyleSheet("color: white; background-color: blue")
        

        self.defenders_frame = QFrame(self)
        self.defenders_frame.setGeometry(QtCore.QRect(10, 280, 1230, 100))
        self.defenders_frame.setStyleSheet("QWidget { background-color: #1E1E1E}")
        self.defenders_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.defenders_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.defenders_frame.setLineWidth(2)
        
        self.defenders_info = QLabel(self)
        self.defenders_info.setGeometry(QtCore.QRect(15, 265, 900, 10))
        self.defenders_info.setText("Defenders")
        self.defenders_info.setStyleSheet("color: green")

        self.base_frame = QFrame(self)
        self.base_frame.setGeometry(QtCore.QRect(10, 390, 958, 534))
        self.base_frame.setStyleSheet("QWidget { background-color: #1E1E1E}")
        self.base_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.base_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.base_frame.setLineWidth(2)

        self.hand_frame = QFrame(self)
        self.hand_frame.setGeometry(QtCore.QRect(1000, 410, 228, 558))
        self.hand_frame.setStyleSheet("QWidget { background-color: #1E1E1E}")
        self.hand_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.hand_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hand_frame.setLineWidth(2)
        
        
        
        self.hand_info = QLabel(self)
        self.hand_info.setGeometry(QtCore.QRect(1005, 395, 228, 10))
        self.hand_info.setText("Your Hand")
        self.hand_info.setStyleSheet("color: white")
        
        
        self.events_frame = QFrame(self)
        self.events_frame.setGeometry(QtCore.QRect(425, 250, 300, 350))
        self.events_frame.setStyleSheet("QWidget { background-color: gray}") 
        self.events_frame.hide()
        
        self.events_announce =QLabel(self.events_frame)
        self.events_announce.setGeometry(QtCore.QRect(0, 150, 300,10))
        self.events_announce.setText("EVENT")
        self.events_announce.setStyleSheet("color: red")
        self.events_announce.setAlignment(Qt.AlignCenter)
        
        
        
        self.event_pict = QtWidgets.QLabel(self.events_frame)
        self.event_pict.setGeometry(QtCore.QRect(90, 10, 120, 120))
        self.event_pict.setStyleSheet("color: white; background-color: yellow")
        self.event_pict.setPixmap(QtGui.QPixmap(""))
        self.event_pict.setScaledContents(True)
        
        
        self.eventcard_label = QLabel(self.events_frame)
        self.eventcard_label.setGeometry(QtCore.QRect(0, 170, 300, 15))
        self.eventcard_label.setText("Card: "+"")
        self.eventcard_label.setAlignment(Qt.AlignCenter)
        
        self.eventtype_label = QLabel(self.events_frame)
        self.eventtype_label.setGeometry(QtCore.QRect(0, 190, 300, 15))
        self.eventtype_label.setText("Type: "+"")
        self.eventtype_label.setAlignment(Qt.AlignCenter)
        
        
        
        self.eventattr_label = QLabel(self.events_frame)
        self.eventattr_label.setGeometry(QtCore.QRect(20, 220, 260, 80))
        self.eventattr_label.setText("Attr: "+"")
        self.eventattr_label.setAlignment(Qt.AlignTop)
        self.eventattr_label.setWordWrap(True)
        
        self.event_button = QPushButton(self.events_frame)
        self.event_button.setGeometry(QtCore.QRect(90, 300, 120, 40))
        self.event_button.setText("OK")
        self.event_button.clicked.connect(lambda: self.eventok())
        
        self.communication_frame = QFrame(self)
        self.communication_frame.setGeometry(QtCore.QRect(425, 250, 400, 400))
        self.communication_frame.setStyleSheet("QWidget { background-color: gray}")
        self.communication_frame.hide()
        
        self.communication_label = QLabel(self.communication_frame)
        self.communication_label.setText("Base Destroyed")
        self.communication_label.setGeometry(QtCore.QRect(100,50,200,50))
        
        self.communication_label2 = QLabel(self.communication_frame)
        self.communication_label2.setText("DEFEAT")
        self.communication_label2.setGeometry(QtCore.QRect(100,120,200,50))
        
        self.communication_label_mega = QLabel(self.communication_frame)
        self.communication_label_mega.setText("Megacredits = "+str(self.control.megacredits))
        self.communication_label_mega.setGeometry(QtCore.QRect(100,180,200,50))
        
        self.communication_frame_button = QPushButton("Play Again",self.communication_frame)
        self.communication_frame_button.setGeometry(QtCore.QRect(100,280,200,50))
        self.communication_frame_button.clicked.connect(lambda: self.restart())
        
        
        self.building_choose_frame = QFrame(self)
        self.building_choose_frame.setGeometry(QtCore.QRect(425, 250, 400, 200))
        self.building_choose_frame.setStyleSheet("QWidget { background-color: gray}")
        self.building_choose_frame.hide() 
        
        self.building_label = QLabel(self.building_choose_frame)
        self.building_label.setText("Building Phase Options")       
        self.building_label.setGeometry(QtCore.QRect(100,20,200,50))
        
        self.choosing_button = QPushButton(self.building_choose_frame)
        self.choosing_button.setGeometry(QtCore.QRect(60,80,280,50))
        self.choosing_button.setStyleSheet("QWidget { background-color: red}")
        self.choosing_button.show()
        
        self.choosing_button_2 = QPushButton(self.building_choose_frame)
        self.choosing_button_2.setGeometry(QtCore.QRect(60,130,280,50))
        self.choosing_button_2.setStyleSheet("QWidget { background-color: blue}")
        self.choosing_button_2.show()
        
        
        self.happening_label = QLabel(self)
        self.happening_label.setGeometry(QtCore.QRect(10, 930, 790, 20))
        self.happening_label.setText("")
        self.happening_label.setStyleSheet("color: white")
        
        self.timer = QtCore.QTimer(self)
        
        
        
        # layouts and grids
        
        self.cardcreator()
       
        #handgrido(self.hand_frame, self.information_frame)
        #self.genericlabelassigner()
        #
        #buildgrid(self.base_frame, self.information_frame)
        #self.buildingslabelassigner()
        #
        #invadergrid(self.invaders_frame, self.information_frame)
        #self.genericspecificlabelassigner("invader", self.invaders_frame, "red")
        #defendersgrid(self.defenders_frame, self.information_frame)
        #self.genericspecificlabelassigner("defender", self.defenders_frame, "green")
    
    def cardcreator(self):
        deck = identifierextractor(self.db.genericdatabasequery("SELECT id from deck"))
        print(deck)
        for ident in deck:
            pict = self.db.genericdatabasequery("SELECT pict FROM images WHERE id="+str(ident))[0][0]
            name = self.db.cardselector(ident)[0][1]
            print(pict)
            card = LabelFrames(self,0,0,name,self.infoframeshow,"images\\"+pict+".png")
            card.hide()
            
        
            
            
    
    
    
    
     
        
    
    def infoframeshow(self):
        self.information_frame.show()
    def infoframehide(self):
        self.information_frame.hide()
        
    def infoframeshow(self, identif, *args): # <--- Shows information of hoovered card
        
        if identif != "":
            
            self.information_frame.show()
            number = identifierextractor(self.db.invertedcardselector("card",identif))[0]
            pic = self.db.genericdatabasequery("SELECT pict FROM images WHERE id="+str(number))[0][0]
            descript = self.db.genericdatabasequery("SELECT descript FROM images WHERE id="+str(number))[0][0]
            self.info_pict.setPixmap(QtGui.QPixmap("images\\"+pic+".png"))
            self.info_pict.setStyleSheet("background: white")
            card = self.db.cardselector(number)[0]
            
            self.cardname_label.setText("Card: "+card[1])
            self.cardtype_label.setText("Type: "+card[2])
            self.cardforce_label.setText("Force: "+str(card[12]))
            self.cardhits_label.setText("Hits: "+str(card[13]-card[16]))
            self.cardattr_label.setText("Attr: "+descript)
            
        
        else: 
            
            self.information_frame.show()
            self.info_pict.setPixmap(QtGui.QPixmap(""))
            self.info_pict.setStyleSheet("background-color: transparent")
            self.cardname_label.setText("Card: "+"")
            self.cardtype_label.setText("Type: "+"")
            self.cardforce_label.setText("Force: "+"")
            self.cardhits_label.setText("Hits: "+"")
            self.cardattr_label.setText("Attr: "+"")
            
    def handassigner(self):
        handcopy = self.handgrid.copy()
        inhand = identifierextractor(self.db.invertedcardselector("placement", "hand"))
        for pos in range(len(inhand)):
            card = self.db.cardselector(str(inhand[pos]))[0][1]
            position = handcopy[pos]
            
            label = self.findChildren(LabelFrames, card)[0]
            
            label.setParent(self.hand_frame)
            label.ypos = position[0]
            label.xpos = position[1]
            label.setGeometry(QtCore.QRect(position[1], position[0], 106, 106))
            label.show()
            label.setStyleSheet("background-color: white")
    
    def handcleaner(self):
        tocleanhand = self.hand_frame.findChildren(LabelFrames)
        for toclean in  tocleanhand:
            toclean.setParent(self)
            toclean.hide()
            
    def genericassigner(self, referenceframe, referencegrid, placementcode, size, color):
        gridcopy = referencegrid.copy()
        inplace = identifierextractor(self.db.invertedcardselector("placement", placementcode))
        for pos in range(len(inplace)):
            card = self.db.cardselector(str(inplace[pos]))[0][1]   
            position = gridcopy[pos]
            
            label = self.findChildren(LabelFrames, card)[0]
            
            label.setParent(referenceframe)
            label.setGeometry(QtCore.QRect(position[1], position[0], size, size))
            label.show()
            label.setStyleSheet("background-color: "+color)
            
    def genericframecleaner(self, referenceframe):
        tocleanlabels = referenceframe.findChildren(LabelFrames)
        for toclean in tocleanlabels:
            toclean.setParent(self)
            toclean.hide()
            
    def buildassigner(self):
        
        builded = identifierextractor(self.db.invertedcardselector("placement", "builded"))
        
        for building in builded:
            card = self.db.cardselector(building)[0][1]
            label = self.findChildren(LabelFrames, card)[0]
            for pos in self.buildgrid:
                if card == pos[2]:
                    label.setParent(self.base_frame)
                    label.setGeometry(QtCore.QRect(pos[1], pos[0], 106, 106))
                    label.show()
                    label.setStyleSheet("background-color: grey")
    
    def buildcleaner(self):
        toclean = self.base_frame.findChildren(LabelFrames)
        
        for cleanbuild in toclean:
            cleanbuild.setParent(self)
            cleanbuild.hide()
                            
                    
            
    def viewactualizer(self):
        self.handcleaner()
        self.handassigner()
        self.genericframecleaner(self.invaders_frame)
        self.genericassigner(self.invaders_frame, self.invadersgrid, "invader", 80, "red")
        self.genericframecleaner(self.defenders_frame)
        self.genericassigner(self.defenders_frame, self.defendersgrid, "defending", 90, "green")
        self.buildcleaner()
        self.buildassigner()
        
        
        if self.db.cardselector(1)[0][14] == "discard":
            self.communication_label_mega.setText("Megacredits = "+str(self.control.megacredits))
            self.communication_frame.show()
            self.passturn_button.setEnabled(False)
        if len(identifierextractor(self.db.invertedcardselector("placement","deck"))) == 0:
            self.communication_label2.setText("VICTORY")
            self.communication_label.setText("End of game")
            self.communication_label_mega.setText("Megacredits = "+str(self.control.megacredits))
            self.communication_frame.show()
            self.passturn_button.setEnabled(False)
        
    
    # Game Mechanics
    
    
    
    
    def gameplay(self): 
        if self.counterturn == 8: self.counterturn = 1 
        
        if   self.counterturn == 0:  self.startgame()
        elif self.counterturn == 1:  self.drawphasefunction()
        elif self.counterturn == 2:  self.spacekarmaeventsphasefunction()
        elif self.counterturn == 3:  self.battlepreparationfunction()
        elif self.counterturn == 4:  self.battledefendersfunction()
        elif self.counterturn == 5:  self.battlelassersfunction()
        elif self.counterturn == 6:  self.battledomesfunction()
        elif self.counterturn == 7:  self.battlebasefunction()
        
        
        self.viewactualizer()
        self.counterturn += 1
    
    def startgame(self):
        
        self.passturn_button.setText("Next Phase")
        self.passturn_button.setEnabled(True)
        self.control.restarter()
        self.viewactualizer()
        self.communication_frame.hide()
        self.info_phase_label.setText("New game starting")
        self.control.startgame()        
    
    def restart(self):
        self.passturn_button.setText("Start Game")
        self.passturn_button.setEnabled(True)
        self.control.restarter()
        self.viewactualizer()
        self.communication_frame.hide()
        self.info_phase_label.setText("New game starting")
        self.counterturn = 0   
    
    def drawphasefunction(self):
        self.info_phase_label.setText("Drawing Card - Event and Invaders will automatically be played in the next phase")
        self.control.drawphasefunction()
        """
        timer = QtCore.QTimer(self, interval=5 * 1000)
        timer.timeout.connect(self.handle_timeout)
        timer.start()
        
        self.handle_timeout(self.hand_frame)"""
        apply_color_animation(self.hand_frame, QtGui.QColor("white"), QtGui.QColor("#1E1E1E"), duration=2500)
        
        self.timer.setInterval(2500)
        self.timer.start()
        self.timer.timeout.connect(lambda: apply_color_animation(self.hand_frame, QtGui.QColor("white"), QtGui.QColor("#1E1E1E"), duration=2500))
        #timer = QtCore.QTimer(self)
        
    def spacekarmaeventsphasefunction(self):
        self.timer.stop()
        self.info_phase_label.setText("Space Karma Phase - Invaders are played and Events are triggered at this moment")
        
        
        happening = self.control.spacekarmaphasefunction()
        self.happening_label.setText(happening)
        eventsonwait = identifierextractor(self.db.invertedcardselector("placement", "event"))
        if len(eventsonwait) > 0:    
            self.eventphasefunction()
        if len(self.db.invertedcardselector("placement","invader")) == 0:
            self.counterturn = 0 
            
    def eventphasefunction(self):
        #self.info_phase_label.setText("Events Phase")
        eventsonwait = identifierextractor(self.db.invertedcardselector("placement", "event"))
        """if len(self.db.invertedcardselector("placement","invader")) == 0:
            self.counterturn += 5"""
        #else:pass
        if len(eventsonwait) > 0:
            number = eventsonwait[0]
            self.passturn_button.setEnabled(False)
            self.event_pict.setPixmap(QtGui.QPixmap("images\\"+self.db.genericdatabasequery("SELECT pict FROM images WHERE id="+str(number))[0][0]+".png"))
            self.eventcard_label.setText("Card: "+self.db.cardselector(number)[0][1])
            self.eventtype_label.setText("Type: Event")
            self.eventattr_label.setText("Attr: "+self.db.genericdatabasequery("SELECT descript FROM images WHERE id="+str(number))[0][0])
            self.events_frame.show()
            self.happening_label.setText("The event: "+self.db.cardselector(number)[0][1]+" has taken place")
             
        else: self.happening_label.setText("No events happening now") 
        
    def eventok(self):
        self.control.eventphasefunction()
        self.events_frame.hide()
        
        self.passturn_button.setEnabled(True)
        self.passturn_button.setShortcut("Space")
        #self.counterturn -= 2
        self.gameplay()
        
    def battlepreparationfunction(self):
        
        #self.passturn_button.setEnabled(False)
        self.info_phase_label.setText("Battle Preparations Phase")
        happen = self.control.battlepreparationfunction()
        self.happening_label.setText(happen)
        
        """if len(self.db.invertedcardselector("placement","invader")) == 0:
            self.counterturn += 4"""
    
    def battledefendersfunction(self):
        self.info_phase_label.setText("Battle vs Defenders Phase")
        happen = self.control.battledefendersfunction()
        self.happening_label.setText(happen) 
       
    def battlelassersfunction(self):
        self.info_phase_label.setText("Battle vs Lassers Phase")
        happen = self.control.battlelassersfunction()
        self.happening_label.setText(happen) 
    
    def battledomesfunction(self):
        self.info_phase_label.setText("Battle vs Domes Phase")
        happen = self.control.battledomesfunction()
        self.happening_label.setText(happen) 
        
        
    def battlebasefunction(self):
        self.info_phase_label.setText("Battle vs Base Phase")
        happen = self.control.battlebasefunction()
        self.happening_label.setText(happen) 
        #self.viewactualizer()
        #self.passturn_button.setEnabled(True)
        
    def buildphasefunction(self):
        self.info_phase_label.setText("Build Phase - choose either to build or repair. Phase can be pass after choosing")
        
        self.passturn_button.setEnabled(False)
        self.building_choose_frame.show()
        self.choosing_button_2.setText("Build")
        self.choosing_button_2.clicked.connect(lambda: self.buildingbuildphase())
        self.choosing_button.setText("Repair")
        self.choosing_button.clicked.connect(lambda: self.repairinbuilphase())
    
    def buildingbuildphase(self):
        self.info_phase_label.setText("Building: Choose cards in hand to play")
        apply_color_animation(self.hand_frame, QtGui.QColor("white"), QtGui.QColor("#1E1E1E"), duration=2500)
        apply_color_animation(self.base_frame, QtGui.QColor("white"), QtGui.QColor("#1E1E1E"), duration=2500)
        #timer.singleShot(5000)
        self.timer.setInterval(2500)
        self.timer.start()
        self.timer.timeout.connect(lambda: apply_color_animation(self.base_frame, QtGui.QColor("white"), QtGui.QColor("#1E1E1E"), duration=2500))
        
        self.building_choose_frame.hide()
        self.passturn_button.setEnabled(True)
        self.passturn_button.setShortcut("Space")
        
        for label in self.hand_frame.findChildren(LabelFrames):
            label.asociatedfunc = self.building
            self.viewactualizer()
            
    def building(self, ident):
    
        identificator = identifierextractor(self.db.invertedcardselector("card", ident))[0]
        happen = self.control.building(identificator)
        self.happening_label.setText(happen)
        self.viewactualizer()
        self.buildingbuildphase()
         
        
        
def passer(imprimir = "eventopressed"):
    print(imprimir)
        
class LabelFrames(QLabel):
    def __init__(
        self,
        reference_frame,
        ypos,
        xpos,
        identif,
        infoframe,
        icon="",
        width=106,
        height=106,
        color="#1E1E1E",
        asociatedfunc = passer,
        hits = 1,
        force = 0
        
    ):
        QLabel.__init__(self, reference_frame)
        self.reference_frame = reference_frame
        self.ypos = ypos
        self.xpos = xpos
        self.identif = identif
        self.iconp = icon
        self.infoframe = infoframe
        self.asociatedfunc = asociatedfunc
        self.hits = hits
        self.force = force
        

        self.setGeometry(QtCore.QRect(self.xpos, self.ypos, width, height))

        self.setEnabled(True)
        self.setStyleSheet(" color: black ; background-color:" + color + " ; ")
        

        self.setObjectName(self.identif)
        self.raise_()

        self.setMouseTracking(True)
        # self.mouseMoveEvent()
        #self.iconp = QtGui.QIcon(icon)
        self.setPixmap(QtGui.QPixmap(icon))
        self.setScaledContents(True)

        # self.windowTitle.setStyleSheet("color: white")
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
                
        self.button = QPushButton(self)
        self.button.setGeometry(QtCore.QRect(0,0, width,height))
        self.button.setStyleSheet("background-color: transparent")
        self.button.clicked.connect( lambda:returner(self.asociatedfunc(identif)))
        
        self.labelhits = QLabel(str(self.hits), self)
        self.labelhits.setGeometry(QtCore.QRect(10,30, width, 20))
        self.labelhits.setStyleSheet("background-color: transparent; color:red ")
        self.labelhits.hide()
        
        
        self.labelforce = QLabel(str(self.force), self)
        self.labelforce.setGeometry(QtCore.QRect(10,20, width, 20))
        self.labelforce.setStyleSheet("background-color: transparent; color:red ")
        self.labelforce.hide()
        
        
        #self.button.hide()

        # LabelMiniFrames(self)

        # self.infowindow = Infoshower(self.reference_frame, self.xpos, self.ypos, self.identif, 100, 100, "yellow" )
        
        
        
    """def mouseMoveEvent(self, event):
        print ("'Mouse moved!'")"""
        
    

    def enterEvent(self, event):
        #self.infoframe.show()
        self.infoframe(self.identif)

    def leaveEvent(self, event):
        self.infoframe("")
        #self.infoframe(self.identif)

    """def mousePress(self, event):
        super().mousePressEvent(event)
        self.asociatedfunc()"""


     
def returner(asociated):
    return asociated

    
def passer2(*args):
    print("2nd func")
    
def helper_function(widget, color):
    widget.setStyleSheet("background-color: {}".format(color.name()))
    
def apply_color_animation(widget, start_color, end_color, duration=1000, loops=1):
    anim = QtCore.QVariantAnimation(
        widget,
        duration=duration,
        startValue=start_color,
        endValue=end_color,
        loopCount=loops,
    )
    anim.valueChanged.connect(functools.partial(helper_function, widget))
    anim.start(QtCore.QAbstractAnimation.DeleteWhenStopped)






if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    #ui = Main_window("modules\cards.csv")
    ui = Main_window()
    ui.control.startgame()
    #ui.buildactualizer()
    #ui.buildingslabelassigner()
    #ui.tester()
    #uibutton = BuildedFrames(ui.base_frame, 2, 2, "button", ui.information_frame, color="white", icon="..\\images\\agrodome.png")
    #uilabel = LabelFrames(uibutton,0,0,"buttonlabel", ui.information_frame, icon="..\\images\\agrodome.png", color="blue")
    #handgrido(self.hand_frame, self.information_frame)
    #hand_grid(ui.handlayout, ui.hand_frame)
    #add_label(ui.handlayout, hand_grid_positions(),0, "label1", ui.information_frame,color="pink")
    #add_label(ui.handlayout, hand_grid_positions(),1, "label2", ui.information_frame,color="pink")
    
    

    ui.show()

    sys.exit(app.exec_())