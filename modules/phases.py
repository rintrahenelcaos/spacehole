import random


try:
    from dbcontrol import DBControl
except:
    from modules.dbcontrol import DBControl, identifierextractor


class Phase():
    

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
    
    def actionphase(self, *args):
        b = self.genericdatabasequery("SELECT id FROM deck WHERE deckpos = (SELECT min(deckpos) FROM deck)")
        
        
        a = b[0][0]
        
        self.tablemodifier(a, "placement", "hand")
        self.tablemodifier(a, "deckpos", "")
        
        
   
class SpaceKarmaPhase(Phase):
    
    def __init__(self, deck):
        super().__init__(deck)
        self.availablecards = self.invertedcardselector("placement", "hand")
        self.hand= []
        self.hand = identifierextractor(self.availablecards)
        
    
    def actionphase(self, *args):
        newinvader = 0
        newevent = 0
        
        #hand = self.cardselector(identif)
        for i in self.hand:
            card = self.cardselector(i)
            try:
                if card[0][2] == "event":
                    self.tablemodifier(i, "placement", "event")
                elif card[0][2] == "invader":
                    self.tablemodifier(i, "placement", "invader")
            except: pass

class EventPhase(Phase):
    def __init__(self, deck):
        super().__init__(deck)
        #self.avalablecards = self.invertedcardselector()
    
    def actionphase(self, *args):
        eventsonwaittuple = self.invertedcardselector("placement", "event")
        eventsonwait =identifierextractor(eventsonwaittuple)
        
        if len(eventsonwait) > 0:
            
            self.eventlauncher()
            self.tablemodifier(eventsonwait[0], "placement", "discard")
            
        invadersonwaittuple = self.invertedcardselector("placement", "invader")
        invadersonwait = identifierextractor(invadersonwaittuple)
        if len(invadersonwait) > 0:
            print("battle")
            print(invadersonwait)
            #self.battle()
            
            
        
            
    def eventlauncher(self):
        print("event")


    def battle(self):
        invadermarching = identifierextractor(self.filteredaspectcardselector("placement","invader","force"))
        print("invading",invadermarching)
        invaderforce = 0
        totalattack = 0
        for i in invadermarching:
            invaderforce += i
        for h in range(invaderforce):
            rand =random.randint(1,6)
            if rand == 1:
                totalattack += 1
        
        
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
            
                
        invaderlist = identifierextractor(self.invertedcardselector("placement","invader")) 
        defenderslist = identifierextractor(self.invertedcardselector("placement","defending")) 
        self.lasserturrets = identifierextractor(self.invertedcardselector("placement", "builded"))
        self.lasserturrets2 = self.lasserturrets.copy()
        for lasser in self.lasserturrets2:
            if int(self.cardselector(lasser)[0][12]) == 0:
                self.lasserturrets.remove(lasser)
        print(self.lasserturrets)
        self.lasserturrets.remove(1)
        print(self.lasserturrets)
        self.forcedomes = identifierextractor(self.genericdatabasequery("SELECT id FROM deck WHERE card LIKE 'Force%'", ))
        print(self.forcedomes)
        self.forcedomes2 = self.forcedomes.copy()
        for dome in self.forcedomes2:
            
            if self.cardselector(dome)[0][14] != "builded":
                
                self.forcedomes.remove(dome)
        print("domes",self.forcedomes) 
        
        if totalattack > 0:
            while totalattack > 0:
                if len(defenderslist) > 0:
                    targetdef = random.choice(defenderslist)
                    hitted = int(self.cardselector(targetdef)[0][16])
                    hitted += 1
                    self.tablemodifier(targetdef, "hitted", hitted)
                    if hitted == int(self.cardselector(targetdef)[0][13]):
                        self.tablemodifier(targetdef,"placement", "discard")
                        defenderslist.remove(targetdef)
                    totalattack -= 1
                else: break  
            
            while self.totaldefense > 0:  
                if len(invaderlist) > 0:
                    targetinvader = random.choice(invaderlist)
                    hitted = int(self.cardselector(targetinvader)[0][16])
                    hitted +=1
                    self.tablemodifier(targetinvader, "hitted", hitted)
                    if hitted == int(self.cardselector(targetinvader)[0][13]):
                        self.tablemodifier(targetinvader,"placement", "discard")
                        invaderlist.remove(targetinvader)
                    self.totaldefense -= 1
                else: totalattack = 0
                    
                
            
        if totalattack > 0:
            while totalattack > 0:
                if len(self.lasserturrets) > 0:
                    targetlasser = random.choice(self.lasserturrets)
                    hitted = int(self.cardselector(targetlasser)[0][16])
                    hitted += 1
                    self.tablemodifier(targetlasser, "hitted", hitted)
                    if hitted == int(self.cardselector(targetlasser)[0][13]):
                        self.tablemodifier(targetlasser,"placement", "discard")
                        self.lasserturrets.remove(targetlasser)
                    totalattack -= 1
                else: break   
            
             
                while self.totallasser > 0:
                    if len(invaderlist)>0:
                        targetinvader = random.choice(invaderlist)
                        hitted = int(self.cardselector(targetinvader)[0][16])
                        hitted +=1
                        self.tablemodifier(targetinvader, "hitted", hitted)
                        if hitted == int(self.cardselector(targetinvader)[0][13]):
                            self.tablemodifier(targetinvader,"placement", "discard")
                            invaderlist.remove(targetinvader)
                        self.totaldefense -= 1
                    else: totalattack = 0
                
        
        if totalattack > 0:
            while totalattack > 0:
                if len(self.forcedomes) > 0:
                    targetdome = random.choice(self.forcedomes)
                    hitted = int(self.cardselector(targetdome)[0][16])
                    hitted += 1
                    self.tablemodifier(targetdome, "hitted", hitted)
                    if hitted == int(self.cardselector(targetdome)[0][13]):
                        self.tablemodifier(targetdome,"placement", "discard")
                        self.forcedomes.remove(targetdome)
                    totalattack -= 1
                else: break
        
        if totalattack > 0:
            while totalattack > 0:
                if self.cardselector(1)[0][14] == "discard":
                    
                    hitted = int(self.cardselector(1)[0][16])
                    hitted += 1
                    self.tablemodifier(1, "hitted", hitted)
                    if hitted == int(self.cardselector(1)[0][13]):
                        self.tablemodifier(1,"placement", "discard")
                        
                    totalattack -= 1
                else: break


class BattlePhase(Phase):
    def __init__(self, deck):
        super().__init__(deck)
        
    def actionphase(self, *args):
        
        
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
        print(self.lasserturrets)
        self.lasserturrets.remove(1)
        print(self.lasserturrets)
        self.forcedomes = identifierextractor(self.genericdatabasequery("SELECT id FROM deck WHERE card LIKE 'Force%'", ))
        print(self.forcedomes)
        self.forcedomes2 = self.forcedomes.copy()
        for dome in self.forcedomes2:
            
            if self.cardselector(dome)[0][14] != "builded":
                
                self.forcedomes.remove(dome)
        print("domes",self.forcedomes) 
        
        print("self.totalattack", self.totalattack)
        print("self.totaldefense",self.totaldefense)
        print("self.totallasser", self.totallasser)
        
        
    def vsdefenders(self, *args):
        
        
        
        if len(self.invaderlist) > 0:
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
            print("self.totalattack", self.totalattack)
            print("self.totaldefense",self.totaldefense)
        else: print("No invaders present")
        
                
    def vsturrets(self, *args):
        
        if len(self.invaderlist) > 0 :
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
            print("self.totalattack", self.totalattack)
            print("self.totallasser", self.totallasser)
        else: print("No invaders present")
    
    def vsdome(self, *args):
        
        if len(self.invaderlist) > 0:
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
            print("self.totalattack", self.totalattack)
        else: print("No invaders present")
    
    def vsbase(self, *args):
        
        if len(self.invaderlist) > 0:
            while self.totalattack > 0:
                if self.cardselector(1)[0][14] != "discard":
                    
                    hitted = int(self.cardselector(1)[0][16])
                    print(hitted)
                    hitted += 1
                    print(hitted)
                    self.tablemodifier(1, "hitted", hitted)
                    if hitted == int(self.cardselector(1)[0][13]):
                        self.tablemodifier(1,"placement", "discard")
                        
                    self.totalattack -= 1
                else: break
            print("self.totalattack", self.totalattack)
        else: print("No invaders present")
        


class Buildphase(Phase):
    
    
    def __init__(self, deck):
        super().__init__(deck)
        
        
        #self.builded = identifierextractor(self.invertedcardselector("placement", "builded"))
        self.power = 0
        self.agrogen = 0
        self.defenders = 0
        self.mining = 0
        self.refinerie = 0
        self.colonies = 0
        self.labs = 0
        
        #print("self.builded",self.builded)
        
        self.conditionalcalculators()
        
    
    def conditionalcalculators(self):
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
            #print(building)
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
        
        
        tobuild = self.cardselector(selected)[0]
        print(tobuild)
        if tobuild[2] == "build":
            self.conditionbuildok(tobuild)
        elif tobuild[2] == "defender":
            self.recruit(tobuild)   
        self.conditionalcalculators()
        return self.power, self.agrogen, self.defenders, self.mining, self.refinerie, self.colonies, self.labs 
            
    
    
    
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
        else:pass
        
    def recruit(self, tested):
        if self.defenders + tested[6] > -1:
            
            self.tablemodifier(tested[0], "placement", "defending")   
        else:pass
            
class PowerPhase(Phase):
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
    
class IncomePhase(Phase):    #ojo aca
    def __init__(self, deck):
        super().__init__(deck)
        
        self.megacredits = 0
        self.builded = identifierextractor(self.invertedcardselector("placement", "builded"))
        for i in self.builded:
            building = self.cardselector(i)[0]
            self.megacredits += building[3]
            
    def actionphase(self, megacredits):
        megacredits += self.megacredits
        #print(megacredits)
        return megacredits
    
       
    
                         
        
        




