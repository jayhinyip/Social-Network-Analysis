import pandas as pd
import numpy as np
import pymysql
from evenness import evenness


db = pymysql.connect(
    host = "localhost",
    user = "root",
    passwd= "root",
    database="testdatabase",
autocommit = True)
data = pd.read_excel('SNA_DATA.xlsx')

mycursor = db.cursor()
IDs = ['0007f30bba2eef3df091a632e638320d','001ad6cfbf0481b2d29880161cbb3936','00bc23d8afb357d9340dd38f5226a61b']


#mycursor.execute("ALTER TABLE SIMPLEID ADD COLUMN Evenness float") # Adds Eveness column to table

evenesslist = [] # Caluculates evenness

xls = pd.ExcelFile('SNA_DATA.xlsx')

# Create dataframes
df = xls.parse(xls.sheet_names[0])
df = df.drop_duplicates('Sender', keep='first')
df2 = xls.parse(xls.sheet_names[0])
df2 = df2.drop_duplicates('Recipient', keep='first')

# Create sender and recipent and its respective office & job title lists
senderboys= []
recipientboys = []

senderboys.append(df['Sender'].tolist()) #Gets list of all unique senders with office and title
senderboys.append(df['SendersOffice'].tolist())
senderboys.append(df['SendersJobTitle'].tolist())
recipientboys.append(df2['Recipient'].tolist())#Gets list of all unique recipients with office and title
recipientboys.append(df2['RecipientsOffice'].tolist())
recipientboys.append(df2['RecipientsJobTitle'].tolist())

# Drop any duplicates in recipient list
uniqueRecipientList = [n for n in zip(*recipientboys) if n not in zip(*senderboys)] #we dont know how this works but it drops all the recipientboys already in senderboys list
uniqueRecipientList2 = list(map(list, zip(*uniqueRecipientList))) #transposes unique recipient list for us to add to the senderboys list

# Transpose ID list from vector to a list into 3 columns
ID_list = np.hstack((senderboys,uniqueRecipientList2)) # adds senderboys and uniquerecipient list to get a list of all unique IDs in the email database; is 3 rows and 1800ish columns
print(ID_list)

ID_list1 = list(map(list, zip(*ID_list)))#transpose ID_list into 3 columns and 1800ish rows



for i in range(len(ID_list1)): #Calculates evenness for all ids
    evennesses = evenness(str(ID_list1[i][0]), data)
    print(str(evennesses))
    evenesslist.append(evennesses)

def sqlevennessstatement(ID,Eveness): #update evenness statement
    return "UPDATE SIMPLEID set Evenness ="+str(Eveness) + " where ID = " + "'" + ID +"'"

for i in range(len(ID_list1)): #updates the SIMPLEID table
    mycursor.execute(sqlevennessstatement(str(ID_list1[i][0]),evenesslist[i]))
    db.commit()