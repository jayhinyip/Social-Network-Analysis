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

nwdb = pymysql.connect(
    host = "localhost",
    user = "root",
    passwd= "root",
    database="NWdatabase",
autocommit = True)


nwcursor = nwdb.cursor()



def CallNWTStat(ID):
    return "SELECT * FROM table" + ID

print('Input ID')
ID = 'f39c6d6653abc0a30eea87256265e769'

nwcursor.execute(CallNWTStat(ID))
NWList = []
for x in nwcursor:
    NWList.append(x)

def IDBranchlookup(ID):
    return "SELECT Branch FROM SIMPLEID WHERE ID = " + "'" + ID + "'"

Branchweight = [] #Create list of Branches that user has emailed and add up all the emails sent to that branch
branchlist=[]
for i in range(len(NWList)):
    mycursor.execute(IDBranchlookup(NWList[i][0]))
    for x in mycursor:
        branch = x[0]
    branchwei = (branch,NWList[i][1])
    if branch not in branchlist:
            branchlist.append(branch)
            Branchweight.append(branchwei)


    else:
        for j in range(len(Branchweight)):
            if str(branch) == str(Branchweight[j][0]):
                listbranch = list(Branchweight[j])
                listbranch[1] = listbranch[1] + NWList[i][1]
                Branchweight[j] = tuple(listbranch)


#Find if user has sent emails to their own branch

mycursor.execute(IDBranchlookup(ID))
for x in mycursor:
    targetbranch = x[0]

print(Branchweight)


if targetbranch not in branchlist:
        print('This dude is a loser')
else:
        totalweight = 0
        for j in range(len(Branchweight)):
            totalweight =  totalweight + Branchweight[j][1]
            if str(branch) == str(Branchweight[j][0]):
                officeweight = Branchweight[j][1]

        percentage = int(officeweight/totalweight*100)

        print("% sent to own office = " + str(percentage) + '%')
