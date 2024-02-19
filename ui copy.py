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

from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen, QMouseEvent, QHoverEvent, QFont
from PyQt5.QtCore import Qt, QLine, QPointF, QRectF, QLine, QEvent
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
        
        

        self.invaders_frame = QtWidgets.QFrame(self)
        self.invaders_frame.setGeometry(QtCore.QRect(10, 80, 910, 178))
        self.invaders_frame.setStyleSheet("QWidget { background-color: #1E1E1E}")
        self.invaders_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.invaders_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.invaders_frame.setLineWidth(2)
        
        self.invaders_info = QLabel(self)
        self.invaders_info.setGeometry(QtCore.QRect(15, 65, 900, 10))
        self.invaders_info.setText("Invaders")
        self.invaders_info.setStyleSheet("color: red")
        

        self.information_frame = QtWidgets.QFrame(self)
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
        

        self.defenders_frame = QtWidgets.QFrame(self)
        self.defenders_frame.setGeometry(QtCore.QRect(10, 280, 1230, 100))
        self.defenders_frame.setStyleSheet("QWidget { background-color: #1E1E1E}")
        self.defenders_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.defenders_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.defenders_frame.setLineWidth(2)
        
        self.defenders_info = QLabel(self)
        self.defenders_info.setGeometry(QtCore.QRect(15, 265, 900, 10))
        self.defenders_info.setText("Defenders")
        self.defenders_info.setStyleSheet("color: green")

        self.base_frame = QtWidgets.QFrame(self)
        self.base_frame.setGeometry(QtCore.QRect(10, 390, 958, 534))
        self.base_frame.setStyleSheet("QWidget { background-color: #1E1E1E}")
        self.base_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.base_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.base_frame.setLineWidth(2)

        self.hand_frame = QtWidgets.QFrame(self)
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
        
        
        # layouts and grids
        
       
        handgrido(self.hand_frame, self.information_frame)
        self.genericlabelassigner()
        
        buildgrid(self.base_frame, self.information_frame)
        self.buildingslabelassigner()
        
        invadergrid(self.invaders_frame, self.information_frame)
        self.genericspecificlabelassigner("invader", self.invaders_frame, "red")
        defendersgrid(self.defenders_frame, self.information_frame)
        self.genericspecificlabelassigner("defender", self.defenders_frame, "green")
        
        
    
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
            self.info_pict.setStyleSheet("background-color: white")
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
        inhand = identifierextractor(self.db.invertedcardselector("placement", "hand"))
        dispslot = self.hand_frame.findChildren(BuildedFrames)
        for slot in dispslot:
            listslot = slot.findChildren(LabelFrames)
            for c in listslot:
                c.setEnabled(True)
                c.hide()
        
        for counter in range(len(inhand)):
            card = self.db.cardselector(inhand[counter])[0][1]
            dispslot[counter].findChild(LabelFrames, card).show()
            dispslot[counter].findChild(LabelFrames, card).setEnabled(True)
            
    def otherframesassigner(self, referenceframe, showing):
        playedid = identifierextractor(self.db.invertedcardselector("placement", showing))
        dispslot = referenceframe.findChildren(BuildedFrames)
        for slot in dispslot:
            listslot = slot.findChildren(LabelFrames)
            for c in listslot:
                c.setEnabled(False)
                c.hide()
        for counter in range(len(playedid)):
            card = self.db.cardselector(playedid[counter])[0][1]
            dispslot[counter].findChild(LabelFrames, card).show()
            dispslot[counter].findChild(LabelFrames, card).setEnabled(True)
        
    def randomframeactualizer(self, referenceframe, showing):
        slotlist = [] 
        
        playedid = identifierextractor(self.db.invertedcardselector("placement", showing))
        played = []
        for card in playedid:
            played.append(self.db.cardselector(card)[0][1])
        allslots = referenceframe.findChildren(BuildedFrames)
        dispslots = allslots.copy()
        for slt in allslots:
            labels = slt.findChildren(LabelFrames)
            for visibleok in labels:
                dispcontrol = False
                if visibleok.isVisible():
                    slotlist.append(visibleok.objectName())
                    dispcontrol = True
            if dispcontrol: dispslots.remove(slt)
            else: allslots.remove(slt)

        
                
        slotlist.sort()
        played.sort()
        added = []
        
        added.extend(slotlist)
        added.extend(played)
        tobeadded = [i for i in added if added.count(i)==1]
        
        for i in tobeadded:
            if i in played: # <--- adds card
                print("add",i)
                rndplacing = random.choice(dispslots)
                labels = rndplacing.fincdChildren(LabelFrames)
                for label in labels:
                    if label.objectName() == i:
                        label.setEnabled(True)
                        label.show()
                
                
                
                
            elif i in slotlist: # <--- eliminate those not in db
                print("eliminate",i)
                for slt in allslots:
                    labels = slt.findChildren(LabelFrames)
                    for visibleok in labels:
                        if visibleok.objectName() == i:
                            visibleok.setEnabled(False)
                            visibleok.hide()
                
    def genericlabelassigner(self):
        deck = identifierextractor(self.db.genericdatabasequery("SELECT id FROM deck"))
        
        frames = self.hand_frame.findChildren(BuildedFrames)
        for f in frames:
            for d in deck:
                label = LabelFrames(f, 0,0, self.db.cardselector(d)[0][1],self.infoframeshow, icon="images\\"+self.db.genericdatabasequery("SELECT pict FROM images WHERE id="+str(d))[0][0]+".png",  color="white")
                #label.button.clicked.connect(lambda: passer(label.nroid))
                label.setEnabled(False)
                label.hide()

    def genericspecificlabelassigner(self, specific, reference_frame, color):
        specificdeck = identifierextractor(self.db.invertedcardselector("type",specific))
        
        frames = reference_frame.findChildren(BuildedFrames)
        for f in frames:
            for d in specificdeck:
                label = LabelFrames(f, 0,0, self.db.cardselector(d)[0][1],self.infoframeshow, icon="images\\"+self.db.genericdatabasequery("SELECT pict FROM images WHERE id="+str(d))[0][0]+".png",  color=color, width=80, height=80)
                label.setEnabled(False)
                label.hide()
    
    def buildingslabelassigner(self):
        buildingcards = self.db.filteredaspectcardselector("type", "build", "card")
        buildingcardslist = []
        for card in buildingcards:
            buildingcardslist.append(card[0])
            
        buildingframes = self.base_frame.findChildren(BuildedFrames)
        for bf in buildingframes:
            for bc in buildingcardslist:
                if bf.objectName() == bc:
                    d = identifierextractor(self.db.invertedcardselector("card",bc))[0]
                    icon = self.db.genericdatabasequery("SELECT pict FROM images WHERE id="+str(d))[0][0]
                    print(icon)
                    
                    label = LabelFrames(bf, 0,0,bc, self.infoframeshow,icon="images\\"+self.db.genericdatabasequery("SELECT pict FROM images WHERE id="+str(d))[0][0]+".png", color="grey")
                    label.setEnabled(False)
                    label.hide()
                    label.asociatedfunc = passer2
            
    def buildactualizer(self):
        builded = identifierextractor(self.db.invertedcardselector("placement", "builded"))
        for building in builded:
            card = self.db.cardselector(building)[0][1]
            for frame in self.base_frame.findChildren(BuildedFrames):
                if frame.objectName() == card:
                    label = frame.findChildren(LabelFrames)[0]
                    label.show()
                    label.setEnabled(True)
        discarded = identifierextractor(self.db.invertedcardselector("placement", "discard"))
        for discard in discarded:
            card = self.db.cardselector(discard)[0][1]
            for frame in self.base_frame.findChildren(BuildedFrames):
                if frame.objectName() == card:
                    label = frame.findChildren(LabelFrames)[0]
                    label.hide()
                    label.setEnabled(True)
        indeck = identifierextractor(self.db.invertedcardselector("placement", "deck"))
        for decked in indeck:
            card = self.db.cardselector(decked)[0][1]
            for frame in self.base_frame.findChildren(BuildedFrames):
                if frame.objectName() == card:
                    label = frame.findChildren(LabelFrames)[0]
                    label.hide()
                    label.setEnabled(True)
    
    def viewactualizer(self):
        self.handassigner()
        self.otherframesassigner(self.invaders_frame,"invader")
        self.otherframesassigner(self.defenders_frame,"defending")
        self.buildactualizer() 
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
            
    def startgame(self):
        
        self.passturn_button.setText("Pass Phase")
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
     
                     
    def gameplay(self):
        if self.counterturn == 11: self.counterturn = 1
        
        if   self.counterturn == 0:  self.startgame()
        elif self.counterturn == 1:  self.drawphasefunction()
        elif self.counterturn == 2:  self.spacekarmaeventsphasefunction()
        #elif self.counterturn == 3:  self.eventphasefunction()
        elif self.counterturn == 3:  self.battlepreparationfunction()
        elif self.counterturn == 4:  self.battledefendersfunction()
        elif self.counterturn == 5:  self.battlelassersfunction()
        elif self.counterturn == 6:  self.battledomesfunction()
        elif self.counterturn == 7:  self.battlebasefunction()
        elif self.counterturn == 8:  self.buildphasefunction()
        elif self.counterturn == 9: self.incomephasefunction()
        elif self.counterturn == 10: self.handmaxcleaner()
        self.viewactualizer()
        self.counterturn += 1
        
        
    
        
        
    
    def drawphasefunction(self):
        self.info_phase_label.setText("Drawing Card - Event and Invaders will automatically be played in the next phase")
        self.control.drawphasefunction()
        self.hand_frame.setStyleSheet("background-color: #7c005d")
        
    def spacekarmaphasefunction(self):
        
        self.info_phase_label.setText("Space Karma Phase")
        happening = self.control.spacekarmaphasefunction()
        self.happening_label.setText(happening)
        
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
            
    def spacekarmaeventsphasefunction(self):
        
        self.info_phase_label.setText("Space Karma Phase - Invaders are played and Events are triggered at this moment")
        self.hand_frame.setStyleSheet("background-color: #1E1E1E")
        happening = self.control.spacekarmaphasefunction()
        self.happening_label.setText(happening)
        eventsonwait = identifierextractor(self.db.invertedcardselector("placement", "event"))
        if len(eventsonwait) > 0:    
            self.eventphasefunction()
        if len(self.db.invertedcardselector("placement","invader")) == 0:
            self.counterturn += 5 
        
         
        
        
    
    def eventok(self):
        self.control.eventphasefunction()
        self.events_frame.hide()
        
        self.passturn_button.setEnabled(True)
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
    
    
    def buildphasefunctiontester(self):
        self.info_phase_label.setText("Build Phase 2")
        #self.control.buildphasefunctiontester()
        
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
        self.building_choose_frame.hide()
        self.passturn_button.setEnabled(True)
        for frames in self.hand_frame.findChildren(BuildedFrames):
            for label in frames.findChildren(LabelFrames):
                if label.isVisible():
                    print(label.objectName())
                    label.asociatedfunc = self.building
                    self.viewactualizer()
                    
    def repairinbuilphase(self):
        self.info_phase_label.setText("Repairing: Choose building or Defender to eliminate damge from")
        self.passturn_button.setEnabled(True)
        self.building_choose_frame.hide()
        for frames in self.hand_frame.findChildren(BuildedFrames):
            for label in frames.findChildren(LabelFrames):
                if label.isVisible():
                    label.asociatedfunc = passer
        for frame in self.base_frame.findChildren(BuildedFrames):
            label = frame.findChildren(LabelFrames)[0]
            if label.isVisible(): 
                label.asociatedfunc = self.deletedamage
        for frames in self.defenders_frame.findChildren(BuildedFrames):
            for label in frames.findChildren(LabelFrames): 
                if label.isVisible():
                    label.asociatedfunc = self.deletedamage
        self.viewactualizer()
        
        
        
        
    def buildphasefunctionor(self, passing = False):
        self.info_phase_label.setText("Build Phase")
        for frames in self.hand_frame.findChildren(BuildedFrames):
            for label in frames.findChildren(LabelFrames):
                if label.isVisible():
                    print(label.objectName())
                    label.asociatedfunc = self.building
                    self.viewactualizer()
        if passing == False:
            self.pass_build.setEnabled(True)
        else: self.pass_build.setEnabled(False)
    
    def building(self, ident):
        
        #self.pass_build.setEnabled(False)
        identificator = identifierextractor(self.db.invertedcardselector("card", ident))[0]
        happen = self.control.building(identificator)
        self.happening_label.setText(happen)
        self.viewactualizer()
        self.buildingbuildphase()
        
    def passbuild(self):
        print("passbuild")
        for frames in self.hand_frame.findChildren(BuildedFrames):
            for label in frames.findChildren(LabelFrames):
                if label.isVisible():
                    label.asociatedfunc = passer
        for frame in self.base_frame.findChildren(BuildedFrames):
            label = frame.findChildren(LabelFrames)[0]
            if label.isVisible(): 
                label.asociatedfunc = self.deletedamage
        for frames in self.defenders_frame.findChildren(BuildedFrames):
            for label in frames.findChildren(LabelFrames): 
                if label.isVisible():
                    label.asociatedfunc = self.deletedamage
        self.viewactualizer()
                
    
    def deletedamage(self, ident):
        
        print("deletadamage")
        identificator = identifierextractor(self.db.invertedcardselector("card", ident))[0]
        self.db.tablemodifier(identificator, "hitted", "0")
        self.viewactualizer()
        for frame in self.base_frame.findChildren(BuildedFrames):
            label = frame.findChildren(LabelFrames)[0]
            if label.isVisible(): 
                label.asociatedfunc = passer
        for frames in self.defenders_frame.findChildren(BuildedFrames):
            for label in frames.findChildren(LabelFrames): 
                if label.isVisible():
                    label.asociatedfunc = passer
        self.happening_label.setText("All damage dealt to "+ident+" repaired")
        self.gameplay()
        #self.viewactualizer()
        
        
    def powerphasefunction(self):
        self.info_phase_label.setText("Power Phase")
        self.control.powerphasefunction()
        
    def incomephasefunction(self):
        self.info_phase_label.setText("Income Phase - Megacredits from buildings in play are added")
        #self.pass_build.setEnabled(False)
        for frame in self.base_frame.findChildren(BuildedFrames):
            label = frame.findChildren(LabelFrames)[0]
            if label.isVisible(): 
                label.asociatedfunc = passer
        for frames in self.defenders_frame.findChildren(BuildedFrames):
            for label in frames.findChildren(LabelFrames): 
                if label.isVisible():
                    label.asociatedfunc = passer
        for frames in self.hand_frame.findChildren(BuildedFrames):
            for label in frames.findChildren(LabelFrames):
                if label.isVisible():
                    print(label.objectName())
                    label.asociatedfunc = passer
                    self.viewactualizer()
        self.control.incomephasefunction()
        
            
        
    def handmaxcleaner(self):
        self.info_phase_label.setText("Handclean Phase - excess of cards over the maximun allowed must be discarded")
        
        
        if self.db.cardselector(36)[0][14] == "builded":
            handmax = 7
        else: handmax = 5
        
        inhandcount = len(identifierextractor(self.db.invertedcardselector("placement", "hand")))
        if inhandcount > handmax:
            for frames in self.hand_frame.findChildren(BuildedFrames):
                for label in frames.findChildren(LabelFrames): 
                    if label.isVisible():
                        label.asociatedfunc = self.discardextra
            self.passturn_button.setEnabled(False)
        else: 
            for frames in self.hand_frame.findChildren(BuildedFrames):
                for label in frames.findChildren(LabelFrames): 
                    if label.isVisible():
                        label.asociatedfunc = passer
            self.happening_label.setText("No need to discard")
            self.passturn_button.setEnabled(True)
            
            
            
        """for frames in self.hand_frame.findChildren(BuildedFrames):
            for label in frames.findChildren(LabelFrames): 
                if label.isVisible():
                    inhandcount += 1
        if inhandcount > handmax:
            for frames in self.hand_frame.findChildren(BuildedFrames):
                for label in frames.findChildren(LabelFrames): 
                    if label.isVisible():
                        label.asociatedfunc = self.discardextra
        else: label.asociatedfunc = passer"""
            
            
    def discardextra(self, ident):
        identificator = identifierextractor(self.db.invertedcardselector("card", ident))[0]
        self.db.tablemodifier(identificator, "placement", "discard")
        self.viewactualizer()
        self.handmaxcleaner()
        self.happening_label.setText(ident + " discarded")
                      
                
        
    
        
    
    def tester(self):  
        #self.buildassigner() 
        if self.counterturn == 0:
            self.handassigner()
            self.control.startgame()
            self.viewactualizer()
            
        elif self.counterturn ==1:
            self.viewactualizer()
        
            self.control.tester()
            self.viewactualizer()
        self.counterturn += 1
        if self.counterturn == 2: self.counterturn = 1 
        #self.randomframeactualizer(self.invaders_frame, "invader", self.invadersgrid, color="red")
        #self.randomframeactualizer(self.defenders_frame, "defending", self.defendersgrid, color="green")

def passer(imprimir = "eventopressed"):
    print(imprimir)
    
def passer2(*args):
    print("2nd func")
    

    


class BuildedFrames2(QPushButton):
    def __init__(
        self,
        reference_frame,
        ypos,
        xpos,
        identif,
        infoframe,
        icon=None,
        width=106,
        height=106,
        color="#1E1E1E",
        asociatedfunc=passer,
    ):
        QPushButton.__init__(self, reference_frame)
        self.reference_frame = reference_frame
        self.ypos = ypos
        self.xpos = xpos
        self.identif = identif
        self.iconp = icon
        self.infoframe = infoframe
        self.asociatedfunc = asociatedfunc

        self.setGeometry(QtCore.QRect(self.xpos, self.ypos, width, height))

        self.setCheckable(False)
        self.setAutoExclusive(False)
        self.setDefault(False)
        self.setFlat(True)
        self.setEnabled(True)

        self.setStyleSheet(" color: black ; background-color:" + color + " ; ")

        self.setObjectName(self.identif)
        self.setText(self.identif)

        self.setMouseTracking(True)
        # self.mouseMoveEvent()
        self.iconp = QtGui.QIcon(icon)
        self.setIcon(self.iconp)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def enterEvent(self, event):
        self.infoframe.show()

    def leaveEvent(self, event):
        self.infoframe.hide()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.asociatedfunc(self.objectName())


class BuildedFrames(QFrame):
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
        color="transparent",
        
    ):
        QFrame.__init__(self, reference_frame)
        self.reference_frame = reference_frame
        self.ypos = ypos
        self.xpos = xpos
        self.identif = identif
        self.iconp = icon
        self.infoframe = infoframe
        

        self.setGeometry(QtCore.QRect(self.xpos, self.ypos, width, height))

        self.setEnabled(True)
        self.setStyleSheet(" color: black ; background-color:" + color + " ; ")
        
        self.setObjectName(self.identif)

        self.setMouseTracking(True)
        


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


class LabelMiniFrames(QLabel):
    def __init__(self, containerframe):
        QLabel.__init__(self, containerframe)
        self.setText(containerframe.objectName())
        self.setObjectName("Label" + containerframe.objectName())
        self.setStyleSheet("color: grey")


"""class Infoshower(QFrame):  
    def __init__(self, reference_frame, ypos, xpos, identif, color = "red"):
        QFrame.__init__(self, reference_frame ) 
        
        #self =  QtWidgets.QLabel(self.reference_frame)
        self.setGeometry(QtCore.QRect(xpos+10, ypos+10, 100, 100))
        self.setStyleSheet("background-color: yellow")
        self.raise_()
        self.hide()"""


def buildgrid(reference_frame, infoframe):
    laser0b =  BuildedFrames(reference_frame, 2, 108, "Laser_Turret0", infoframe)
    laser1b =  BuildedFrames(reference_frame, 2, 214, "Laser_Turret1", infoframe)
    dome0b =   BuildedFrames(reference_frame, 2, 320, "Force_Dome0", infoframe)
    laser2b =  BuildedFrames(reference_frame, 2, 426, "Laser_Turret2", infoframe)
    dome1b =   BuildedFrames(reference_frame, 2, 532, "Force_Dome1", infoframe)
    laser3b =  BuildedFrames(reference_frame, 2, 638, "Laser_Turret3", infoframe)
    mine0b =   BuildedFrames(reference_frame, 108, 2, "Mine0", infoframe)
    solar0b =  BuildedFrames(reference_frame, 108, 108, "Solar_Array0", infoframe)
    solar1b =  BuildedFrames(reference_frame, 108, 214, "Solar_Array1", infoframe)
    solar2b =  BuildedFrames(reference_frame, 108, 320, "Solar_Array2", infoframe)
    solar3b =  BuildedFrames(reference_frame, 108, 426, "Solar_Array3", infoframe)
    solar4b =  BuildedFrames(reference_frame, 108, 532, "Solar_Array4", infoframe)
    solar5b =  BuildedFrames(reference_frame, 108, 638, "Solar_Array5", infoframe)
    solar6b =  BuildedFrames(reference_frame, 108, 744, "Solar_Array6", infoframe)
    mine1b =   BuildedFrames(reference_frame, 108, 850, "Mine1", infoframe)
    mine2b =   BuildedFrames(reference_frame, 214, 2, "Mine2", infoframe)
    agro0b =   BuildedFrames(reference_frame, 214, 108, "Agrodome0", infoframe)
    stport0b = BuildedFrames(reference_frame, 214, 214, "Starport0", infoframe)
    stgate0b = BuildedFrames(reference_frame, 214, 320, "Stargate0", infoframe)
    lab0b =    BuildedFrames(reference_frame, 214, 426, "Research_Labs0", infoframe)
    lab1b =    BuildedFrames(reference_frame, 214, 532, "Research_Labs1", infoframe)
    ref0b =    BuildedFrames(reference_frame, 214, 638, "Refinery0", infoframe)
    agro1b =   BuildedFrames(reference_frame, 214, 744, "Agrodome1", infoframe)
    mine3b =   BuildedFrames(reference_frame, 214, 850, "Mine3", infoframe)
    mine4b =   BuildedFrames(reference_frame, 320, 2, "Mine4", infoframe)
    agro2b =   BuildedFrames(reference_frame, 320, 108, "Agrodome2", infoframe)
    col0b =    BuildedFrames(reference_frame, 320, 214, "Colony0", infoframe)
    col1b =    BuildedFrames(reference_frame, 320, 320, "Colony1", infoframe)
    comm0b =   BuildedFrames(reference_frame, 320, 426, "Command_Center0", infoframe)
    ref1b =    BuildedFrames(reference_frame, 320, 532, "Refinery1", infoframe)
    ref2b =    BuildedFrames(reference_frame, 320, 638, "Refinery2", infoframe)
    agro3b =   BuildedFrames(reference_frame, 320, 744, "Agrodome3", infoframe)
    mine5b =   BuildedFrames(reference_frame, 320, 850, "Mine5", infoframe)
    mine6b =   BuildedFrames(reference_frame, 426, 2, "Mine6", infoframe)
    agro4b =   BuildedFrames(reference_frame, 426, 108, "Agrodome4", infoframe)
    col2b =    BuildedFrames(reference_frame, 426, 214, "Colony2", infoframe)
    col3b =    BuildedFrames(reference_frame, 426, 320, "Colony3", infoframe)
    base0b =   BuildedFrames(reference_frame, 426, 426, "Base0", infoframe)
    fact0b =   BuildedFrames(reference_frame, 426, 532, "Factory0", infoframe)
    ref3b =    BuildedFrames(reference_frame, 426, 638, "Refinery3", infoframe)
    agro5b =   BuildedFrames(reference_frame, 426, 744, "Agrodome5", infoframe)
    mine7b =   BuildedFrames(reference_frame, 426, 850, "Mine7", infoframe)


def invadergrid(reference_frame, infoframe):
    for i in range(10):
        posleft = 10 + i * 90
        for j in range(2):
            postop = 4 + j * 90

            BuildedFrames(
                reference_frame,
                postop,
                posleft,
                "empty",
                infoframe,
                width=80,
                height=80,
                color= "#1E1E1E"
            )


def defendersgrid(reference_frame, infoframe):
    for i in range(12):
        posleft = 20 + i * 100

        postop = 6

        BuildedFrames(
            reference_frame, postop, posleft, "empty", infoframe, width=90, height=90, color="#1E1E1E"
        )

def handgrid(reference_frame):
    ypos = 0
    for j in range(4):
        xpos = j
        addlabel(reference_frame,xpos,ypos,"hand", color="white",icon="test.png")
    

def handgrido(reference_frame, infoframe):
    """for i in range(2):
    posleft = 6+i*110
    for j in range(5):
        postop = 6+j*110

        BuildedFrames(reference_frame, postop, posleft, "hand", infoframe, width=106, height=106)"""

    posleft = 6
    for j in range(5):
        postop = 6 + j * 110
        
        
        BuildedFrames(reference_frame, postop, posleft, "hand", infoframe, width=106, height=106)
        
    posleft = 116
    for j in range(4):
        postop = 6 + j * 110
        
        

        BuildedFrames(reference_frame, postop, posleft, "hand", infoframe, width=106, height=106)
        
def hand_grid(reference_frame, father_reference_frame):
    """indicators = ["0,0", "1,0",
                      "0,1", "1,1",
                      "0,2", "1,2",
                      "0,3", "1,3",
                      "0,4", "1,4"]"""
        
    positions = [(i, j) for i in range(5) for j in range(2)]
    print("positions: ", positions)
    
    
    for position in positions:
        print(position)
        
        addlabel(reference_frame, int(position[0]),int(position[1]),str(position), color= "white")
        
def hand_grid_positions():
    """indicators = ["0", "5",
                      "1", "6",
                      "2", "7",
                      "3", "8",
                      "4", "9"]"""
        
    positions = [(i, j) for i in range(5) for j in range(2)]
    
    return positions

def add_label(reference_frame, positions, pos, identif,infoframe = None,icon="test.png",width=106,height=106, color="#1E1E1E",asociatedfunc =passer):
    label = QLabel()
    
    label.setEnabled(True)
    label.setStyleSheet(" color: black ; background-color:" + color + " ; ")
    label.setPixmap(QtGui.QPixmap(icon))
    label.setScaledContents(True)
    label.setObjectName(identif)
    xpos, ypos = positions[pos]
    
    reference_frame.addWidget(label, xpos, ypos)


def addlabel(reference_frame,xpos,ypos,identif,infoframe = None,icon="test.png",width=106,height=106, color="#1E1E1E",asociatedfunc =passer):
    label = QLabel()
    
    label.setEnabled(True)
    label.setStyleSheet(" color: black ; background-color:" + color + " ; ")
    label.setPixmap(QtGui.QPixmap(icon))
    label.setScaledContents(True)
    label.setObjectName(identif)
    
    reference_frame.addWidget(label, xpos, ypos)

class Selectionbutton:
    def __init__(
        self, reference_button, xpos, ypos, identif, height, width, color, icon=None
    ):

        self.pushButton = QPushButton(reference_button)
        self.pushButton.setGeometry(QtCore.QRect(xpos, ypos, width, height))
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoExclusive(True)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setEnabled(True)
        self.pushButton.setStyleSheet(
            " color: black ; background-color: " + color + ";"
        )
        self.pushButton.setText(identif)
        self.pushButton.setObjectName(identif)
        self.icon = QtGui.QIcon(icon)

        self.pushButton.setIcon(self.icon)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))



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
