
import csv
import sqlite3


filename = "modules\\cards.csv"


fields = []
rows = []



def csvlistconverter(filename):

    


    fields = []
    rows = []

<<<<<<< HEAD
=======
    
>>>>>>> 4ee3f75e3d4a981205cf86f6585f6f7c35a2fe8a
    with open(filename, "r") as csvfile:
        
        csvreader = csv.reader(csvfile)

        
        fields = next(csvreader)

        
        for row in csvreader:
            rows.append(row)

        
    
    return fields, rows

def cardextraction(cardsroute):
    decki = []
    
    notcare, individual = csvlistconverter(cardsroute)
    for cd in individual:
        if cd[2] != "":
            cou = cd[2]
            cd.pop(2)
            for num in range(int(cou)):
                
                name = cd[0]+str(num)
                temp = cd[1:]
                temp.insert(0,name)
                decki.append(temp)
                
                
        else:
            cd.pop(2)
            decki.append(cd)
    
    
                
    return decki


def conection_sql():
    global conector
    conector = sqlite3.connect("currentgame.db")
    return conector

def tabledropper(conection):
    pointer = conection.cursor()
    dropping = "DROP TABLE IF EXISTS deck"
    pointer.execute(dropping)
    conection.commit()
    dropping = "DROP TABLE IF EXISTS images"
    pointer.execute(dropping)
    conection.commit()
    

def tableconstructor(conection):
    pointer = conection.cursor()
    table = "CREATE TABLE IF NOT EXISTS deck(id INTEGER PRIMARY KEY AUTOINCREMENT, card TEXT NOT NULL, type TEXT NOT NULL, income INTEGER, power INTEGER,  agrogen INTEGER,  defenders INTEGER, mining INTEGER, refinerie INTEGER, colonies INTEGER, labs INTEGER, notes TEXT, force INTEGER, hits INTEGER, placement TEXT, deckpos INTEGER, hitted INTEGER  )"
    pointer.execute(table)
    conection.commit()
    tableimages = "CREATE TABLE IF NOT EXISTS images(id INTEGER PRIMARY KEY AUTOINCREMENT, card TEXT NOT NULL, pict TEXT, descript TEXT )"
    pointer.execute(tableimages)
    conection.commit()
    


<<<<<<< HEAD
def loaddb(coneccion, tupleload):

    

    pointer = coneccion.cursor()
=======

def loaddb(conection, tupleload):

    

    pointer = conection.cursor()
>>>>>>> 4ee3f75e3d4a981205cf86f6585f6f7c35a2fe8a
    load = "INSERT INTO deck(card, type, income, power, agrogen, defenders, mining, refinerie, colonies, labs, notes, force, hits, placement, deckpos, hitted) VALUES (?,?,?,?,?,?,?,?,?,?, ?,?,?,?,?,?)"
    pointer.execute(load, tupleload)
    coneccion.commit()
    
    
def loadimages(coneccion, tupleimages):
    
    pointer = coneccion.cursor()
    load = "INSERT INTO images(card, pict, descript) VALUES (?,?,?)"
    pointer.execute(load, tupleimages)
    coneccion.commit()
    

def massiveloader(conector, deck):
    for x in deck:
        row = x
        
        income = int(row[2])
        power = int(row[3])
        agrogen = int(row[4])
        defenders = int(row[5])
        mining = int(row[6])
        refinerie = int(row[7])
        colonies = int(row[8])
        labs = int(row[9])
        force = int(row[11])
        hits = int(row[12])
        loadtuple = (row[0], row[1], income, power, agrogen, defenders, mining, refinerie, colonies, labs, row[10], force, hits, row[13], row[14], row[15])
        
        loaddb(conector, loadtuple)
        
        loadimagestuple = (row[0], row[16], row[17])
        loadimages(conector, loadimagestuple)
    


if __name__ == "__main__":
    conector = conection_sql()
    tabledropper(conector)
    tableconstructor(conector)
    deck = cardextraction(filename)
    massiveloader(conector, deck)
    
    
    
    
        
    
    
    
    


    

    


