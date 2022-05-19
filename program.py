import sqlite3 as SQL

#Establish Database Connection
conn = SQL.connect("words.db")
co = conn.cursor()


#Program to Assits with Words With Friends
badCharacters = ["-", "'","/"," ",'"',"1","2","3","4","5","6","7","8","9","_"]
query = []


def findWord():
    #Propmpts User For Input
    #Gets Length of Word
    word = ""
    print("Enter Length of the Word:", end = " ")
    length = int(input())

    #Checks word input
    while True:
        badWord = False
        print("Enter unknown letters as a 0")
        print("Enter Word to Search For:", end = " ")
        word = str(input())
        if len(word) != length:
            badWord = True
        for c in badCharacters:
            if c in word:
                badWord = True
        if not badWord:
            break
        else:
            print("Please enter valid input!")

    #Puts right characters into word
    word = word.replace("0","_")
    word = word.upper()
    #Queries for word
    co.execute("SELECT Word FROM Words INNER JOIN Information ON Words.ID = Information.ID WHERE Word LIKE ? AND Information.Length = ?", (word, length,))
    row = co.fetchall()

    #Prints out results
    resultNum = len(row)
    print(f"There are {str(resultNum)} results!")
    if resultNum == 0:
        exit()

    count = 1
    for i in row:
        if i:
            print(str(count) +  ". " + i[0])
            query.append(i[0])
            count += 1
    cho()
    
#Redfine Search or Choose Word
def cho():
    print("Would you like to choose a word, redefine a word, or exit?")
    print("CHOOSE/REDEFINE/EXIT:", end = " ")
    choice = input()
    if choice.upper() == "CHOOSE":
        #Finds which word is used
        count = 1
        for i in query:
            print(str(count) +  ". " + i)
            count += 1
        print("Which word did you use?")
        print("(If none enter 0)", end = " ")
        ans = input()
        if ans == "0":
            exit()
        #Gets current used value
        co.execute("SELECT Uses, Information.ID FROM Information INNER JOIN Words ON Words.ID = Information.ID WHERE Word = ?", (ans.upper(),))
        uses = co.fetchone()
        id = uses[1]
        uses = uses[0]
        uses = uses + 1
        co.execute("UPDATE Information SET Uses = ? WHERE ID = ?", (uses, id,))
        conn.commit()
        exit()
    elif choice.upper() == "REDFINE":
        findWord()
    elif choice.upper() == "EXIT":
        exit()    
    else:
        print("Please try again!")
        cho()
        return()

findWord()


