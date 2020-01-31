import pandas as pd
import csv
import numpy as np
from makeNetwork import makeNetwork
import pymysql
from hiPoIdentifier import Responsiveness

db = pymysql.connect(
    host = "localhost",
    user = "root",
    passwd= "root",
    database="testdatabase",
autocommit = True)
data = pd.read_excel('SNA_DATA.xlsx')


responselist =[]

mycursor = db.cursor()

mycursor.execute("SELECT ID FROM SIMPLEID") # Calls List of all ids
IDlist =[]
for x in mycursor:
    IDlist.append(x[0])

mycursor.execute("ALTER TABLE SIMPLEID ADD COLUMN Response float") # Adds response Column
def returnresponse(ID): # Returns response column
    return "SELECT Response FROM SIMPLEID WHERE ID = " + "'" + ID + "'"
mycursor.execute(returnresponse(IDlist[3]))
for x in mycursor:
    print(x)
=======

for i in range(len(IDs)): #
        response = Responsiveness(str(IDs[i]), 2, data)
        responselist.append(response)

def sqlevennessstatement(ID, Eveness):
            return "UPDATE SIMPLEID set Response =" + str(Eveness) + " where ID = " + "'" + ID + "'"

for i in range(len(IDs)):
    mycursor.execute(sqlevennessstatement(str(IDs[i]),responselist[i]))
