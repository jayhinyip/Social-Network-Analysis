#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import collections as cl
import datetime as dt
from makeNetwork import makeNetwork




filePath = 'SNA_DATA.xlsx'
df=pd.read_excel(filePath)



#### data cleaning
# should remove all conference room-type emails
# look into missing attribute correction


# calculates temporal responsiveness of a given employee
def Responsiveness(target, timeLimit, df):

    # convert date attributes to dt objects for calcs
    dateList = []
    for serialNum in df['SerialNumber']:

        dtObj = dt.datetime.strptime(serialNum[:6], '%y%m%d') #why why oh why is this here you retardds
        dtObj = int(serialNum[:6])
        dateList.append(dtObj)


    recievedCount = 0
    previousID = 0
    responseCount=0

    # loop through entire dataframe
    for ind in range(0,len(df['Sender'])):

        # check the recipient was the intended user
        if target == df['Recipient'].iloc[ind]:
            # store sender
            sender_b = df['Sender'].iloc[ind]
            # incremement count
            recievedCount += 1
            recipient_c = df['Recipient'].iloc[ind]

            # loop through from the current row onwards to try and find response email
            for ind2 in range(ind+1, len(df['Sender'])):

                # check we're within the current time limit for considering a response
                temp1 = dateList[ind] - dateList[ind2]
                if (temp1 > timeLimit):
#                 if ((dateList[ind] - dateList[ind2]).days > timeLimit) or ((dateList[ind] - dateList[ind2]).days < 0):
#                     print('days', (dateList[ind] - dateList[ind2]).days)
                    break

                # else check the sender-recipient arrangment is in reverse order
                # this was assumed to mean an email was responded to
                else:
                    sender_d = df['Sender'].iloc[ind2]
                    recipient_e = df['Recipient'].iloc[ind2]
                    # check not double-counting
                    if dateList[ind] is previousID:
                        test = 67
                    
                    else:
                        # reverse order for sender recipient check
                        if (sender_b is recipient_e) and (recipient_c is sender_d):
                            responseCount+=1
                            previousID = dateList[ind]
                            break
    
    # return total response rate
    if recievedCount == 0:
        response = 1
    else:
        response = responseCount/recievedCount

    return response
