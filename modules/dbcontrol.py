import sqlite3

class DBControl():
    
    
    def __init__(self,databse):
        """Data Base Control class

        Args:
            databse (db): Deck database 
        """
        
        self.conector = databse
        self.pointer = self.conector.cursor()
        self.tuplavista = ()
        self.lista_enganche = []
    
    def tablemodifier(self, identif, aspect, newaspect):
        """Table values modifier

        Args:
            identif (int): entry identification
            aspect (str): aspect to modify
            newaspect (any): Modified aspect
        """
        
        changetuple = (newaspect, identif)
        column = str(aspect)
        change = "UPDATE deck SET "+column+" = ? WHERE id=?"
        
        self.pointer.execute(change, changetuple)
        self.conector.commit()
        
    def cardselector(self, identif):
        """Table values targeter for exporting

        Args:
            identif (int): entry identification

        Returns:
            list: entry data identifications
        """
        
        databsesearcher = "SELECT * FROM deck WHERE id=?"
        self.pointer.execute(databsesearcher, (identif,))
        targetcard = self.pointer.fetchall()
        
        return targetcard
    
    
    
    
    
    def invertedcardselector(self, aspect, value):
        
        
        databsesearcher = "SELECT id FROM deck WHERE "+aspect+"=?"
        self.pointer.execute(databsesearcher, (value,))
        targetcard = self.pointer.fetchall()
        
        return targetcard
    
    def filteredaspectcardselector(self, aspect, value, searchedvalue):
        
        
        datasearcher = "SELECT "+searchedvalue+" FROM deck WHERE "+aspect+"=?"
        self.pointer.execute(datasearcher, (value,))
        targetcard = self.pointer.fetchall()
        return targetcard
    
    def invertedcardselectorordered(self, aspect, value, ordering):
        
        databsesearcher = "SELECT id FROM deck WHERE "+aspect+"=? ORDER by "+ordering+" DESC "
        self.pointer.execute(databsesearcher, (value,))
        targetcard = self.pointer.fetchall()
        
        return targetcard
        
    def genericdatabasequery(self, query):
        
        self.pointer.execute(query) 
        target = self.pointer.fetchall()
        
        return target  
    
    
    
def identifierextractor(identifiertuple):
    identifierlist = []
    for i in identifiertuple:
        identifierlist.append(i[0])
    return identifierlist
        
        
    
    
            
    
 
    