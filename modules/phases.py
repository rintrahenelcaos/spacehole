import random


try:
    from dbcontrol import DBControl
    from events import Events
except:
    from modules.dbcontrol import DBControl, identifierextractor
    from modules.events import Events




class Phase():
    """ Pahse blueprint
    """
    

    def __init__(self, deck):
        table = DBControl(deck)
        self.tablemodifier = table.tablemodifier
        self.cardselector = table.cardselector
        self.invertedcardselector = table.invertedcardselector
        self.filteredaspectcardselector = table.filteredaspectcardselector
        self.genericdatabasequery = table.genericdatabasequery

class DeckMixer(Phase):
    
    
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
        Phase (_type_): _description_
    """
    
    def actionphase(self, *args):
        b = self.genericdatabasequery("SELECT id FROM deck WHERE deckpos = (SELECT min(deckpos) FROM deck)")
        
        
        a = b[0][0]
        
        self.tablemodifier(a, "placement", "hand")
        self.tablemodifier(a, "deckpos", "")
        
        
   
class SpaceKarmaPhase(Phase):
    """ Space karma phase

    
    """
    
    def __init__(self, deck):
        super().__init__(deck)
        self.availablecards = self.invertedcardselector("placement", "hand")
        self.hand= []
        self.hand = identifierextractor(self.availablecards)
        self.communicator = ""
        
    
    def actionphase(self, *args):
        
        for i in self.hand:
            card = self.cardselector(i)
            try:
                if card[0][2] == "event":
                    self.tablemodifier(i, "placement", "event")
                    self.communicator = "Event: "+card[0][1]+" about to happen"
                elif card[0][2] == "invader":
                    self.tablemodifier(i, "placement", "invader")
                    self.communicator = "New invader: "+card[0][1]
            except: self.communicator = "No new events or invaders to report"
        return self.communicator

class EventPhase(Phase):
    """Event phase

    
    """
    
    def __init__(self, deck):
        super().__init__(deck)
        
        self.deck = deck
        
    
    def actionphase(self, *args):
        eventsonwaittuple = self.invertedcardselector("placement", "event")
        eventsonwait =identifierextractor(eventsonwaittuple)
        
        if len(eventsonwait) > 0:
            
            meg = self.eventlauncher(eventsonwait[0])
            self.tablemodifier(eventsonwait[0], "placement", "discard")
            
        invadersonwaittuple = self.invertedcardselector("placement", "invader")
        invadersonwait = identifierextractor(invadersonwaittuple)
        if len(invadersonwait) > 0:
            print("battle")
            print(invadersonwait)
            #self.battle()
        
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
        super().__init__(deck)
        
        self.communicator =""
        
    def actionphase(self, *args):
        """ Battle preparations subphase. Manages all data to subsequent methods

        Returns:
            str: description 
        """
        
        
        invadermarching = identifierextractor(self.filteredaspectcardselector("placement","invader","force"))
        print("invading",invadermarching)
        invaderforce = 0
        self.totalattack = 0
        for i in invadermarching:
            invaderforce += i
            print("total invaderforce: ",invaderforce)
        for h in range(invaderforce):
            rand =random.randint(1,6)
            print("hs",h,"  ",rand)
            if rand == 1:
                self.totalattack += 1
        
        
        defendersonline = identifierextractor(self.filteredaspectcardselector("placement","defending","force"))
        lasersonline = identifierextractor(self.filteredaspectcardselector("placement","builded","force"))
        print("defending",defendersonline)
        print("laser ",lasersonline)
        defenderforce = 0
        laserforce = 0
        self.totaldefense = 0
        self.totallasser = 0
        for d in defendersonline:
            defenderforce += d
        for l in lasersonline:
            laserforce += l
        for h in range(defenderforce):
            rand = random.randint(1,6)
            if rand == 1:
                self.totaldefense += 1
        for h2 in range(laserforce):
            rand = random.randint(1,6)
            if rand == 1:
                self.totallasser += 1
            
                
        self.invaderlist = identifierextractor(self.invertedcardselector("placement","invader")) 
        self.defenderslist = identifierextractor(self.invertedcardselector("placement","defending")) 
        self.lasserturrets = identifierextractor(self.invertedcardselector("placement", "builded"))
        self.lasserturrets2 = self.lasserturrets.copy()
        for lasser in self.lasserturrets2:
            if int(self.cardselector(lasser)[0][12]) == 0:
                self.lasserturrets.remove(lasser)
        
        self.lasserturrets.remove(1)
        
        self.forcedomes = identifierextractor(self.genericdatabasequery("SELECT id FROM deck WHERE card LIKE 'Force%'", ))
        
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
        
        
        
        if len(self.invaderlist) > 0:
            originalinvaderattack = self.totalattack
            originaldefense = self.totaldefense
            while self.totalattack > 0:
                if len(self.defenderslist) > 0:
                    
                    targetdef = random.choice(self.defenderslist)
                    hitted = int(self.cardselector(targetdef)[0][16])
                    hitted += 1
                    self.tablemodifier(targetdef, "hitted", hitted)
                    if hitted == int(self.cardselector(targetdef)[0][13]):
                        self.tablemodifier(targetdef,"placement", "discard")
                        self.defenderslist.remove(targetdef)
                    self.totalattack -= 1
                else: break  
            
            while self.totaldefense > 0:  
                if len(self.invaderlist) > 0:
                    targetinvader = random.choice(self.invaderlist)
                    hitted = int(self.cardselector(targetinvader)[0][16])
                    hitted +=1
                    self.tablemodifier(targetinvader, "hitted", hitted)
                    if hitted == int(self.cardselector(targetinvader)[0][13]):
                        self.tablemodifier(targetinvader,"placement", "discard")
                        self.invaderlist.remove(targetinvader)
                    self.totaldefense -= 1
                else: break
            self.communicator = "Damage dealt to defenders: "+str(originalinvaderattack-self.totalattack)+". Damage dealt to invaders by defenders: "+str(originaldefense - self.totaldefense)
            
        else: self.communicator = "All invaders destroyed"
        return self.communicator, originalinvaderattack-self.totalattack, originaldefense - self.totaldefense
        
                
    def vsturrets(self, *args):
        """Subphase in charge of the lassers

        Returns:
            tuple: description(str), damage dealt to lassers (int), damage dealt to invaders (int)
        """
        
        if len(self.invaderlist) > 0 :
            originalinvaderattack = self.totalattack
            originallasser = self.totallasser
            while self.totalattack > 0:
                if len(self.lasserturrets) > 0:
                    targetlasser = random.choice(self.lasserturrets)
                    hitted = int(self.cardselector(targetlasser)[0][16])
                    hitted += 1
                    self.tablemodifier(targetlasser, "hitted", hitted)
                    if hitted == int(self.cardselector(targetlasser)[0][13]):
                        self.tablemodifier(targetlasser,"placement", "discard")
                        self.lasserturrets.remove(targetlasser)
                    self.totalattack -= 1
                else: break   
            
             
            while self.totallasser > 0:
                if len(self.invaderlist)>0:
                    targetinvader = random.choice(self.invaderlist)
                    hitted = int(self.cardselector(targetinvader)[0][16])
                    hitted +=1
                    self.tablemodifier(targetinvader, "hitted", hitted)
                    if hitted == int(self.cardselector(targetinvader)[0][13]):
                        self.tablemodifier(targetinvader,"placement", "discard")
                        self.invaderlist.remove(targetinvader)
                    self.totallasser -= 1
                else: break
            
            self.communicator = "Damage dealt to lassers: "+str(originalinvaderattack-self.totalattack)+". Damage dealt to invaders by lassers: "+str(originallasser - self.totallasser)
            
        else: self.communicator = "All invaders destroyed"
        return self.communicator, originalinvaderattack-self.totalattack, originallasser - self.totallasser
    
    def vsdome(self, *args):
        """Subphase in charge of the domes

        Returns:
            tuple: description(str), damage dealt to domes (int)
        """
        
        if len(self.invaderlist) > 0:
            originalinvaderattack = self.totalattack
            while self.totalattack > 0:
                if len(self.forcedomes) > 0:
                    targetdome = random.choice(self.forcedomes)
                    hitted = int(self.cardselector(targetdome)[0][16])
                    hitted += 1
                    self.tablemodifier(targetdome, "hitted", hitted)
                    if hitted == int(self.cardselector(targetdome)[0][13]):
                        self.tablemodifier(targetdome,"placement", "discard")
                        self.forcedomes.remove(targetdome)
                    self.totalattack -= 1
                else: break
            self.communicator = "Damage dealt to domes: "+str(originalinvaderattack-self.totalattack)+"."
            
        else: self.communicator = "All invaders destroyed"
        return self.communicator, originalinvaderattack-self.totalattack
    
    def vsbase(self, *args):
        """Subphase in charge of the base

        Returns:
            tuple: description(str), damage dealt to base (int)
        """
        
        if len(self.invaderlist) > 0:
            originalinvaderattack = self.totalattack
            while self.totalattack > 0:
                if self.cardselector(1)[0][14] != "discard":
                    
                    hitted = int(self.cardselector(1)[0][16])
                    
                    hitted += 1
                    
                    self.tablemodifier(1, "hitted", hitted)
                    if hitted == int(self.cardselector(1)[0][13]):
                        self.tablemodifier(1,"placement", "discard")
                        
                    self.totalattack -= 1
                else: break
            self.communicator = "Damage dealt to base: "+str(originalinvaderattack-self.totalattack)+"."
            
        else: self.communicator = "All invaders destroyed"
        return self.communicator, originalinvaderattack-self.totalattack
        


class Buildphase(Phase):
    """ Build Phase

    
    """
    
    
    def __init__(self, deck):
        super().__init__(deck)
        
        self.power = 0
        self.agrogen = 0
        self.defenders = 0
        self.mining = 0
        self.refinerie = 0
        self.colonies = 0
        self.labs = 0
        self.comunicator = ""
        
        
        self.conditionalcalculators()
        
    
    def conditionalcalculators(self):
        """Checks for the conditions to build
        """
        self.builded = identifierextractor(self.invertedcardselector("placement", "builded"))  
        self.defending = identifierextractor(self.invertedcardselector("placement", "defending"))
        self.power = 0
        self.agrogen = 0
        self.defenders = 0
        self.mining = 0
        self.refinerie = 0
        self.colonies = 0
        self.labs = 0
        for i in self.builded:
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
            self.defenders += defendingok[6]
        
           
            
    def testeractionphase(self, *args):
        """Unused/ Test function
        """
        self.availablecards =  identifierextractor(self.invertedcardselector("placement", "hand"))
        #print(self.availablecards)
        for i in self.availablecards:
            self.actionphase(i)
        self.builded = identifierextractor(self.invertedcardselector("placement", "builded"))
        #print(self.builded)
        #self.avilabletobuild = identifierextractor(self.availablecardstuple)
        #self.availabletubuild = identifierextractor(self.genericdatabasequery("SELECT id FROM deck WHERE placement=hand AND type=build;"))
        #print(self.availabletubuild)    
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
        #print(self.builded)
        for i in self.builded:
            building = self.cardselector(i)[0]
            self.power += building[4]
   
    def actionphase(self, *args):
        #print(self.power)
        if self.power < 0 :
            self.poweralocation()
        else: pass
            
            
        
    def poweralocation(self):
        pass
        #print("poweralocation")
    
class IncomePhase(Phase):  
    """ Income phase
    """  
    def __init__(self, deck):
        super().__init__(deck)
        
        self.megacredits = 0
        self.builded = identifierextractor(self.invertedcardselector("placement", "builded"))
        for i in self.builded:
            building = self.cardselector(i)[0]
            self.megacredits += building[3]
            
    def actionphase(self, megacredits):
        """ MMegacredits calculation method

        Args:
            megacredits (str): variation at the end of turn

        Returns:
           int: new megacredits
        """
        megacredits += self.megacredits
        
        return megacredits
    

        
        
        
    
       
    
                         
        
        




