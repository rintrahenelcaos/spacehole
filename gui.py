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
    
    """Game by itself
    """
    
    def __init__(self):
        super(Main_window, self).__init__()
        
        
        
        
        self.conector = sqlite3.connect("currentgame.db")
        self.pointer = self.conector.cursor()
        cardpath = "modules\cards.csv"
        
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
        
        self.defendersgrid = [[6,20],[6,120],[6,220],[6,320],[6,420],[6,520],[6,620],[6,720],[6,820],[6,920],[6,1020]]
        
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
        
    

    def initUI(self):

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1250, 21))
        self.file_menu = self.menubar.addMenu("Game")
        self.menubar.setStyleSheet("color: white ;background-color: #1E1E1E")

        self.new_game = QtWidgets.QAction(self)
        self.file_menu.addAction(self.new_game)
        self.new_game.setText("New Game")
        self.new_game.triggered.connect(lambda: self.restart())
        
        # Indicates Score
        self.megacredits_label = QLabel(self)
        self.megacredits_label.setGeometry(QtCore.QRect(940, 20 ,150, 15))
        self.megacredits_label.setText("Megacredits: $"+str(self.control.megacredits))
        self.megacredits_label.setStyleSheet("color: lightgreen")
        
        # Shows information on current game phase and what's happening
        self.info_phase_label = QtWidgets.QLabel(self)
        self.info_phase_label.setGeometry(QtCore.QRect(15, 45, 900, 15))
        self.info_phase_label.setText("Press New Game button or select New Game in menu to start. Your objective is to earn as much megacredits as possible.")
        self.info_phase_label.setObjectName("info_phase_label")
        self.info_phase_label.setStyleSheet("color: white")
        
        # Phase Passer to allow gameplay
        self.passturn_button = QPushButton(self)
        self.passturn_button.setGeometry(QtCore.QRect(800, 920, 100, 50))
        self.passturn_button.setStyleSheet("QWidget { background-color: white}")
        self.passturn_button.setText("New Game")
        self.passturn_button.clicked.connect(lambda:self.gameplay())
        self.passturn_button.setShortcut("Space")
        
        # Where the invaders go
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
        
        # Shows information on hoovered card 
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
        
        # Where defenders go
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
        
        # Where the base is displayed
        self.base_frame = QFrame(self)
        self.base_frame.setGeometry(QtCore.QRect(10, 390, 958, 534))
        self.base_frame.setStyleSheet("QWidget { background-color: #1E1E1E}")
        self.base_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.base_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.base_frame.setLineWidth(2)
        
        # Cards in hand to be played
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
        
        # Shows information on the current event
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
        
        # End gamne communication
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
        
        # Building Phase options
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
        
        # Shows what had happenned
        self.happening_label = QLabel(self)
        self.happening_label.setGeometry(QtCore.QRect(10, 930, 790, 20))
        self.happening_label.setText("")
        self.happening_label.setStyleSheet("color: white")
        
        
        
        # layouts and grids
        
        self.cardcreator()
       
        
    
    def cardcreator(self):
        """Creates the cards as labels
        """
        
        deck = identifierextractor(self.db.genericdatabasequery("SELECT id from deck"))
        
        for ident in deck:
            pict = self.db.genericdatabasequery("SELECT pict FROM images WHERE id="+str(ident))[0][0]
            name = self.db.cardselector(ident)[0][1]
            
            card = LabelFrames(self,0,0,name,self.infoframeshow,"images\\"+pict+".png")
            card.hide()
            
            
    def infoframeshow(self, identif, *args): # <--- Shows information of hoovered card
        """_summary_

        Args:
            identif (str): card name
        """
        
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
        """Assigns cards to hand from db
        """
        
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
        """Clears the hand to keep it actualized
        """
        
        tocleanhand = self.hand_frame.findChildren(LabelFrames)
        for toclean in  tocleanhand:
            toclean.setParent(self)
            toclean.hide()
            
    def genericassigner(self, referenceframe, referencegrid, placementcode, size, color):
        """generic function to assign cards to frames

        Args:
            referenceframe (QFrame): Frame to assign
            referencegrid (list): grid of positions to place cards
            placementcode (str): value in db "placement"
            size (int): size of card in frame
            color (str): rgb or color
        """
        
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
        """Clears the frame to keep it actualized

        Args:
            referenceframe (QFrame): target frame
        """
        
        tocleanlabels = referenceframe.findChildren(LabelFrames)
        for toclean in tocleanlabels:
            toclean.setParent(self)
            toclean.hide()
            
    def buildassigner(self):
        """Assigns cards to the base frame
        """
        
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
        """Clears the base to keep it actualized
        """
        
        toclean = self.base_frame.findChildren(LabelFrames)
        
        for cleanbuild in toclean:
            cleanbuild.setParent(self)
            cleanbuild.hide()
                            
                    
            
    def viewactualizer(self):
        """Actualizes the ui
        """
        
        self.handcleaner()
        self.handassigner()
        self.genericframecleaner(self.invaders_frame)
        self.genericassigner(self.invaders_frame, self.invadersgrid, "invader", 80, "red")
        self.genericframecleaner(self.defenders_frame)
        self.genericassigner(self.defenders_frame, self.defendersgrid, "defending", 90, "green")
        self.buildcleaner()
        self.buildassigner()
        self.megacredits_label.setText("Megacredits: $"+str(self.control.megacredits))
        
        
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
        """Sequential function for game phases
        """
        
        if self.counterturn == 11: self.counterturn = 1 
        
        if   self.counterturn == 0:  self.startgame()
        elif self.counterturn == 1:  self.drawphasefunction()
        elif self.counterturn == 2:  self.spacekarmaeventsphasefunction()
        elif self.counterturn == 3:  self.battlepreparationfunction()
        elif self.counterturn == 4:  self.battledefendersfunction()
        elif self.counterturn == 5:  self.battlelassersfunction()
        elif self.counterturn == 6:  self.battledomesfunction()
        elif self.counterturn == 7:  self.battlebasefunction()
        elif self.counterturn == 8:  self.buildphasefunction()
        elif self.counterturn == 9:  self.incomephasefunction()
        elif self.counterturn == 10: self.handmaxcleaner()
        
        self.viewactualizer()
        self.counterturn += 1
    
    def startgame(self):
        """Game starting function
        """
        
        self.passturn_button.setText("Next Phase")
        self.passturn_button.setEnabled(True)
        self.control.restarter()
        self.viewactualizer()
        self.communication_frame.hide()
        self.info_phase_label.setText("New game starting")
        self.control.startgame()        
    
    def restart(self):
        """Game restarting function
        """
        self.passturn_button.setText("Start Game")
        self.passturn_button.setEnabled(True)
        self.control.restarter()
        self.viewactualizer()
        self.communication_frame.hide()
        self.info_phase_label.setText("New game starting")
        self.counterturn = 0   
    
    def drawphasefunction(self):
        """Draw cards
        """
        
        self.info_phase_label.setText("Drawing Card - Event and Invaders will automatically be played in the next phase")
        self.control.drawphasefunction()
        
        apply_color_animation(self.hand_frame, QtGui.QColor("dimgray"), QtGui.QColor("#1E1E1E"), duration=2500)
        
        
        
        
    def spacekarmaeventsphasefunction(self):
        """Compose function to autoplay events and invaders. Jumps to build phase if further actions are not needed
        """
        
        self.info_phase_label.setText("Space Karma Phase - Invaders are played and Events are triggered at this moment")
        
        
        happening = self.control.spacekarmaphasefunction()
        self.happening_label.setText(happening)
        eventsonwait = identifierextractor(self.db.invertedcardselector("placement", "event"))
        if len(eventsonwait) > 0:    
            self.eventphasefunction()
        if len(self.db.invertedcardselector("placement","invader")) == 0:
            self.counterturn = 7 
            
    def eventphasefunction(self):
        """Previously used as phase in itself, calls the event window and launches the events
        """
        
        eventsonwait = identifierextractor(self.db.invertedcardselector("placement", "event"))
        
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
        """ Events launcher 
        """
        
        self.control.eventphasefunction()
        self.events_frame.hide()
        
        self.passturn_button.setEnabled(True)
        self.passturn_button.setShortcut("Space")
        
        self.gameplay()
        
    def battlepreparationfunction(self):
        """ If invaders are in game this is called. 
        """
        
        self.passturn_button.setEnabled(False)
        
        self.info_phase_label.setText("Battle Preparations Phase")
        happen = self.control.battlepreparationfunction()
        self.happening_label.setText(happen)
        
        apply_color_animation(self.invaders_frame, QtGui.QColor("darkred"), QtGui.QColor("#1E1E1E"), duration=1000, loops=2)
        waiter = QtCore.QTimer()
        waiter.singleShot(1000, self.passturn_button_unblocker)
        
        
    
    def battledefendersfunction(self):
        
        """ Invaders attack defenders
        """
        
        
        self.passturn_button.setEnabled(False)
        self.info_phase_label.setText("Battle vs Defenders Phase")
        apply_color_animation(self.defenders_frame, QtGui.QColor("darkgreen"), QtGui.QColor("#1E1E1E"), duration=1000)
        apply_color_animation(self.invaders_frame, QtGui.QColor("darkred"), QtGui.QColor("#1E1E1E"), duration=1000)
        happen, damagetodefenders, damagetoinvaders = self.control.battledefendersfunction()
        waiter = QtCore.QTimer()
        waiter.singleShot(1000,lambda: self.battleressulttwosides(happen, damagetodefenders, damagetoinvaders, self.defenders_frame))
        
        
    def battlelassersfunction(self):
        """ Invaders fight lasser turrets
        """
        
        
        self.passturn_button.setEnabled(False)
        self.info_phase_label.setText("Battle vs Lassers Phase")
        apply_color_animation(self.base_frame, QtGui.QColor("darkgreen"), QtGui.QColor("#1E1E1E"), duration=1000)
        apply_color_animation(self.invaders_frame, QtGui.QColor("darkred"), QtGui.QColor("#1E1E1E"), duration=1000)
        happen, damagetolassers, damagetoinvaders= self.control.battlelassersfunction()
        
        waiter = QtCore.QTimer()
        waiter.singleShot(1000,lambda: self.battleressulttwosides(happen, damagetolassers, damagetoinvaders, self.base_frame)) 
    
    def battledomesfunction(self):
        """Invaders hit domes
        """
        
        self.passturn_button.setEnabled(False)
        self.info_phase_label.setText("Battle vs Domes Phase")
        apply_color_animation(self.base_frame, QtGui.QColor("darkgreen"), QtGui.QColor("#1E1E1E"), duration=1000)
        apply_color_animation(self.invaders_frame, QtGui.QColor("darkred"), QtGui.QColor("#1E1E1E"), duration=1000)
        happen, damagetodomes = self.control.battledomesfunction()
        
        waiter = QtCore.QTimer()
        waiter.singleShot(1000,lambda: self.battleressultonesided(happen, damagetodomes, self.base_frame))
        
        
    def battlebasefunction(self):
        """Invaders hit base
        """
        
        self.passturn_button.setEnabled(False)
        self.info_phase_label.setText("Battle vs Base Phase")
        apply_color_animation(self.base_frame, QtGui.QColor("darkgreen"), QtGui.QColor("#1E1E1E"), duration=1000)
        apply_color_animation(self.invaders_frame, QtGui.QColor("darkred"), QtGui.QColor("#1E1E1E"), duration=1000)
        happen, damagetobase = self.control.battlebasefunction()
        
        waiter = QtCore.QTimer()
        waiter.singleShot(1000,lambda: self.battleressultonesided(happen, damagetobase, self.base_frame))
        
        
    
    def passturn_button_unblocker(self):
        """ Enables passturn_button after battle animations
        """
        self.passturn_button.setEnabled(True)
        
    def battleressulttwosides(self, happen, damagetodefenders, damagetoinvaders, defendersframe):
        """ Shows battle results if there are two sides dealing damage

        Args:
            happen (str): description of battle results
            damagetodefenders (int): amount of hits dealt to the defending side
            damagetoinvaders (int): amount of hits dealt to the atacking side
            defendersframe (QFrame): frame indicating who are defending
        """


        self.happening_label.setText(happen)
    
        for d in range(damagetodefenders):
            apply_color_animation(defendersframe, QtGui.QColor("white"), QtGui.QColor("#1E1E1E"), duration=800, loops=1)
            
        for d in range(damagetoinvaders):
            apply_color_animation(self.invaders_frame, QtGui.QColor("white"), QtGui.QColor("#1E1E1E"), duration=800, loops=1)
            
        self.passturn_button_unblocker()
    
    def battleressultonesided(self,happen,damagetodefenders, defendersframe):
        """Shows battle results if there is only one side dealing damage

        Args:
            happen (str): description of battle results
            damagetodefenders (int): amount of hits dealt to the defending side
            defendersframe (QFrame): frame indicating who are defending
        """
        
        
        self.happening_label.setText(happen)
    
        for d in range(damagetodefenders):
            apply_color_animation(defendersframe, QtGui.QColor("white"), QtGui.QColor("#1E1E1E"), duration=800, loops=1)
        
        self.passturn_button_unblocker()
        
        
    def buildphasefunction(self):
        """Function to decide what to do in build phase
        """
        
        self.info_phase_label.setText("Build Phase - choose either to build or repair. Phase can be pass after choosing")
        
        self.passturn_button.setEnabled(False)
        self.building_choose_frame.show()
        self.choosing_button_2.setText("Build")
        self.choosing_button_2.clicked.connect(lambda: self.buildingbuildphase())
        self.choosing_button.setText("Repair")
        self.choosing_button.clicked.connect(lambda: self.repairinbuilphase())
    
    def buildingbuildphase(self):
        """If build is chosed, this is called in order to play cards in hand
        """
        
        self.info_phase_label.setText("Building: Choose cards in hand to play")
        apply_color_animation(self.hand_frame, QtGui.QColor("dimgray"), QtGui.QColor("#1E1E1E"), duration=2000)
        waiter = QtCore.QTimer()
        waiter.singleShot(1500, self.doublecoloranimation)
        
        self.building_choose_frame.hide()
        self.passturn_button.setEnabled(True)
        self.passturn_button.setShortcut("Space")
        
        for label in self.hand_frame.findChildren(LabelFrames):
            label.asociatedfunc = self.building
            self.viewactualizer()
    
    def doublecoloranimation(self):
        """Function necessary to highlight two frames at the same time
        """
        
        apply_color_animation(self.base_frame, QtGui.QColor("darkgreen"), QtGui.QColor("#1E1E1E"), duration=2000)
        apply_color_animation(self.defenders_frame, QtGui.QColor("darkgreen"), QtGui.QColor("#1E1E1E"), duration=2000)
        
            
    def building(self, ident):
        """ Play cards function

        Args:
            ident (str): card name to be played
        """
    
        identificator = identifierextractor(self.db.invertedcardselector("card", ident))[0]
        happen = self.control.building(identificator)
        self.happening_label.setText(happen)
        self.viewactualizer()
        self.buildingbuildphase()
        
    def repairinbuilphase(self):
        """ If repair is chosed, this is called in order to repair cards in play
        """
        
        self.info_phase_label.setText("Repairing: Choose building or Defender to eliminate damge from")
        self.passturn_button.setEnabled(True)
        self.passturn_button.setShortcut("Space")
        self.building_choose_frame.hide()
        
        apply_color_animation(self.base_frame, QtGui.QColor("dimgray"), QtGui.QColor("#1E1E1E"), duration=2000)
        
        
        for label in self.hand_frame.findChildren(LabelFrames):
            label.asociatedfunc = passer
        
        for built in self.base_frame.findChildren(LabelFrames):
            
            built.asociatedfunc = self.deletedamage
            
            
        for defender in self.defenders_frame.findChildren(LabelFrames):
            defender.asociatedfunc = self.deletedamage
        
        self.viewactualizer()
    
    def deletedamage(self, ident):
        """ Function to eliminate damage from selected card

        Args:
            ident (str): card name to be repaired
        """
        
        
        identificator = identifierextractor(self.db.invertedcardselector("card", ident))[0]
        self.db.tablemodifier(identificator, "hitted", "0")
        self.viewactualizer()
        
        for built in self.base_frame.findChildren(LabelFrames):
            built.asociatedfunc = passer
            
        for defender in self.defenders_frame.findChildren(LabelFrames):
            defender.asociatedfunc = passer
        
        self.happening_label.setText("All damage dealt to "+ident+" repaired")
        self.gameplay()
        
        
    def incomephasefunction(self):
        """Function to calculate megacredits(score)
        """
        
        self.info_phase_label.setText("Income Phase - Megacredits from buildings in play are added")
        
        
        for built in self.base_frame.findChildren(LabelFrames):
            built.asociatedfunc = passer
        
        for defender in self.defenders_frame.findChildren(LabelFrames):
            defender.asociatedfunc = passer
            
        for label in self.hand_frame.findChildren(LabelFrames):
            label.asociatedfunc = passer
        
        self.control.incomephasefunction()
    
    def handmaxcleaner(self):
        """Function to decide if discard is necesary
        """
        
        self.info_phase_label.setText("Handclean Phase - excess of cards over the maximun allowed must be discarded")
        
        
        if self.db.cardselector(36)[0][14] == "builded":
            handmax = 7
        else: handmax = 5
        
        inhandcount = len(identifierextractor(self.db.invertedcardselector("placement", "hand")))
        if inhandcount > handmax:
            
            for label in self.hand_frame.findChildren(LabelFrames):
                label.asociatedfunc = self.discardextra
            self.passturn_button.setEnabled(False) 
            self.happening_label.setText("Number of cards in hand excedes the maximun allowed, choose card to discard")
               
            
        else: 
            
            for label in self.hand_frame.findChildren(LabelFrames):
                label.asociatedfunc = passer
            self.happening_label.setText("No need to discard")
            self.passturn_button.setEnabled(True)
    
    def discardextra(self, ident):
        """ Chosen card is discarded

        Args:
            ident (str): card name
        """
        
        identificator = identifierextractor(self.db.invertedcardselector("card", ident))[0]
        self.db.tablemodifier(identificator, "placement", "discard")
        self.viewactualizer()
        self.happening_label.setText(ident + " discarded")
        self.handmaxcleaner()
        
                
            
         
        
        
def passer(imprimir = "eventopressed"):
    """Dummy function

    Args:
        imprimir (str, optional): card name. Defaults to "eventopressed".
    """
    #print(imprimir)
    pass
        
class LabelFrames(QLabel):
    """Base class to create each card

    
    """
    
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
        
        self.setPixmap(QtGui.QPixmap(icon))
        self.setScaledContents(True)

        
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
    

    def enterEvent(self, event):
        
        self.infoframe(self.identif)

    def leaveEvent(self, event):
        self.infoframe("")
       

    


     
def returner(asociated):
    """Dummy function"""
    return asociated

    
def passer2(*args):
    print("2nd func")
    
def helper_function(widget, color):
    """ Allows color change

    Args:
        widget (Qwidget): Target widget
        color (str): colour code
    """
    widget.setStyleSheet("background-color: {}".format(color.name()))
    
def apply_color_animation(widget, start_color, end_color, duration=1000, loops=1):
    """ Function to indicate what to do via colors

    Args:
        widget (QWidget): target widget
        start_color (str): initial color
        end_color (str): end color, usually original one
        duration (int, optional): transition duration. Defaults to 1000.
        loops (int, optional): number of transitions. Defaults to 1.
    """
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
    
    ui = Main_window()
    ui.control.startgame()
    
    
    

    ui.show()

    sys.exit(app.exec_())