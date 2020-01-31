import pandas as pd
import numpy as np
import pymysql

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
ID = input()

nwcursor.execute(CallNWTStat(ID))

for x in nwcursor:
    print(x)