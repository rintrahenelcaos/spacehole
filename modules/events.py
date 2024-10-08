# Event Cards handling module. Works by reading event codes from db and linking to each method. creating a class prevents the creation of individual functions

# prevent crash 
try:
    from dbcontrol import DBControl
except:
    from modules.dbcontrol import DBControl, identifierextractor

import random

class Events(DBControl):
    """ Class encapsulating all events effects

    
    """
    
    def __init__(self, databse, order):
        """ Class encapsulating all events effects

        Args:
            databse (db): database
            order (str): code to get selected effect
        """
        super().__init__(databse)
        self.order=order
        
    def actionphase(self): # method choser method. Used to link the event card effect to its method by reading db
        """ Method choser method. Used to link the event card effect to its method by reading db

        Returns:
            int: megacredits variation as consecuence of some events
        """
        
        if self.order == "damage_to_defenders":meg = self.damage_to_defenders()
        elif self.order == "reinforcements":meg =self.reinforcements()
        elif self.order == "discard_defender":meg =self.discard_defender()
        elif self.order == "discard_hand":meg =self.discard_hand()
        elif self.order == "destroy_structure":meg =self.destroy_structure()
        elif self.order == "increase_prod":meg =self.increase_prod()
        elif self.order == "destroy_defender":meg =self.destroy_defender()
        elif self.order == "eliminate_damage":meg =self.eliminate_damage()
        elif self.order == "gain_money_per_structure":meg =self.gain_money_per_structure()
        elif self.order == "return_discarded_defender":meg =self.return_discarded_defender()
        elif self.order == "return_discarded_building":meg =self.return_discarded_building()
        elif self.order == "gain_per_mine":meg =self.gain_per_mine()
        elif self.order == "gain_per_colony":meg =self.gain_per_colony()
        elif self.order == "gain_per_lab":meg =self.gain_per_lab()
        elif self.order == "halve_money":meg =self.halve_money()
        elif self.order == "tax":meg =self.tax()
        
        return meg
            
        

    def damage_to_defenders(self, damage = 2):
        """_summary_

        Args:
            damage (int, optional): Damage dealt to defenders. Defaults to 2.

        Returns:
            int: megacredits variation
        """
        
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
        return 0
        

    def reinforcements(self):
        """ Unused

        Returns:
            _type_: _description_
        """
        
        return 0

    def discard_defender(self):
        """ discard defenders card from hand

        Returns:
            int: megacredits variation
        """
        hand = identifierextractor(self.invertedcardselector("placement", "hand"))
        for card in hand:
            if self.cardselector(card)[0][2] == "defender":
                self.tablemodifier(card,"placement", "discard")
        return 0

    def discard_hand(self):
        """ discard hand

        Returns:
            int: megacredits variation
        """
        hand = identifierextractor(self.invertedcardselector("placement", "hand"))
        for card in hand:
            self.tablemodifier(card,"placement", "discard")
        return 0

    def destroy_structure(self):
        """ deals 1 hit to random building

        Returns:
            int: megacredits variation
        """
        
        structures = identifierextractor(self.invertedcardselector("placement", "builded"))
        if len(structures) > 0:
            targetstructure = random.choice(structures)
            hitted = int(self.cardselector(targetstructure)[0][16])
            hitted += 1
            self.tablemodifier(targetstructure, "hitted", hitted)
            if hitted == int(self.cardselector(targetstructure)[0][13]):
                    self.tablemodifier(targetstructure,"placement", "discard")
        else: pass
        return 0
    
    def increase_prod(self):
        """ Cahnge agrodomes output

        Returns:
            int: megacredits variation
        """
        
        agrodomes = identifierextractor(self.genericdatabasequery("SELECT id FROM deck WHERE card LIKE 'Agrodome%'"))
        for a in agrodomes:
            self.tablemodifier(a, "income", 3)
        return 0
            
            
    def destroy_defender(self):
        """ Discard defenders card in play

        Returns:
            int: megacredits variation
        """
        
        defenders = identifierextractor(self.invertedcardselector("placement", "defending"))
        if len(defenders) > 0:
            destroyed = random.choice(defenders)
            self.tablemodifier(destroyed, "placement", "discard")
        return 0

    def eliminate_damage(self):
        """ Clears all hits to defenders and buildings to their original values

        Returns:
            int: megacredits variation
        """
        
        defenders = identifierextractor(self.invertedcardselector("placement", "defending"))
        for defender in defenders:
            self.tablemodifier(defender, "hitted", 0)
        buildings = identifierextractor(self.invertedcardselector("placement", "builded"))
        for built in buildings:
            self.tablemodifier(built, "hitted", 0)
        return 0

    def gain_money_per_structure(self):
        """ get money for every building

        Returns:
            int: megacredits variation
        """
        meg = 0
        built = identifierextractor(self.invertedcardselector("placement", "builded"))
        meg = 3*len(built)
        return meg

    def return_discarded_defender(self):
        """ return discarded defender to hand

        Returns:
            int: megacredits variation
        """
        discarteddefender = []
        discarded = identifierextractor(self.invertedcardselector("placement", "discard"))
        for discarted in discarded:
            if self.cardselector(discarted)[0][2] == "defender":
                discarteddefender.append(discarted)
        if len(discarteddefender) > 0:
            returned = random.choice(discarteddefender)
            self.tablemodifier(returned, "hitted", 0)
            self.tablemodifier(returned, "placement", "hand")
        return 0
    
    def return_discarded_building(self):
        """ return discarded building to hand
        
        Returns:
            int: megacredits variation
        """
        discartedbuilding = []
        discarded = identifierextractor(self.invertedcardselector("placement", "discard"))
        for discarted in discarded:
            if self.cardselector(discarted)[0][2] == "build":
                discartedbuilding.append(discarted)
        if len(discartedbuilding) > 0:
            returned = random.choice(discartedbuilding)
            self.tablemodifier(returned, "hitted", 0)
            self.tablemodifier(returned, "placement", "hand")
        return 0
    
    def gain_per_mine(self):
        """ gain megacredits per mine in play
        
        Returns:
            int: megacredits variation
        """        
        meg = 0
        built = identifierextractor(self.invertedcardselector("placement", "builded"))
        for b in built:
            if self.cardselector(b)[0][7] == 1:
                meg +=10
        return meg
    
    def gain_per_colony(self):
        """ gain megacredits per colony in play
        
        Returns:
            int: megacredits variation
        """
        meg = 0
        built = identifierextractor(self.invertedcardselector("placement", "builded"))
        for b in built:
            if self.cardselector(b)[0][5] == -1:
                meg += 20
        return meg
    
    def gain_per_lab(self):
        """ gain megacredits per lab in play
        
        Returns:
            int: megacredits variation
        """
        meg = 0
        built = identifierextractor(self.invertedcardselector("placement", "builded"))
        for b in built:
            if self.cardselector(b)[0][10] == 1:
                meg = 50
        return meg
    
    def halve_money(self):
        """ lose megacredits per building
        
        Returns:
            int: megacredits variation
        """
        meg = 0
        built = identifierextractor(self.invertedcardselector("placement", "builded"))
        for b in built:
            if self.cardselector(b)[0][5] == -1:
                meg -= 10
        return meg
        
    def tax(self):
        """ lose megacredits per building
        
        Returns:
            int: megacredits variation
        """
        meg = 0
        built = identifierextractor(self.invertedcardselector("placement", "builded"))
        meg = -2*len(built)
        return meg
        
            
