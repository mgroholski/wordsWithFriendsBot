import _sqlite3 as SQL
import csv

#Establishes Connection
conn = SQL.connect("words.db") 
c = conn.cursor()

#Clears table
c.execute("DELETE FROM Words")
c.execute("DELETE FROM Information")

#Populates data into table
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
badCharacters = ["-", "'","/"," ",'"',"1","2","3","4","5","6","7","8","9","0"]

for i in alphabet:
    with open("./Word lists in csv/" + i.capitalize() + "word.csv", "r") as file:
        read = csv.reader(file, delimiter = " ", quotechar = "|")
        try:
            for row in read:
                data = "".join(row)
                data = data.replace(" ", "")
                bad = False
                #Checks for bad symbols
                for ba in badCharacters:
                    if  ba in data:
                        bad = True
                if not bad:
                    data=data.upper()
                    #Check if repeat
                    c.execute('SELECT * FROM Words WHERE Word=?', (data,))
                    row = c.fetchall()
                    if not row:
                        l = len(data)
                        c.execute("INSERT INTO Words(Word) VALUES (?)",(data,))
                        c.execute('INSERT INTO Information(ID, Length, Uses) VALUES ((SELECT ID FROM Words WHERE Word = ?),?,0);', (data, l,))
        except UnicodeDecodeError:
            print("Unicode Error")
            continue
            
    
conn.commit()


