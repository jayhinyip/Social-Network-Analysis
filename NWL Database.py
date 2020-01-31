#This creates a new database called the network database that stores all the employees network lists as their own table. the name of the table is in the form "nw'_id_'"
# Its in the form (Target_ID, Weight_in, Weight_out)

import pandas as pd
import numpy as np
import pymysql
from makeNetwork import makeNetwork
db = pymysql.connect(
    host = "localhost",
    user = "root",
    passwd= "root",
    database="testdatabase",
autocommit = True)

mycursor = db.cursor()
mycursor.execute("CREATE DATABASE NWdatabase") #creates NW database

nwdb = pymysql.connect(
    host = "localhost",
    user = "root",
    passwd= "root",
    database="NWdatabase",
autocommit = True)

data = pd.read_excel('SNA_DATA.xlsx')


nwcursor = nwdb.cursor()

#Calls list of unique IDs

mycursor.execute("SELECT ID FROM SIMPLEID")
IDlist =[]
for x in mycursor:
    IDlist.append(x[0])

def CreateNWtable(ID): #statement for making a table of that id (the nw is added because for some reason some id strings were unable to be made into table names directly; to fix this we added nw before all the ids as explained above)
    return "CREATE TABLE nw" + ID + " (TargetID VARCHAR(50) PRIMARY KEY, Weight_in int, Weight_out int )"

def POPNWLTable(ID,Direction):#statment to insert rows into network list
    return "INSERT INTO nw" + ID + " (TargetID, Weight_"+ Direction +" ) VALUES(%s,%s)"


for i in range(len(IDlist)):
    nwcursor.execute(CreateNWtable(str(IDlist[i]))) #Creates table
    (G, labels, edgeThicc, n_nodes, NWL) = makeNetwork(str(IDlist[i]), 'Local', data) #Creates network (we need the Node weight list

    for j in range(len(NWL)):

        if str(IDlist[i]) == (str(NWL[j][0])): #Nodeweightlist contains messages going both in and out of target node; this code delineates between them and adds to the correct weight column
                nwcursor.execute(POPNWLTable(IDlist[i],'Out'), (str(NWL[j][1]), NWL[j][2])) #WORK REQUIRED: All networks only have either ingoing or outgoin messages. Change from insert into statement to maybe update statement
        else:
                nwcursor.execute(POPNWLTable(IDlist[i],'In'), (str(NWL[j][0]), NWL[j][2]))


