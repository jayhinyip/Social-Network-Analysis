#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import heapq, operator, pprint, time, matplotlib, community
from modularity import modularity
import numpy as np
from simrank import simrank
import collections as cl

# Creates the networks used by all the auxilliary functions, based off a target user
# and desired level (office/role etc)
def makeNetwork(target, level, df):


    # get correct level of network
    if level == 'Local':
        # find all rows where target is sender or receiver and
        # reduce df to only the those rows
        dfTarget = df.loc[(df['Sender'] == target) | (df['Recipient']==target)]

    elif level == 'Global':
        dfTarget = df


    else:
         # find targets office/dpartment/whatever
        targetLevel = df.loc[(df['Sender'] == target)][level].iloc[0]
        # check if level of target exists (i.e. sender XYZ has a non-blank 'SendersDepartment')
        while True:
            #### be careful with this if statement, didnt get time to test properly (i.e. 'if targetLevel' vs 'if targetLevel None' etc)
            if targetLevel: 
                break
            else:
                raise Exception('Target {} is missing attribute {}. try agian'.format(target, level))
        # reduce df to only the targets office/department/whatever
        dfTarget = df.loc[(df[level]==targetLevel)]



    # get edges
    edges = []
    for temp in zip(dfTarget['Sender'], dfTarget['Recipient']):
        edges.append(tuple(temp))

    # get edge weights {'node1', 'node2': numberOfEmails} (unordered)
    edgesWeight = cl.Counter(map(frozenset, edges))
    G = nx.Graph()
    nodeWeightList = []
    for edge in edgesWeight:
        temp = list(edge)
        if len(temp) < 2: ## CATCH FOR SENDING EMAIL TO SELF
            continue
        nodeWeightList.append((temp[0], temp[1], edgesWeight[edge]))

    # add edges with weight attr
    G.add_weighted_edges_from(nodeWeightList)

    # add distance attribute to edges, defined as 1/weight
    distanceDict = {(e1, e2): 1 / weight for e1, e2, weight in G.edges(data='weight')}
    nx.set_edge_attributes(G, distanceDict, 'distance')




    # get nodes (think this is actually unnecesary and its smart enough to not add duplicates?)
    dfUnique = dfTarget.drop_duplicates(subset = ['Sender', 'Recipient'])
    IDList = list(dfUnique['Sender'])

    # add nodes
    G.add_nodes_from(IDList)



    # grab only target for labelling/colouring
    labels = {}
    for node in G.nodes():
        if node == target:
            labels[node] = 'Target - ' + target


    # get list of thickness for edges based off weights
    edges = G.edges()
    edgeThicc = [G[u][v]['weight'] for u,v in edges]
    n_nodes = (len(G.nodes()))
    return (G, labels, edgeThicc, n_nodes,nodeWeightList)
4