# importing csv module
import csv
import sqlite3

# csv file name
filename = "modules\\cards.csv"

# initializing the titles and rows list
fields = []
rows = []



def csvlistconverter(filename):
# csv file name
    

# initializing the titles and rows list
    fields = []
    rows = []

    # reading csv file
    with open(filename, "r") as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
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
    


def carga_sistema(apellidoc, nombrec, cursoc, tp1c=0, tp2c=0, tp3c=0, examenc=0):
    
    notac = round((tp1c + tp2c + tp3c) / 6 + examenc / 2, 0)
    tupla_carga_sist = (apellidoc, nombrec, cursoc, tp1c, tp2c, tp3c, examenc, notac)
    
    return tupla_carga_sist


def loaddb(coneccion, tuplacarga):

    

    apuntador = coneccion.cursor()
    carga = "INSERT INTO deck(card, type, income, power, agrogen, defenders, mining, refinerie, colonies, labs, notes, force, hits, placement, deckpos, hitted) VALUES (?,?,?,?,?,?,?,?,?,?, ?,?,?,?,?,?)"
    apuntador.execute(carga, tuplacarga)
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
    
    
    
    
        
    
    
    
    


    

    


