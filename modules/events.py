try:
    from dbcontrol import DBControl
except:
    from modules.dbcontrol import DBControl, identifierextractor

import random

class Events(DBControl):
    def __init__(self, databse):
        super().__init__(databse)

    def damage_to_defenders(self, damage = 2):
        
        defenders = identifierextractor(self.invertedcardselector("placement", "defending"))
        for dam in range(damage):
            if len(defenders) > 0:
                targetdefender = random.choice(defenders)
                hitted = int(self.cardselector(targetdefender)[0][16])
                hitted += 1
                self.tablemodifier(targetdefender, "hitted", hitted)
                if hitted == int(self.cardselector(targetdefender)[0][13]):
                        self.tablemodifier(targetdefender,"placement", "discard")
                        defenders.remove(targetdefender)
            else: pass
        

    def reinforcements(self):
        pass

    def discard_defender(self):
        hand = identifierextractor(self.invertedcardselector("placement", "hand"))
        for card in hand:
            if self.cardselector(card)[0][2] == "defender":
                self.tablemodifier(card,"placement", "discard")

    def discard_hand(self):
        
        hand = identifierextractor(self.invertedcardselector("placement", "hand"))
        for card in hand:
            self.tablemodifier(card,"placement", "discard")

    def destroy_structure(self):
        
        structures = identifierextractor(self.invertedcardselector("placement", "builded"))
        if len(structures) > 0:
            targetstructure = random.choice(structures)
            hitted = int(self.cardselector(targetstructure)[0][16])
            hitted += 1
            self.tablemodifier(targetstructure, "hitted", hitted)
            if hitted == int(self.cardselector(targetstructure)[0][13]):
                    self.tablemodifier(targetstructure,"placement", "discard")
        else: pass
                    
        
    

    def increase_prod(self):
        
        agrodomes = identifierextractor(self.genericdatabasequery("SELECT id FROM deck WHERE card LIKE 'Agrodome%'"))
        for a in agrodomes:
            self.tablemodifier(a, "income", 3)
            
            
    def destroy_defender(self):
        
        defenders = identifierextractor(self.invertedcardselector("placement", "defending"))
        destroyed = random.choice(defenders)
        self.tablemodifier(destroyed, "placement", "discard")

    def eliminate_damage(self):
        
        defenders = identifierextractor(self.invertedcardselector("placement", "defending"))
        for defender in defenders:
            self.tablemodifier(defender, "hitted", 0)
        buildings = identifierextractor(self.invertedcardselector("placement", "builded"))
        for built in buildings:
            self.tablemodifier(built, "hitted", 0)

    def gain_money(self):
        pass

    def return_discarded_defender(self):
        discarteddefender = []
        discarded = identifierextractor(self.invertedcardselector("placement", "discard"))
        for discarted in discarded:
            if self.cardselector(discarted)[0][3] == "defender":
                discarteddefender.append(discarted)
        if len(discarteddefender) > 0:
            returned = random.choice(discarteddefender)
            self.tablemodifier(returned, "hitted", 0)
            self.tablemodifier(returned, "placement", "hand")
    
    def return_discarded_building(self):
        discartedbuilding = []
        discarded = identifierextractor(self.invertedcardselector("placement", "discard"))
        for discarted in discarded:
            if self.cardselector(discarted)[0][3] == "defender":
                discartedbuilding.append(discarted)
        if len(discartedbuilding) > 0:
            returned = random.choice(discartedbuilding)
            self.tablemodifier(returned, "hitted", 0)
            self.tablemodifier(returned, "placement", "hand")