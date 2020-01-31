import pymysql
import pandas as pd
import numpy as np

db = pymysql.connect(
    host = "localhost",
    user = "root",
    passwd= "root",
    database="testdatabase"
)


xls = pd.ExcelFile('SNA_DATA.xlsx')
data = pd.read_excel('SNA_DATA.xlsx')

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
print('This is' +str(ID_list))

ID_list1 = list(map(list, zip(*ID_list)))#transpose ID_list into 3 columns and 1800ish rows


mycursor = db.cursor()
mycursor.execute("CREATE TABLE SIMPLEID (ID VARCHAR(50) PRIMARY KEY, Branch VARCHAR(100), Jobtitle VARCHAR(100))") #creates SIMPLEID table
#mycursor.execute("INSERT INTO IDLIST (ID, Branch,Jobtitle,Response,Evenness) VALUES (%s,%s,%s,%s,%s)", ("d7e68a0d48f04fbaa78dbc6ed7a28e9e","North Sydney - Mount Street","DIGITAL ENGINEER LEADZ",0.71,0.84))

#mycursor.execute("ALTER TABLE SIMPLEID CHANGE BRANCH BRANCH VARCHAR(100)")
#mycursor.execute("DESCRIBE IDLIST")
#mycursor.executemany('INSERT IGNORE into SIMPLEID (ID, Branch, Jobtitle) VALUES(%s, %s, %s)', ID_list1)
for i in range(len(ID_list1)):
    mycursor.execute("INSERT INTO SIMPLEID (ID, Branch, Jobtitle) VALUES(%s,%s,%s)",(str(ID_list1[i][0]), str(ID_list1[i][1]), str(ID_list1[i][2]))) #populates SIMPLEID table with id, branch and jobttiltle
    db.commit()

        #mycursor.execute("SELECT * FROM SIMPLEID WHERE ID = 'value1'")


#mycursor.execute("SELECT * FROM SIMPLEID")
for x in mycursor:
  print(x)