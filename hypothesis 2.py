import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import *
import seaborn as sns
from datetime import datetime
import time

#Import edge table from gephi
edge_table = pd.read_csv("retweet edges table.csv")
#Import botometer results
botometer_humans = pd.read_csv("humans.csv")['list'].tolist()
botometer_simple_bots = pd.read_csv("simple.csv")['list'].tolist()
botometer_sop_bots = pd.read_csv("sophisticated.csv")['list'].tolist()
#Assign classification to each edge
i = 0
edge_users = pd.DataFrame({'origin':[],'target':[], 'weight':[]})
target_class = ""
origin_class = ""
weight = ""

while i < len(edge_table):

    current_edge_users = []
    origin_user = edge_table.iloc[i,0]
    if (origin_user in botometer_humans):
        origin_class = "human"
    elif origin_user in botometer_simple_bots:
        origin_class = "simple bot"
    elif origin_user in botometer_sop_bots:
        origin_class = "sophisticated bot"
    else:
        origin_class = "missing"


    target_user = edge_table.iloc[i,1]
    if (target_user in botometer_humans):
        target_class = "human"
    elif target_user in botometer_simple_bots:
        target_class = "simple bot"
    elif target_user in botometer_sop_bots:
        target_class = "sophisticated bot"
    else:
        target_class = "missing"

    weight = edge_table.iloc[i,6]

    edge_users = edge_users.append({'origin':origin_class,'target':target_class, 'weight':weight}, ignore_index=True)
    i = i+1

i = 0
edge_classes= []
while i < len(edge_users):
    if edge_users.iloc[i,0] == "human" and edge_users.iloc[i,1] == "human":
        edge_type = "h-h"
        edge_classes.append(edge_type)
        if (edge_users.iloc[i,2] > 1):
            y = 0
            while y < (edge_users.iloc[i,2]-1):
                edge_classes.append(edge_type)
                y= y+1
    elif edge_users.iloc[i,0] == "human" and edge_users.iloc[i,1] == "simple bot":
        edge_type = "h-bb"
        edge_classes.append(edge_type)
        if (edge_users.iloc[i,2] > 1):
            y = 0
            while y < (edge_users.iloc[i,2]-1):
                edge_classes.append(edge_type)
                y= y+1
    elif edge_users.iloc[i,0] == "human" and edge_users.iloc[i,1] == "sophisticated bot":
        edge_type = "h-sb"
        edge_classes.append(edge_type)
        if (edge_users.iloc[i,2] > 1):
            y = 0
            while y < (edge_users.iloc[i,2]-1):
                edge_classes.append(edge_type)
                y= y+1
    elif edge_users.iloc[i,0] == "simple bot" and edge_users.iloc[i,1] == "human":
        edge_type = "bb-h"
        edge_classes.append(edge_type)
        if (edge_users.iloc[i,2] > 1):
            y = 0
            while y < (edge_users.iloc[i,2]-1):
                edge_classes.append(edge_type)
                y= y+1
    elif edge_users.iloc[i,0] == "simple bot" and edge_users.iloc[i,1] == "simple bot":
        edge_type = "bb-bb"
        edge_classes.append(edge_type)
        if (edge_users.iloc[i,2] > 1):
            y = 0
            while y < (edge_users.iloc[i,2]-1):
                edge_classes.append(edge_type)
                y= y+1
    elif edge_users.iloc[i,0] == "simple bot" and edge_users.iloc[i,1] == "sophisticated bot":
        edge_type = "bb-sb"
        edge_classes.append(edge_type)
        if (edge_users.iloc[i,2] > 1):
            y = 0
            while y < (edge_users.iloc[i,2]-1):
                edge_classes.append(edge_type)
                y= y+1
    elif edge_users.iloc[i,0] == "sophisticated bot" and edge_users.iloc[i,1] == "human":
        edge_type = "sb-h"
        edge_classes.append(edge_type)
        if (edge_users.iloc[i,2] > 1):
            y = 0
            while y < (edge_users.iloc[i,2]-1):
                edge_classes.append(edge_type)
                y= y+1
    elif edge_users.iloc[i,0] == "sophisticated bot" and edge_users.iloc[i,1] == "simple bot":
        edge_type = "sb-bb"
        edge_classes.append(edge_type)
        if (edge_users.iloc[i,2] > 1):
            y = 0
            while y < (edge_users.iloc[i,2]-1):
                edge_classes.append(edge_type)
                y= y+1
    elif edge_users.iloc[i,0] == "sophisticated bot" and edge_users.iloc[i,1] == "sophisticated bot":
        edge_type = "sb-sb"
        edge_classes.append(edge_type)
        if (edge_users.iloc[i,2] > 1):
            y = 0
            while y < (edge_users.iloc[i,2]-1):
                edge_classes.append(edge_type)
                y= y+1
    else:
        edge_type = "includes_missing"
        edge_classes.append(edge_type)
        if (edge_users.iloc[i,2] > 1):
            y = 0
            while y < (edge_users.iloc[i,2]-1):
                edge_classes.append(edge_type)
                y= y+1

    i = i+1

#Count the assigned edge types
print('number of h-h edges is: ', edge_classes.count('h-h'))
print('number of h-bb edges is: ', edge_classes.count('h-bb'))
print('number of h-sb edges is: ', edge_classes.count('h-sb'))
print('number of bb-h edges is: ', edge_classes.count('bb-h'))
print('number of bb-bb edges is: ', edge_classes.count('bb-bb'))
print('number of bb-sb edges is: ', edge_classes.count('bb-sb'))
print('number of sb-h edges is: ', edge_classes.count('sb-h'))
print('number of sb-bb edges is: ', edge_classes.count('sb-bb'))
print('number of sb-sb edges is: ', edge_classes.count('sb-sb'))

edge_class_counts = pd.DataFrame(
    {'o-h':[edge_classes.count('h-h'),edge_classes.count('h-bb'),edge_classes.count('h-sb')],
     'o-bb':[edge_classes.count('bb-h'),edge_classes.count('bb-bb'),edge_classes.count('bb-sb')],
     'o-sb':[edge_classes.count('sb-h'),edge_classes.count('sb-bb'),edge_classes.count('sb-sb')]},
    index=['target - h','target - bb','target - sb'])

edge_class_counts.to_csv('edge_class_counts.csv',index=False)

###Secondary analysis
#import best performing node names

#import adjecency table of all retweets

#see where most retweets of best performing nodes came from