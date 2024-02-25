from PyQt5 import QtWidgets, QtCore,QtGui
import sys
import sqlite3
import random

from modules.cards import cardextraction, massiveloader, tableconstructor, tabledropper
from modules.dbcontrol import DBControl, identifierextractor


from modules.phases import DeckMixer, DrawCardPhase, SpaceKarmaPhase, EventPhase, BattlePhase,Buildphase, PowerPhase, IncomePhase


class Control(DBControl):
    def __init__(self, cardpath):
        
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
        
        
        
        
    def startgame(self):
        """ Calls Deckmixer object at game start
        """
        
        DeckMixer(self.conector)
        
        
       
    def conection_sql(self):
        global conector
        conector = sqlite3.connect("currentgame.db")
        return conector  
    
    def tester(self):
        """ Test method
        """
        
        
        
        
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
        
    
        
    def restarter(self):
        """ Clears and reloads db from csv file
        """
        tabledropper(self.conector)
        tableconstructor(self.conector)
        self.deck = cardextraction(self.cardpath)
        massiveloader(self.conector, self.deck)
        self.megacredits = 0
    
    def drawphasefunction(self):
        """ Calls DrawCardPhase object and method
        """
        
        DrawCardPhase(self.conector).actionphase()
        
    def spacekarmaphasefunction(self):
        """ Calls SpaceKarmaPhase object and method

        Returns:
            str: Information to print
        """
        
        communicator = SpaceKarmaPhase(self.conector).actionphase()
        return communicator
        
    def eventphasefunction(self):
        """ Calls EventPhase object and method
        """
        
        self.megacredits += EventPhase(self.conector).actionphase()
        
    def battlepreparationfunction(self):
        """ Instantiates BattlePhase. Must be called before all other battlephases

        Returns:
            str: Information to print
        """
        self.battle = BattlePhase(self.conector)
        communicator = self.battle.actionphase()
        return communicator
    
    def battledefendersfunction(self):
        """ Calls BattlePhase method

        Returns:
            tuple: Information to print, damage to defenders, damage to invaders
        """
        communicator, damagetodefenders, damagetoinvaders = self.battle.vsdefenders()
        return communicator, damagetodefenders, damagetoinvaders
        
    def battlelassersfunction(self):
        """ Calls BattlePhase method

        Returns:
            tuple: Information to print, damage to defenders, damage to invaders
        """
        communicator, damagetolassers, damagetoinvaders = self.battle.vsturrets()
        return communicator, damagetolassers, damagetoinvaders
        
    def battledomesfunction(self):
        """ Calls BattlePhase method

        Returns:
            tuple: Information to print, damage to defenders
        """
        communicator, damagetodomes = self.battle.vsdome()
        return communicator, damagetodomes
        
    def battlebasefunction(self):
        """ Calls BattlePhase method

        Returns:
            tuple: Information to print, damage to defenders
        """
        communicator, damagetobase = self.battle.vsbase()
        return communicator, damagetobase
    
    def buildphasefunctiontester(self):
        """Test method
        """
        #self.ui.info_phase_label.setText("Build Phase")
        Buildphase(self.conector).testeractionphase()
      
        
    def building(self, ident):
        """ Instantiates Buildphase and methods

        Args:
            ident (int): selected card to play

        Returns:
            str: Information to print
        """
        
        comunicator = Buildphase(self.conector).actionphase(ident)
        return comunicator  
                
    
    def powerphasefunction(self):
        """ Unused
        """
        
        PowerPhase(self.conector).actionphase()
    
    def incomephasefunction(self):
        """Instantiates IncomePhase and methods
        """
        
        self.megacredits = IncomePhase(self.conector).actionphase(self.megacredits)
        
        
           
    
   
    
     
        




    

    
        
        
        