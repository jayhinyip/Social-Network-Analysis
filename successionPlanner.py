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
from makeNetwork import makeNetwork




def successionPlanner(target, df, n):
    '''compares all nodes in the network to a target node and returns simRank similarities.
    used to identify the people best placed to replace the target
    '''
    # create targets network (implicitly assuming best recplacements are gonna be in same department)
    # but should probably be 'global' -> run once -> stored in db -> queried when needed
    (targetG, labels, edgeThicc,n_nodes,NWL) = makeNetwork(target, 'Local', df)

    # make the local networks of everyone in the targets local network
    localNets = []
    for node in targetG.nodes():
        (localG, labels, edgeThicc,n_nodes,NWL) = makeNetwork(node, 'Local', df)
        localNets.append(localG)


    mother = nx.compose_all(localNets)

    # run simrank (taken from https://github.com/hhchen1105/networkx_addon)
    # didnt get time to look into the appropriateness of using simRank in this context to
    # compare the graphs, should research if a measure like ASCOS or ASCOS++ is better.
    # extremely expensive to run.
    sim = simrank(mother) 
    simDict = dict(sim[target])

    # grab top n values in dict and take 2nd index onwards cause 1st is self
    candidates = heapq.nlargest(n, simDict.items(), key=lambda i: i[1])[1:]

    # collect labels for top n
    labels = {}
    for ind in range(len(candidates)):
        labels[candidates[ind][0]] = str(ind+1) + ' - ' + candidates[ind][0]
    labels[target] = 'Target'

    plotFlag = False
    if plotFlag:
        pos = nx.spring_layout(mother, k=0.1)
        plt.figure(figsize=(30,15))
        nx.draw(mother, pos, with_labels=False, alpha=0.8)
        nx.draw_networkx_nodes(mother, pos,
                               nodelist=[target],
                               node_color='r',
                               node_size=250,
                           alpha=0.8)
        nodelist = [x[0] for x in candidates]
        nx.draw_networkx_nodes(mother, pos,
                               nodelist=nodelist,
                               node_color='r',
                               node_size=250,
                           alpha=0.8)
        nx.draw_networkx_labels(mother, pos, labels, font_size=20)

    return (candidates, labels)
