import pandas as pd
import numpy as np


#Import node table from gephi, following calculations
node_table = pd.read_csv("retweet nodes table.csv")
#import botomoter results
botometer_humans = pd.read_csv("humans.csv")['list'].tolist()
botometer_simple_bots = pd.read_csv("simple.csv")['list'].tolist()
botometer_sop_bots = pd.read_csv("sophisticated.csv")['list'].tolist()

#assign class to each node
current_class = ""
user_classes = []
i = 0
while i < len(node_table):
    current_user = node_table.iloc[i, 1]
    if current_user in botometer_humans:
        current_class = "human"
    elif current_user in botometer_simple_bots:
        current_class = "simple bot"
    elif current_user in botometer_sop_bots:
        current_class = "sophisticated bot"
    else:
        current_class = "missing"

    user_classes.append(current_class)
    i = i+1

node_table.insert(0,'class',user_classes)

node_table.to_csv('classified_retweet_nodes_table.csv',index=False)
nodes_table = node_table
#statistical descriptions
human_nodes = nodes_table[node_table['class'] == "human"].describe()
basic_bot_nodes = nodes_table[node_table['class'] == "simple bot"].describe()
sophisticate_bot_nodes = nodes_table[node_table['class'] == "sophisticated bot"].describe()

#place nodes into top 1000, 100, 50, 10, for every measured variable, DONE IN excel on the node_table.csv
