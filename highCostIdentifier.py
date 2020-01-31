#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import heapq, operator, pprint, time, matplotlib, community
from community import community_louvain
from modularity import modularity
import numpy as np
from simrank import simrank
import collections as cl





def highCostIdentifier(G,n):
    '''works off assumption that high betweeness makes a person a "broker"
     brokers are expensive (time/cost) to replace, regardless of influence or
     position within business. Does not need to consider weights of connections
     '''
    # brokers
    betCent = nx.betweenness_centrality(G, endpoints=True, weight='weight')

    # return top 'n' people based of their betweenness measures
    return heapq.nlargest(n, betCent.items(), key=lambda i: i[1])

