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


def impactRecommender(target, G, df, n):
    '''
    1 - confirm target is not highly connected
            defined as not being in top nth percentile of all nodes in terms of betweenness and closeness
    2 - determine key influencers and ensure target is not one of them
    3 - check if target is connected with top influencers
    4 - check influencers are not in close proximity to target
    5 - scan for communities that target is loosely part of
    6 - find other people in the same communities that have high betweenness with key influencers
    '''
    # 11111111111111111111111111
    # make list of every nodes centraily and check we're not in the top nth percentile
    closCent = nx.closeness_centrality(G, distance='distance')
    betCent = nx.betweenness_centrality(G, normalized=True, endpoints=True, weight='weight')

    # expensive conversion to list, should be replaced
    closCentValues = list(closCent.values())
    betCentValues = list(betCent.values())

    # sort highest->lowest
    closCentValues.sort(reverse=True)
    betCentValues.sort(reverse=True)

    # check theyre not well connected
    cutOff1 = 85
    if closCent[target] > np.percentile(closCentValues, cutOff1) and betCent[target] > np.percentile(betCentValues, cutOff1):
    #    raise Exception(
    #        '''Closeness Centrality of Employee = {}. Cutoff percentile = {}
#        \Betweenness Centrality of Employee = {}. Cutoff percentile = {}
#        \n------------------------already BNOC--------------------------'''.format(closCent[target],
#                                                                                   np.percentile(closCentValues, cutOff1),
#                                                                                   betCent[target],
#                                                                                   np.percentile(betCentValues, cutOff1)
    #                                                                              )
        #)
        middleMen = 'invalid'
        return middleMen



    # 22222222222222222222222
    # find individuals with high eig, and check target isnt one of them
    eigCent = nx.eigenvector_centrality(G, weight='weight')
    eigCentValues = list(eigCent.values())
    eigCentValues.sort(reverse=True)
    cutOff2 = 85
    if eigCent[target] > np.percentile(eigCentValues, cutOff2) and closCent[target] > np.percentile(closCentValues, cutOff2):
        raise Exception(
            '''cutoff = {}. target = {}
            ------------------------already BNOC--------------------------'''.format(np.percentile(eigCentValues, cutOff2), eigCent[target])
        )



    # 333333333333333333333333333
    # find top half of influencers off eigCent
    topInfluencers = []
    cutOff3 = 80
    for node in eigCent:
        if eigCent[node] > np.percentile(eigCentValues, cutOff3): # ---------------------------------- prob change this to eig and closeness cutoff
            topInfluencers.append(node)

    # check how many of the top influencers are in bro's local network
    (targetG, labels, edgeThicc,n_nodes) = makeNetwork(target, 'Local', df)
    targetLocalNodeList = list(targetG.nodes())
    # check crossover between local connections and influencers (i.e what influencers does target already know)
    intersection = list(set(topInfluencers) & set(targetLocalNodeList))
    if target in intersection:
        intersection.remove(target)




    # 4444444444444444444444444444444444444444
    # get proximity of known influencers to bro (degree separation) (unweighted)
    pathLengths = {}
    for node in intersection:
        # if theyre 1 degree away, she needs no help connecting to them
        if nx.shortest_path_length(G, source=target, target=node) > 1:
            pathLengths[node] = nx.shortest_path_length(G, source=target, target=node)

    plotFlag = False
    if plotFlag:
        plt.figure(figsize=(20,10))
        nx.draw(targetG, with_labels=True)
        pprint.pprint(pathLengths)
        plt.figure(figsize=(20,10))
        pos = nx.spring_layout(G, k=0.1)
        nx.draw(G, pos, with_labels=False, alpha=0.8)
        nx.draw_networkx_nodes(G, pos,
                               nodelist=[target],
                               node_color='g',
                               node_size=600,
                           alpha=0.8)
        nx.draw_networkx_nodes(G, pos,
                               nodelist=topInfluencers,
                               node_color='r',
                               node_size=200,
                           alpha=0.8)
        nx.draw_networkx_nodes(G, pos,
                               nodelist=intersection,
                               node_color='k',
                               node_size=100,
                           alpha=0.8)
        nx.draw_networkx_labels(G, pos, labels, font_size=20)




    # 55555555555555555555555555555555
    #identify communities
    (communityDF, nodeDict) = commDetector(G)

    # find which communtiies target is in
    targetComms = [x for x in nodeDict if target in nodeDict[x]]




    # 6666666666666666666666666
    # find people in targetComms that have high betweenness with influencers

    # find distance between everyone in targetCOmms with everyone in topInfluencers
    # should is be weighted by rank of influencer?


    pathCutOff = 1
    middleMen = []

    for node in topInfluencers:
        for communityN in targetComms:
            for communityMember in nodeDict[communityN]:
                # distance from influencer to community member
                if nx.shortest_path_length(G, source=communityMember, target=node) < pathCutOff+1:
                    middleMen.append(communityMember)
                    if len(middleMen) > n-1: return middleMen




    return middleMen





def commDetector(G):
    partition=community_louvain.best_partition(G, weight='weight')
    values=[partition.get(node) for node in G.nodes()]
    list_com=partition.values()

    # Creating a dictionary like {community_number:list_of_participants}
    dict_nodes={}

    # Populating the dictionary with items
    for each_item in partition.items():
        community_num=each_item[1]
        community_node=each_item[0]
        if community_num in dict_nodes:
            value=dict_nodes.get(community_num) + ' | ' + str(community_node)
            dict_nodes.update({community_num:value})
        else:
            dict_nodes.update({community_num:community_node})


    # Creating a dictionary like {community_number:list_of_participants}
    dict_nodes2={}

    # Populating the dictionary with items
    for each_item in partition.items():
        community_num=each_item[1]
        community_node=each_item[0]
        if community_num in dict_nodes2:

            temp = dict_nodes2[community_num]
            if community_node not in temp:
                nodeList = temp.append(community_node)
        else:
            dict_nodes2.update({community_num:[community_node]})


    # Creating a dataframe from the diet, and getting the output into excel
    community_df=pd.DataFrame.from_dict(dict_nodes, orient='index',columns=['Members'])
    community_df.index.rename('Community_Num' , inplace=True)
    saveFlag = False
    if saveFlag:
        community_df.to_csv('Community_List_snippet.csv')

    # Creating a new graph to represent the communities created by the Louvain algorithm
    plotFlag = False
    if plotFlag:
        matplotlib.rcParams['figure.figsize']= [12, 8]
    G_comm=nx.Graph()

    # Populating the data from the node dictionary created earlier
    G_comm.add_nodes_from(dict_nodes)

    # Calculating modularity and the total number of communities
    mod=modularity(partition,G)


    # Creating the Graph and also calculating Modularity
    if plotFlag:
        matplotlib.rcParams['figure.figsize']= [12, 8]
        pos_louvain=nx.spring_layout(G_comm)
        nx.draw_networkx(G_comm, pos_louvain, with_labels=True,node_size=160,font_size=11,label='Modularity =' + str(round(mod,3)) +
                            ', Communities=' + str(len(G_comm.nodes())))
        plt.suptitle('Community structure (Louvain Algorithm)',fontsize=22,fontname='Arial')
        plt.box(on=None)
        plt.axis('off')
        plt.legend(bbox_to_anchor=(0,1), loc='best', ncol=1)
    return (community_df, dict_nodes2)
