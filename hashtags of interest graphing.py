#similar to hashtag timeline graphing, if notes missing here, look there
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import time
import matplotlib.dates as dates

#import timeline and hashtags of interest
hashtag_timeline = pd.read_csv('hashtag timeline with class.csv')
hashtags_of_interest = pd.read_csv('hashtags_of_interest.csv') #needs csv file where every column starts with a hashtag of interest and the following rows contain connected hashtags

#load overall timeline
all_used = pd.read_csv('hashtag timeline with class.csv') #this includes hashtags used exclusively by bots or humans
all_used_copy = all_used

#counts occurances and removes hashtags that are used too much
all_used_counts = pd.DataFrame(all_used_copy.value_counts('hashtag')) #counts occurances and makes a dataframe with hashtag and occurances
all_used_counts = all_used_counts.rename_axis("hashtag").reset_index() #moves hashtags from row names to first column (previous step messes it up for some reason)
all_used_counts.columns = ['hashtag','occurances'] #renames column titles to something more relevant
all_used_counts = all_used_counts[all_used_counts['occurances'] < 100] #removes hashtags if they have more than 50 occurances
hashtags_with_less_than_50_occurances = list(all_used_counts.iloc[:, 0]) #makes a list of relevant hashtags

#removes too frequently used hashtags from timeline (to not distort overall image)
less_than_timeline = pd.DataFrame({'hashtag': ['nan'], 'posted_at': ['nan'], 'class': ['nan']})
i=0
while i < len(all_used_copy):
    z = all_used_copy.iloc[i, 0] #select a hashtag from the ones used by both bots and humans
    if (z in hashtags_with_less_than_50_occurances): #see if hashtag is in list of >50 occurances
        less_than_timeline_temp = pd.DataFrame(all_used_copy.iloc[i,]).transpose() #if in list, save the hashtag and associated data to a dataframe
        less_than_timeline = pd.concat([less_than_timeline, less_than_timeline_temp], axis=0) #combine previously saved data with current hashtag
    i = i + 1
less_than_timeline = less_than_timeline.iloc[1:, :]

#graphing data prep
i = 0
while (i< 10):
    current_interest = hashtags_of_interest.columns[i] #finds name of hashtag

    hashtag_in_question = list(hashtags_of_interest[current_interest]) #selects all connected hashtags
    hashtag_in_question = [x for x in hashtag_in_question if pd.isnull(x) == False]#removes nan values, because different hashtags have different # of associated hashtags, nan appears

    #a loop to create a timeline of usages for all hashtags connected to a hashtag of interest
    hashtag_in_question_occurances = pd.DataFrame({'hashtag': ['nan'], 'posted_at': ['nan'], 'class': ['nan']})

    y = 0
    while y < len(less_than_timeline):
        z = less_than_timeline.iloc[y,0]  # select a hashtag from the ones used by both bots and humans
        if (z in hashtag_in_question):  # see if hashtag is in list of >50 occurances
            hashtag_in_question_occurances_temp = pd.DataFrame(less_than_timeline.iloc[y,]).transpose()  # if in list, save the hashtag and associated data to a dataframe
            hashtag_in_question_occurances = pd.concat([hashtag_in_question_occurances, hashtag_in_question_occurances_temp],axis=0)  # combine previously saved data with current hashtag
        y = y + 1
    hashtag_in_question_occurances = hashtag_in_question_occurances.iloc[1:, :]

    #Changing time to something python can read
    both_used = pd.DataFrame(hashtag_in_question_occurances["posted_at"])#.reset_index(drop=True)  # makes a copy of the dates for later

    #Split bot and human hashtag usages
    human_used = hashtag_in_question_occurances[hashtag_in_question_occurances['class']=='human'] #save all rows with 'human' in class column separately
    human_used = pd.concat([human_used, both_used], axis=1, keys="posted_at", ignore_index=True) #Combine the human_used data with the timeline from both (because human only will be missing time segments)
    human_used.iloc[:,3] = pd.to_datetime(human_used.iloc[:,3]) #convert the time column to the datetime data type
    human_used.set_index(human_used.iloc[:,3], inplace=True) #replace the row names with the datetime made previously
    human_used.set_axis(['hashtag','human_time','class','time'],axis=1,inplace=True) #set column names for easier graphing

    bot_used = hashtag_in_question_occurances[hashtag_in_question_occurances['class']=='bot']
    bot_used = pd.concat([bot_used, both_used], axis = 1, keys= "posted_at", ignore_index=True)
    bot_used.iloc[:,3] = pd.to_datetime(bot_used.iloc[:,3])
    bot_used.set_index(bot_used.iloc[:,3], inplace=True)
    bot_used.set_axis(['hashtag','bot_time','class','time'],axis=1,inplace=True)

    #chaning type of big lists index post merge with bot and human usages, inorder to support graphing later
    hashtag_in_question_occurances.iloc[:,1] = pd.to_datetime(hashtag_in_question_occurances.iloc[:,1])
    hashtag_in_question_occurances.set_index('posted_at', inplace=True, drop= False) #sets datetime as index (row names) ---- works despite error

    #constructing segments to be used on x axis
    over15min_timeline = hashtag_in_question_occurances.groupby(pd.Grouper(freq='15T')).count() #group all occurences by segments of 15mins (the useful part is grouping our overall timeline) | .count() isn't neccessary here?
    over15min_human = human_used.groupby(pd.Grouper(freq='15T')).count() #group all human used hashtag occurances by segments of (# before 't') mins
    over15min_bot = bot_used.groupby(pd.Grouper(freq='15T')).count()

	#Graphing
    f = plt.figure() #saves figure to be shown into 'f', allows for exporting later
    plt.plot(over15min_timeline.index, over15min_human.hashtag, label = "human") #plot using human occurance counts as y, and the overall timeline segments as x
    #plt.plot(over15min_timeline.index, over15min_human.cum_sum, label="human")#FOR CUMULATIVE
    plt.plot(over15min_timeline.index, over15min_bot.hashtag, label = "bot")
    #plt.plot(over15min_timeline.index, over15min_bot.cum_sum, label="bot")#FOR CUMULATIVE

    plt.legend() #introduces a legend into the figure
    plt.title(str(hashtag_in_question)) #gives graph a title - the hashtag in question
    plt.xlabel("time") #labels the x axis
    plt.ylabel("occurrence count")
    plt.minorticks_on()

    # x = over15min_timeline.index
    # plt.xticks(np.arange(min(x), max(x), 3600000000)) #9*10^9 microseconds in 15min? deal with multiples of that
    # plt.xticks(rotation=45)
    # date_format = dates.DateFormatter('%H:%T')
    # plt.gca().xaxis.set_major_formatter(date_format)
    # plt.tight_layout()
    # plt.locator_params(axis='x', nbins=100)
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.grid(b=True, which='major', color='#999999', linestyle='-', alpha=0.5)
    f.set_figwidth(18) #sets size, too small makes precise visual analysis more difficult, hence the bigger size
    f.set_figheight(9)

    plt.savefig((str(current_interest)+'_connected_tags.png')) #save figure

    i += 1 #reset loop

