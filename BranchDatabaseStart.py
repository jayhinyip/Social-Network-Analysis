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

mycursor.execute("CREATE DATABASE BranchDatabase") # Initialises Branch database - comment out after created

brdb = pymysql.connect(
    host = "localhost",
    user = "root",
    passwd= "root",
    database="BranchDatabase",
autocommit = True)

brcursor = brdb.cursor()

#Creates list of unique Branches
mycursor.execute("SELECT BRANCH FROM SIMPLEID")
branchlist =[]
for x in mycursor:
    branchlist.append(x[0])
branchlist = list(dict.fromkeys(branchlist)) #Drops duplicates from branchlist

def callidbranch(branch): # statement for calling list of ids who are at that branch
    return "SELECT ID, BetweenessCent, ClosenessCent, EigCent FROM SIMPLEID WHERE BRANCH = " +"'" + branch +"'"

def Createbranchtable(branch): #statement for making a table of that branch
    return "CREATE TABLE " + branch + " (TargetID VARCHAR(50) PRIMARY KEY, BetweenessCent float, CLoseCent float, EigenvectorCent float)"

def POPbranchTable(branch): #statment to insert rows into branch
    return "INSERT INTO " + branch + " (TargetID, BetweenessCent, CLoseCent, EigenvectorCent) VALUES(%s,%s,%s,%s)"


count = 0

uniquetableidlist = []

badwords = [" ", "-", "&", "(", ")", ",", "/", "_", "__"] #list of characters that will be ommited because they are invalid table names

for i in range(len(branchlist)):

    mycursor.execute((callidbranch(str(branchlist[i])))) #calls list of ids who are at that branch
    uniquebranchids = [] #initalises vector of  ids that for each branchlist[i]
    for x in mycursor:
        uniquebranchids.append(x) #populates vector with list of people who are at that branch
    count = count +1
    print(count)

    #Removes any characters in 'badwords' from table names
    for t in range(len(badwords)):
        if badwords[t] in branchlist[i]:
            branchlist[i] = branchlist[i].replace(badwords[t],"_")

    #Removes any double underscores after filtering badwords
    if "__" in branchlist[i]:
        branchlist[i] = branchlist[i].replace("__", "_")

    #Removes trailing underscores
    if branchlist[i].endswith('_'):
        fix = branchlist[i]
        branchlist[i] = fix[:-1]

    # If branchname contains 'logged' (e.g. Jeff_McGrath_logged_on_at_4:20:00_am_with_fred) classify branch as "nan"
    if "logged" in branchlist[i]:
        branchlist[i] = "nan"

    print(branchlist[i])

    # Checks if a table for branchlist[i] already exists
    if branchlist[i] in uniquetableidlist:
        for j in range(len(uniquebranchids)):
            #Populate table with IDs and centrality metrics
            brcursor.execute(POPbranchTable(branchlist[i]), (str(uniquebranchids[j][0]),uniquebranchids[j][1],uniquebranchids[j][2],uniquebranchids[j][3]))

    # If a table for branchlist[i] does not exist
    else:
        # Creates branchlist[i] table and populate
        uniquetableidlist.append(branchlist[i])
        brcursor.execute((Createbranchtable(str(branchlist[i]))))
        for j in range(len(uniquebranchids)):
            brcursor.execute(POPbranchTable(branchlist[i]), (str(uniquebranchids[j][0]),uniquebranchids[j][1],uniquebranchids[j][2],uniquebranchids[j][3]))