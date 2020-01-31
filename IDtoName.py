import pandas as pd
import numpy as np
import pymysql

# Read namelist excel file
xls = pd.ExcelFile('NameIDList.xlsx')
df = xls.parse(xls.sheet_names[0])

# Create namelist
namelist = []

namelist.append(df['ID'].tolist())
namelist.append(df['First Name'].tolist())
namelist.append(df['Last Name'].tolist())
namelist.append(df['Jobtitle'].tolist())
namelist1 = list(map(list, zip(*namelist)))

def IDtoName(ID):
    name = []
    for sublist in namelist1:
        if sublist[0] == ID:
            firstname = sublist[1]
            lastname = sublist[2]
            jobtitle = sublist [3]
            fullname = str(firstname) + ' ' +str(lastname)
            jobtitle = str(jobtitle)
            name = [fullname, jobtitle]
    return name

