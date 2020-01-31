#!/usr/bin/env python
# coding: utf-8
#$#$#$#$#$#
# In[ ]:


import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import heapq, operator, pprint, time, matplotlib, community
from modularity import modularity
import numpy as np
from simrank import simrank
import collections as cl


# Function to calculate the ratio of outgoing to ingoing emails for a given 
# 'target' (str) within a dataframe, 'df'. Does not take into account one email
# being sent to multiple targets (i.e. counts these as > 1 email) - ran out of 
# time, but simple fix.
def evenness(target, df):
    
    # num sent/recieved
    sentNum = len(df.loc[(df['Sender'] == target)])
    recNum = len(df.loc[(df['Recipient'] == target)])
    
    # catch for dividing by 0
    if recNum == 0: return 1
    
    # returned as normalised (sent:recieved) ratio, ideally 0.5
    return sentNum/(sentNum+recNum)

