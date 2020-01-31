import pandas as pd
import numpy as np
import pymysql

brdb = pymysql.connect(
    host = "localhost",
    user = "root",
    passwd= "root",
    database="BranchDatabase",
autocommit = True)


brcursor = brdb.cursor()

def rankstatement(branch, Category):
    brcursor.execute('SELECT TargetID, BetweenessCent, CLoseCent, EigenvectorCent, RANK () OVER (ORDER BY '+ str(Category)+ ' DESC) '+ str(Category)+ '_rank FROM ' +str(branch))
    dag = []
    for x in brcursor:
        dag.append(x)
    return dag

