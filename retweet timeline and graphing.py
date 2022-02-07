import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import time

dataset = pd.read_csv("retweets.csv") #requires csv with: created_at|screen_name|class|retweet_screen_name

#these are the 20 most retweeted humans and bots. Two columns: bots|humans, with rows being usernames of appropriate class
highly_retweeted_users = pd.read_csv("retweet_big_players.csv")

#define selections by class
humans_of_interest = highly_retweeted_users["humans"].tolist()
bots_of_interest = highly_retweeted_users["bots"].tolist()

#select class
#users_of_interest = humans_of_interest
users_of_interest = bots_of_interest

#how long are the intervals into which the retweets are grouped and counted
seg_len = '15T'

while i <= (len(users_of_interest)-1):
    #
    retweeters = dataset[dataset["retweet_screen_name"].str.contains(users_of_interest[i])]
    #
    print(users_of_interest[i])
    human_retweeters = retweeters[retweeters["class"]=="human"]
    print("human retweeters:" + str(len(human_retweeters)))
    bot_retweeters = retweeters[retweeters["class"]=="bot"]
    print("bot retweeters:" + str(len(bot_retweeters)))
    #
    retweeters["created_at"] = pd.to_datetime(retweeters["created_at"])
    retweeter_reused = retweeters.iloc[:,:1]

    #looking for when user was retweeted most frequently

    retweeters.set_index(retweeters["created_at"], inplace=True)
    retweeters = retweeters.groupby(pd.Grouper(freq=seg_len)).count()

    #retweeters.set_axis(['timestamp', 'timeagain', 'retweeter', 'class', 'retweeted'], axis=1, inplace=True)

    #
    human_retweeters = pd.concat([retweeter_reused,human_retweeters],axis = 1, keys="created_at", ignore_index=True)
    human_retweeters.set_axis(['timestamp','timeagain','retweeter','class','retweeted'],axis=1,inplace=True)
    human_retweeters.set_index(human_retweeters["timestamp"], inplace=True)
    human_retweeters = human_retweeters.groupby(pd.Grouper(freq=seg_len)).count()
    human_retweeters['cum_sum'] = human_retweeters['class'].cumsum()
    human_retweeters = human_retweeters.loc[timeline_start:timeline_end] #run for the spliting


    bot_retweeters = pd.concat([retweeter_reused,bot_retweeters],axis = 1, keys="created_at", ignore_index=True)
    bot_retweeters.set_axis(['timestamp','timeagain','retweeter','class','retweeted'],axis=1,inplace=True)
    bot_retweeters.set_index(bot_retweeters["timestamp"], inplace=True)
    bot_retweeters = bot_retweeters.groupby(pd.Grouper(freq=seg_len)).count()
    bot_retweeters['cum_sum'] = bot_retweeters['class'].cumsum()
    bot_retweeters = bot_retweeters.loc[timeline_start:timeline_end] #run for the spliting

    f = plt.figure()  # saves figure to be shown into 'f', allows for exporting later
    #plt.plot(human_retweeters.index, human_retweeters.retweeter, label="human")  # plot using human occurance counts as y, and the overall timeline segments as x
    plt.plot(human_retweeters.index, human_retweeters.cum_sum, label="human")
    #plt.plot(bot_retweeters.index, bot_retweeters.retweeter, label="bot")
    plt.plot(bot_retweeters.index, bot_retweeters.cum_sum, label="bot")
    plt.legend()  # introduces a legend into the figure
    plt.title(str(users_of_interest[i]))  # gives graph a title - the hashtag in question
    plt.xlabel("time")  # labels the x axis
    plt.ylabel("retweet count")
    f.set_figwidth(18)  # sets size, too small makes precise visual analysis more difficult, hence the bigger size
    f.set_figheight(9)
    plt.savefig((str(users_of_interest[i]) + '.png'))  # save figure

    i = i + 1
