# module linking db to UI. Contains most game functions appart from a couple which are contained in gui.py

import sqlite3


from modules.cards import cardextraction, massiveloader, tableconstructor, tabledropper
from modules.dbcontrol import DBControl, identifierextractor


from modules.phases import DeckMixer, DrawCardPhase, SpaceKarmaPhase, EventPhase, BattlePhase,Buildphase, PowerPhase, IncomePhase


class Control(DBControl): # instantiate the db control object inside the class
    def __init__(self, cardpath):
        
        self.cardpath = cardpath # get the database
        self.conector = self.conection_sql()
        self.pointer = self.conector.cursor()
        tabledropper(self.conector) # restart game db
        tableconstructor(self.conector) # rebuilt it
        self.deck = cardextraction(cardpath) # extract data from csv
        massiveloader(self.conector, self.deck) # load data
        #self.turnlist = [DrawCardPhase, SpaceKarmaPhase, EventPhase, Buildphase, PowerPhase, IncomePhase] # list of classes
        self.megacredits = 0
        self.phasecounter = 0
        
        
        
        
    def startgame(self):
        """ Calls Deckmixer object at game start
        """
        
        DeckMixer(self.conector)
        
        
       
    def conection_sql(self): # method to conect to the db
        global conector
        conector = sqlite3.connect("currentgame.db")
        return conector  
    
       
    def restarter(self): # method to restar the game. Different form the startgame function. Bassically cleans the db and reloads it
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
        
        self.megacredits += EventPhase(self.conector).actionphase() # gets megacredits change in case its needed
        
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
        
        
           
    
   
    
     
        




    

    
        
        
        