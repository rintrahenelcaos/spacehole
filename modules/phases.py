# Module containing game phases

import random


try:
    from dbcontrol import DBControl
    from events import Events
except:
    from modules.dbcontrol import DBControl, identifierextractor
    from modules.events import Events




class Phase():
    """ Phase blueprint. Serves as a master class for the rest of the classes instantiating DBControl
    """
    

    def __init__(self, deck):
        table = DBControl(deck)
        self.tablemodifier = table.tablemodifier
        self.cardselector = table.cardselector
        self.invertedcardselector = table.invertedcardselector
        self.filteredaspectcardselector = table.filteredaspectcardselector
        self.genericdatabasequery = table.genericdatabasequery

class DeckMixer(Phase): 
    """ Deckmixer class

    Args:
        Phase (class): Phase blueprint. Serves as a master class for the rest of the classes instantiating DBControl
    """
    
    def __init__(self, deck):
        super().__init__(deck)
        availablecards = self.invertedcardselector("placement", "deck")
        deckorder = []
        
        for i in availablecards:
            deckorder.append(i[0])
        
        random.shuffle(deckorder)
        
        for pos in range(len(deckorder)):
            self.tablemodifier(deckorder[pos], "deckpos", pos)


class DrawCardPhase(Phase):
    """ Drawcard Phase

    Args:
        Phase (class): Phase blueprint. Serves as a master class for the rest of the classes instantiating DBControl
    """
    
    def actionphase(self, *args):
        b = self.genericdatabasequery("SELECT id FROM deck WHERE deckpos = (SELECT min(deckpos) FROM deck)")
        
        
        a = b[0][0]
        
        self.tablemodifier(a, "placement", "hand")
        self.tablemodifier(a, "deckpos", "")
        
        
   
class SpaceKarmaPhase(Phase):
    """ Space karma phase

    Args:
        Phase (class): Phase blueprint. Serves as a master class for the rest of the classes instantiating DBControl
    """
    
    def __init__(self, deck):
        super().__init__(deck)
        self.availablecards = self.invertedcardselector("placement", "hand")
        self.hand= []
        self.hand = identifierextractor(self.availablecards)
        self.communicator = ""
        
    
    def actionphase(self, *args): # launches the phase
        
        for i in self.hand:
            card = self.cardselector(i)
            try:
                if card[0][2] == "event": # get if there is an event to play
                    self.tablemodifier(i, "placement", "event")
                    self.communicator = "Event: "+card[0][1]+" about to happen"
                elif card[0][2] == "invader": # get if there is an invader to play
                    self.tablemodifier(i, "placement", "invader")
                    self.communicator = "New invader: "+card[0][1]
            except: self.communicator = "No new events or invaders to report"
        return self.communicator

class EventPhase(Phase):
    """Event phase

    
    """
    
    def __init__(self, deck):
        """Event phase

        Args:
            deck (db): db
        """
        super().__init__(deck)
        
        self.deck = deck
        
    
    def actionphase(self, *args): # launches the phase
        eventsonwaittuple = self.invertedcardselector("placement", "event")
        eventsonwait =identifierextractor(eventsonwaittuple) # detect events in play
        
        if len(eventsonwait) > 0: # launch events if needed
            
            meg = self.eventlauncher(eventsonwait[0]) # call the event luancher
            self.tablemodifier(eventsonwait[0], "placement", "discard") # discard the event card
            
        invadersonwaittuple = self.invertedcardselector("placement", "invader")
        invadersonwait = identifierextractor(invadersonwaittuple)
        
        
        return meg
            
            
        
            
    def eventlauncher(self, event):
        """ Launches events

        Args:
            event (str): event effect definner in db

        Returns:
           int: megacredits modification
        """
        ev = self.cardselector(event)[0][11]
        
        meg = Events(self.deck, ev).actionphase()
        return meg
        


class BattlePhase(Phase):
    """Battle phase. Includes all subphases of battle

    
    """
    def __init__(self, deck):
        """ Battle phase. Includes all subphases of battle. Works by passing the damage from method to method. 
        First calculates the damage, second assing it to the defenders, then lasers, domes and finally to the base. 
        if the invaders are destroyed in any of the subphases, the rest are passed

        Args:
            deck (db): db
        """
        super().__init__(deck)
        
        
        self.communicator =""
        
    def actionphase(self, *args):
        """ Battle preparations subphase. Manages all data to subsequent methods. Counts defenders, laserturrets and invaders and calculates how much damage each dealt

        Returns:
            str: description 
        """
        
        
        invadermarching = identifierextractor(self.filteredaspectcardselector("placement","invader","force")) # get the invaders
        
        invaderforce = 0
        self.totalattack = 0
        for i in invadermarching:
            invaderforce += i
            
        for h in range(invaderforce):
            rand =random.randint(1,6)
           
            if rand == 1:
                self.totalattack += 1 # total damage invaders deal
        
        
        defendersonline = identifierextractor(self.filteredaspectcardselector("placement","defending","force")) # get the defenders in play
        lasersonline = identifierextractor(self.filteredaspectcardselector("placement","builded","force")) # get the invaders in play
       
        defenderforce = 0
        laserforce = 0
        self.totaldefense = 0
        self.totallasser = 0
        for d in defendersonline:
            defenderforce += d # amount of attacks of the defenders
        for l in lasersonline:
            laserforce += l # amount of lasers
        for h in range(defenderforce):
            rand = random.randint(1,6)
            if rand == 1:
                self.totaldefense += 1 # total damage the defenders deal
        for h2 in range(laserforce):
            rand = random.randint(1,6)
            if rand == 1:
                self.totallasser += 1 # total damage lasers deal
            
                
        self.invaderlist = identifierextractor(self.invertedcardselector("placement","invader")) # setting the list of invaders to recieve damage
        self.defenderslist = identifierextractor(self.invertedcardselector("placement","defending")) # setting the list of defenders to recieve damage
        self.lasserturrets = identifierextractor(self.invertedcardselector("placement", "builded")) # setting the list of invaders to recieve damage
        self.lasserturrets2 = self.lasserturrets.copy()
        for lasser in self.lasserturrets2:
            if int(self.cardselector(lasser)[0][12]) == 0:
                self.lasserturrets.remove(lasser)
        
        self.lasserturrets.remove(1)
        
        self.forcedomes = identifierextractor(self.genericdatabasequery("SELECT id FROM deck WHERE card LIKE 'Force%'", )) # setting the list of domes to recieve damage
        
        self.forcedomes2 = self.forcedomes.copy()
        for dome in self.forcedomes2:
            
            if self.cardselector(dome)[0][14] != "builded":
                
                self.forcedomes.remove(dome)
        
        
        self.communicator = "Invaders: "
        for i in self.invaderlist:
            self.communicator += self.cardselector(i)[0][1]
        self.communicator += " are marching"
        
        
        
        return self.communicator
        
        
    def vsdefenders(self, *args):
        """Subphase in charge of the defenders

        Returns:
            tuple: description(str), damage dealt to defenders (int), damage dealt to invaders (int)
        """
        
        
        
        if len(self.invaderlist) > 0: # check if thre are invaders left
            originalinvaderattack = self.totalattack
            originaldefense = self.totaldefense
            while self.totalattack > 0: # assign damage to the defenders 
                if len(self.defenderslist) > 0:
                    
                    targetdef = random.choice(self.defenderslist)
                    hitted = int(self.cardselector(targetdef)[0][16])
                    hitted += 1
                    self.tablemodifier(targetdef, "hitted", hitted)
                    if hitted == int(self.cardselector(targetdef)[0][13]):
                        self.tablemodifier(targetdef,"placement", "discard")
                        self.defenderslist.remove(targetdef)
                    self.totalattack -= 1
                else: break  # all defenders destroyed
            
            while self.totaldefense > 0:  # assign damage to the invaders
                if len(self.invaderlist) > 0:
                    targetinvader = random.choice(self.invaderlist)
                    hitted = int(self.cardselector(targetinvader)[0][16])
                    hitted +=1
                    self.tablemodifier(targetinvader, "hitted", hitted)
                    if hitted == int(self.cardselector(targetinvader)[0][13]):
                        self.tablemodifier(targetinvader,"placement", "discard")
                        self.invaderlist.remove(targetinvader)
                    self.totaldefense -= 1
                else: break # all invaders destroyed
            self.communicator = "Damage dealt to defenders: "+str(originalinvaderattack-self.totalattack)+". Damage dealt to invaders by defenders: "+str(originaldefense - self.totaldefense)
            
        else: self.communicator = "All invaders destroyed"
        return self.communicator, originalinvaderattack-self.totalattack, originaldefense - self.totaldefense
        
                
    def vsturrets(self, *args):
        """Subphase in charge of the lassers

        Returns:
            tuple: description(str), damage dealt to lassers (int), damage dealt to invaders (int)
        """
        
        if len(self.invaderlist) > 0 : # check if thre are invaders left
            originalinvaderattack = self.totalattack
            originallasser = self.totallasser
            while self.totalattack > 0:
                if len(self.lasserturrets) > 0: # assing damage to lasers
                    targetlasser = random.choice(self.lasserturrets)
                    hitted = int(self.cardselector(targetlasser)[0][16])
                    hitted += 1
                    self.tablemodifier(targetlasser, "hitted", hitted)
                    if hitted == int(self.cardselector(targetlasser)[0][13]):
                        self.tablemodifier(targetlasser,"placement", "discard")
                        self.lasserturrets.remove(targetlasser)
                    self.totalattack -= 1
                else: break    # all lasers destroyed
            
             
            while self.totallasser > 0: # assign damage to invaders
                if len(self.invaderlist)>0:
                    targetinvader = random.choice(self.invaderlist)
                    hitted = int(self.cardselector(targetinvader)[0][16])
                    hitted +=1
                    self.tablemodifier(targetinvader, "hitted", hitted)
                    if hitted == int(self.cardselector(targetinvader)[0][13]):
                        self.tablemodifier(targetinvader,"placement", "discard")
                        self.invaderlist.remove(targetinvader)
                    self.totallasser -= 1
                else: break # all invaders destroyed
            
            self.communicator = "Damage dealt to lassers: "+str(originalinvaderattack-self.totalattack)+". Damage dealt to invaders by lassers: "+str(originallasser - self.totallasser)
            
        else: self.communicator = "All invaders destroyed"
        return self.communicator, originalinvaderattack-self.totalattack, originallasser - self.totallasser
    
    def vsdome(self, *args):
        """Subphase in charge of the domes

        Returns:
            tuple: description(str), damage dealt to domes (int)
        """
        
        if len(self.invaderlist) > 0: # check if thre are invaders left
            originalinvaderattack = self.totalattack
            while self.totalattack > 0:
                if len(self.forcedomes) > 0: # assign damage to domes
                    targetdome = random.choice(self.forcedomes)
                    hitted = int(self.cardselector(targetdome)[0][16])
                    hitted += 1
                    self.tablemodifier(targetdome, "hitted", hitted)
                    if hitted == int(self.cardselector(targetdome)[0][13]):
                        self.tablemodifier(targetdome,"placement", "discard")
                        self.forcedomes.remove(targetdome)
                    self.totalattack -= 1
                else: break # all domes destroyed
            self.communicator = "Damage dealt to domes: "+str(originalinvaderattack-self.totalattack)+"."
            
        else: self.communicator = "All invaders destroyed"
        return self.communicator, originalinvaderattack-self.totalattack
    
    def vsbase(self, *args):
        """Subphase in charge of the base

        Returns:
            tuple: description(str), damage dealt to base (int)
        """
        
        if len(self.invaderlist) > 0: # check if thre are invaders left
            originalinvaderattack = self.totalattack
            while self.totalattack > 0: # assign damage to base
                if self.cardselector(1)[0][14] != "discard":
                    
                    hitted = int(self.cardselector(1)[0][16])
                    
                    hitted += 1
                    
                    self.tablemodifier(1, "hitted", hitted)
                    if hitted == int(self.cardselector(1)[0][13]):
                        self.tablemodifier(1,"placement", "discard")
                        
                    self.totalattack -= 1
                else: break # base destroyed
            self.communicator = "Damage dealt to base: "+str(originalinvaderattack-self.totalattack)+"."
            
        else: self.communicator = "All invaders destroyed"
        return self.communicator, originalinvaderattack-self.totalattack
        


class Buildphase(Phase):
    """ Build Phase

    
    """
    
    
    def __init__(self, deck):
        """ Build and recruit Phase

        Args:
            deck (db): db
        """
        super().__init__(deck)
        # initialize all building conditions
        self.power = 0
        self.agrogen = 0
        self.defenders = 0
        self.mining = 0
        self.refinerie = 0
        self.colonies = 0
        self.labs = 0
        self.comunicator = ""
        
        
        self.conditionalcalculators() # check for contditions
        
    
    def conditionalcalculators(self):
        """ Gets the conditions to build
        """
        self.builded = identifierextractor(self.invertedcardselector("placement", "builded"))  # get the built structures and their properties
        self.defending = identifierextractor(self.invertedcardselector("placement", "defending")) # get the defenders
        self.power = 0
        self.agrogen = 0
        self.defenders = 0
        self.mining = 0
        self.refinerie = 0
        self.colonies = 0
        self.labs = 0
        for i in self.builded: # get the important values
            building = self.cardselector(i)[0]
            
            self.power += building[4]
            self.agrogen += building[5]
            self.defenders += building[6]
            self.mining += building[7]
            self.refinerie += building[8]
            self.colonies += building[9]
            self.labs += building[10]
        for d in self.defending:
            defendingok = self.cardselector(d)[0]
            self.defenders += defendingok[6] # get the availability of recruiting. 
        
           
            
    def testeractionphase(self, *args):
        """Unused/ Test function
        """
        self.availablecards =  identifierextractor(self.invertedcardselector("placement", "hand"))
        
        for i in self.availablecards:
            self.actionphase(i)
        self.builded = identifierextractor(self.invertedcardselector("placement", "builded"))
        
    def actionphase(self, selected, *args):
        """ Action method of build phase

        Args:
            selected (str): card id

        Returns:
            str: description of the result of method
        """
        
        
        tobuild = self.cardselector(selected)[0]
        
        if tobuild[2] == "build":
            self.conditionbuildok(tobuild)
        elif tobuild[2] == "defender":
            self.recruit(tobuild)   
        self.conditionalcalculators()
        return self.comunicator 
            
    
    
    
    def conditionbuildok(self, tested):
        """ Checks if the conditions to build are met. It chacks every variable vs tested. 

        Args:
            tested (_type_): _description_
        """
        ok = True
        if self.power + tested[4] < 0: ok = False
        if self.agrogen + tested[5] < 0: ok = False
        if self.mining + tested[7] < 0: ok = False
        if self.refinerie + tested[8] < 0: ok = False
        if self.colonies + tested[9] < 0: ok = False
        if self.labs + tested[10] < 0: ok = False
        
        if ok: 
            self.tablemodifier(tested[0], "placement", "builded")
            self.comunicator = str(self.cardselector(tested[0])[0][1])+" builded"
        else: self.comunicator = "Building conditions not met"
        
    def recruit(self, tested):
        if self.defenders + tested[6] > -1:
            
            self.tablemodifier(tested[0], "placement", "defending")  
            self.comunicator = str(self.cardselector(tested[0])[0][1])+" recruited" 
        else:self.comunicator = "Recruiting conditions not met"
            
class PowerPhase(Phase):
    """Unused

    
    """
    def __init__(self, deck):
        super().__init__(deck)
        
        self.power = 0
        self.builded = identifierextractor(self.invertedcardselector("placement", "builded"))
        
        for i in self.builded:
            building = self.cardselector(i)[0]
            self.power += building[4]
   
    def actionphase(self, *args):
        
        if self.power < 0 :
            self.poweralocation()
        else: pass
            
            
        
    def poweralocation(self): # unused
        pass
        
    
class IncomePhase(Phase):  
    """ Income phase
    """  
    def __init__(self, deck):
        """ Income phase
        """  
        super().__init__(deck)
        
        self.megacredits = 0
        self.builded = identifierextractor(self.invertedcardselector("placement", "builded"))
        for i in self.builded:
            building = self.cardselector(i)[0]
            self.megacredits += building[3] # add all income values of buildings
            
    def actionphase(self, megacredits):
        """ MMegacredits calculation method

        Args:
            megacredits (str): variation at the end of turn

        Returns:
           int: new megacredits
        """
        megacredits += self.megacredits # change megacredits
        
        return megacredits
    

        
        
        
    
       
    
                         
        
        




