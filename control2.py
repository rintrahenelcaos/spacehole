from PyQt5 import QtWidgets, QtCore,QtGui
import sys
import sqlite3
import random

from modules.cards import cardextraction, massiveloader, tableconstructor, tabledropper
from modules.dbcontrol import DBControl, identifierextractor
#from ui import Main_window, LabelFrames, add_label, hand_grid,hand_grid_positions

from modules.phases import DeckMixer, DrawCardPhase, SpaceKarmaPhase, EventPhase, BattlePhase,Buildphase, PowerPhase, IncomePhase


class Control(DBControl):
    def __init__(self, cardpath):
        
        #self.ui = Main_window()
        self.cardpath = cardpath
        self.conector = self.conection_sql()
        self.pointer = self.conector.cursor()
        tabledropper(self.conector)
        tableconstructor(self.conector)
        self.deck = cardextraction(cardpath)
        massiveloader(self.conector, self.deck)
        self.turnlist = [DrawCardPhase, SpaceKarmaPhase, EventPhase, Buildphase, PowerPhase, IncomePhase]
        self.megacredits = 0
        self.phasecounter = 0
        #self.ui.passturn_button.clicked.connect(lambda:self.gameplay())
        #self.ui.show()
        #self.startgame()
        self.invadersgrid = [[4,10],[4,100],[4,190],[4,280],[4,370],[4,460],[4,550],[4,640],[4,730],[4,820],
                             [94,10],[94,100],[94,190],[94,280],[94,370],[94,460],[94,550],[94,640],[94,730],[94,820]]
        
        self.defendersgrid = [[6,20],[6,120],[6,220],[6,320],[6,420],[6,520],[6,620],[6,720],[6,820],[6,920],[6,1020]]
        
        
        
    def startgame(self):
        #self.viewactualizer()
        DeckMixer(self.conector)
        #self.ui.show()
        
       
    def conection_sql(self):
        global conector
        conector = sqlite3.connect("currentgame.db")
        return conector  
    
    def tester(self):
        
        #self.ui.show()
        
        
        DrawCardPhase(self.conector).actionphase()
        SpaceKarmaPhase(self.conector).actionphase()
        EventPhase(self.conector).actionphase()
        Buildphase(self.conector).testeractionphase()
        #self.handassigner()
        #self.buildingsactualizer()
        #self.randomframeactualizer(self.ui.invaders_frame, "invader")
        #self.randomframeactualizer(self.ui.defenders_frame, "defending")
        #self.viewactualizer()
        PowerPhase(self.conector).actionphase()
        IncomePhase(self.conector).actionphase(self.megacredits)
        
    
    
    
    def gameplay(self):
        
        self.viewactualizer()
        if self.phasecounter > 5: self.phasecounter = 0
        self.turn(self.phasecounter)
        
        
        
        self.viewactualizer()
        
    def turn(self, phaseindicator):
        print("phase: ",phaseindicator)
        
        
        if phaseindicator == 0: self.drawphasefunction()
        elif phaseindicator == 1: self.spacekarmaphasefunction()
        elif phaseindicator == 2: self.eventphasefunction()
        elif phaseindicator == 3: self.buildphasefunction()
        elif phaseindicator == 4: self.powerphasefunction()
        elif phaseindicator == 5: self.incomephasefunction()
        
        self.phasecounter += 1
        
    def restarter(self):
        tabledropper(self.conector)
        tableconstructor(self.conector)
        self.deck = cardextraction(self.cardpath)
        massiveloader(self.conector, self.deck)
    
    def drawphasefunction(self):
        #self.ui.info_phase_label.setText("Drawing Card")
        DrawCardPhase(self.conector).actionphase()
        
    def spacekarmaphasefunction(self):
        #self.ui.info_phase_label.setText("Space Karma Phase")
        communicator = SpaceKarmaPhase(self.conector).actionphase()
        return communicator
        
    def eventphasefunction(self):
        #self.ui.info_phase_label.setText("Events Phase")
        self.megacredits += EventPhase(self.conector).actionphase()
        
    def battlepreparationfunction(self):
        self.battle = BattlePhase(self.conector)
        communicator = self.battle.actionphase()
        return communicator
    
    def battledefendersfunction(self):
        communicator = self.battle.vsdefenders()
        return communicator
        
    def battlelassersfunction(self):
        communicator = self.battle.vsturrets()
        return communicator
        
    def battledomesfunction(self):
        communicator = self.battle.vsdome()
        return communicator
        
    def battlebasefunction(self):
        communicator = self.battle.vsbase()
        return communicator
    
    def buildphasefunctiontester(self):
        #self.ui.info_phase_label.setText("Build Phase")
        Buildphase(self.conector).testeractionphase()
      
        
    def building(self, ident):
        
        comunicator = Buildphase(self.conector).actionphase(ident)
        return comunicator  
                
    
    def powerphasefunction(self):
        #self.ui.info_phase_label.setText("Power Phase")
        PowerPhase(self.conector).actionphase()
    
    def incomephasefunction(self):
        #self.ui.info_phase_label.setText("Income Phase")
        self.megacredits = IncomePhase(self.conector).actionphase(self.megacredits)
        
        
           
    def printer(self, toprint):
        print(toprint)
    
    def cleanandload(function):
        
        def package(self):
            
            self.viewactualizer()
        return package
     
    #def viewactualizer(self):
    #    self.handassigner()
    #    self.buildingsactualizer()
        #self.randomframeactualizer(self.ui.invaders_frame, "invader")
        #self.randomframeactualizer(self.ui.defenders_frame, "defending")
        
        
    """def buildingsactualizer(self):
        built = identifierextractor(self.invertedcardselector("placement", "builded"))
        for i in built:
            individualbuilding = self.cardselector(i)[0][1]
            #for card in self.ui.base_frame.findChildren(QtWidgets.QLabel):
                if individualbuilding == card.objectName():
                    card.setStyleSheet(" color: black ; background-color: yellow")"""
    
    """def randomframeactualizer(self, referenceframe, showing):
        tobeadded = []
        playedid = identifierextractor(self.invertedcardselector("placement", showing))
        played = []
        for card in playedid:
            played.append(self.cardselector(card)[0][1])
        allslots = referenceframe.findChildren(QtWidgets.QLabel)
        
        tobeadded = played.copy()
        nodispslotnames = []
        for slots in allslots:
            if slots.objectName() != "empty":
                nodispslotnames.append(slots.objectName()) 
        nodiplotsnamesunique = set((nodispslotnames))
        nodispslot = []
        for names in nodiplotsnamesunique:
            nodispslot.append(identifierextractor(self.invertedcardselector("card", names)))
        
        nodispslot.sort()
        
        
        for newandold in tobeadded:
            for slot2 in nodiplotsnamesunique:
                if newandold == slot2:
                    played.remove(newandold)
        
        
        dispslot = referenceframe.findChildren(QtWidgets.QLabel, name = "empty")
        
        for i in played:
            
            rndplacing = random.choice(dispslot)
            
            rndplacing.setObjectName(i)
            ident = identifierextractor(self.invertedcardselector("card",i))[0]
            rndplacing.setStyleSheet(" background-color: red")
            rndplacing.show()
            icon = self.genericdatabasequery("SELECT pict FROM images WHERE id="+str(ident))[0][0]
            rndplacing.setPixmap(QtGui.QPixmap("images\\"+icon+".png"))
            rndplacing.setScaledContents(True)
            
            """
            
    
    """def handassigner(self):
        inhand = identifierextractor(self.invertedcardselector("placement", "hand"))
        dispslot = self.ui.hand_frame.findChildren(QtWidgets.QLabel)
        
        
        for slt in dispslot:
            slt.setObjectName("hand")
        
        for i in range(len(inhand)):
            
            placing = self.cardselector(inhand[i])[0][1]
            ident = self.cardselector(inhand[i])[0][0]
            dispslot[i].show()
            dispslot[i].setObjectName(placing)
            dispslot[i].setStyleSheet( "background-color: blue")
            icon = "modules\\test.png"
            icon = self.genericdatabasequery("SELECT pict FROM images WHERE id="+str(ident))[0][0]
            
            dispslot[i].setPixmap(QtGui.QPixmap("images\\"+icon+".png"))
            dispslot[i].setScaledContents(True)
            
            #dispslot[i].button.clicked.connect(lambda:self.printer())
        
        for slt in dispslot:
            if slt.objectName() == "hand":
                slt.hide()
                slt.setStyleSheet( "background-color: #1E1E1E")
                slt.setPixmap(QtGui.QPixmap(""))
                slt.button.clicked.connect(lambda:self.passer())"""
                
    def passer(self):
        pass        
            
    def printer(self, *args):
        print("eventincontrol")
            
            
            
        
       
    
    
     
    
         
    
        
            
            
                         
            
        
    
    
    

    
     
        

if __name__ == "__main__":
    
    ui = Control("modules\cards.csv")
    #ui.ui.show()
    
    ui.tester()
    #ui.ui.tester()
    
    


    

    
        
        
        