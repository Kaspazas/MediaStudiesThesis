import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import time
import matplotlib.dates as dates

dataset = pd.read_csv("hashtags from dataset.csv") #Requires columns:time|class|hashtags (file is comma delimited, multiple hashtags in same cell delimited by space)

#making all hashtags lowercase
i=0
while i < len(dataset):
    dataset["hashtags"][i] = dataset["hashtags"][i].lower()
    print(i)
    i = i + 1


#dataset.to_csv('hashtags_lowercased.csv', index=False) #exporting lower-case hashtags for gephi

#first time setup
hashtag_timeline = pd.DataFrame({'hashtag': ['nan'], 'posted_at': ['nan'], 'class': ['nan']}) #creates a dataframe that combines the tweeters username with the username of the mentioned

#creating a timeline of hashtags and poster class
i=0
print('gonna run', (len(dataset)-1),'iterations')

while i < len(dataset):
    current_time = dataset.iloc[i,0] #saves the time of tweet posted
    current_class = dataset.iloc[i,1] #saves the class of the user that tweeted
    current_hashtags = dataset.iloc[i,2] #saves the hashtags used cell
    current_hashtags = current_hashtags.split() #creates a list of hashtags used, separates cell contents by space if needed
    current_lenght = len(current_hashtags) #counts how many hashtags were used

    if current_lenght < 2: #if only one hashtag is used
        relevant_hashtag = str(current_hashtags[0]) #selects the first (in this case only) mentioned hashtag
        temporary_step = pd.DataFrame({'hashtag': [str(relevant_hashtag)], 'posted_at': [(current_time)], 'class': [str(current_class)]}) #creates a dataframe that combines the time of post, class of poster and hashtag
        hashtag_timeline = pd.concat([hashtag_timeline, temporary_step], axis=0) #combines the dataframe created in previous line with our blanc datatable created on line ~8

    else: #if more than one hashtag is used
        y = 0 #creates arbritrary variable to use for loop, where y serves to identify which of the mentioned users we're currently working with

        while y < current_lenght: #loops through each hashtag used and saves them alongside other relevant variables
            relevant_hashtag = str(current_hashtags[y])

            temporary_step = pd.DataFrame({'hashtag': [str(relevant_hashtag)], 'posted_at': [(current_time)], 'class': [str(current_class)]})  # creates a dataframe that combines the time of post, class of poster and hashtag
            hashtag_timeline = pd.concat([hashtag_timeline, temporary_step], axis=0)  # combines the dataframe created in previous line with our blank datatable created on line ~8

            y = y + 1

    i = i + 1

#creating a list of hashtags that were used by both bots and humans #TERRIBLY WRITTEN CODE
hashtag_timeline_copy = hashtag_timeline.copy() #just in case, saves a copy
hashtag_poster_class = hashtag_timeline.copy()
hashtag_poster_class.drop("posted_at", inplace = True, axis = 1)
hashtags_unique_class = hashtag_poster_class.copy()
hashtags_unique_class = hashtags_unique_class.iloc[:, 0] #makes a list of all hashtags
hashtags_unique_class.drop_duplicates(keep=False, inplace = True) #drops hashtags if they OCCUR WITH WITH BOTH CLASS MODIFIERS. We determine this by previously identifying unique entries, meaning that a hashtag was not filtered because it occured in two rows - it had two different classes
hashtag_poster_class.drop_duplicates(inplace = True)
hashtag_poster_class_test = ~hashtag_poster_class.hashtag.isin(hashtags_unique_class)
hashtag_poster_class = hashtag_poster_class[hashtag_poster_class_test]
hashtags_posted_by_both = list(hashtag_poster_class.iloc[:, 0])

#saving timeline that only includes hashtags posted by both bots and humans (filtering the overall timeline)
all_used = pd.DataFrame({'hashtag': ['nan'], 'posted_at': ['nan'], 'class': ['nan']})

i=0
while i < len(hashtag_timeline):
    x = hashtag_timeline.iloc[i, 0] #select a hashtag from our timeline
    if (x in hashtags_posted_by_both): #see if hashtag is in list of used by both
        used_temp = pd.DataFrame(hashtag_timeline.iloc[i,]).transpose() #if used by both, save the hashtag
        all_used = pd.concat([all_used, used_temp], axis=0) #combine previously saved data with current hashtag
    i = i + 1

all_used = all_used.iloc[1:, :]

#removing hashtags with less than X occurances
X = 50
all_used_counts = pd.DataFrame(all_used_copy.value_counts('hashtag')) #counts occurances and makes a dataframe with hashtag and occurances
all_used_counts = all_used_counts.rename_axis("hashtag").reset_index() #moves hashtags from row names to first column (previous step messes it up for some reason)
all_used_counts.columns = ['hashtag','occurances'] #renames column titles to something more relevant
all_used_counts = all_used_counts[all_used_counts['occurances'] > X] #removes hashtags if they have less than 30 occurances
hashtags_with_more_than_50_occurances = list(all_used_counts.iloc[:, 0]) #makes a list of relevant hashtags

#creating a timeline containing only hashtags with more than X occurances
more_than = pd.DataFrame({'hashtag': ['nan'], 'posted_at': ['nan'], 'class': ['nan']})
i=0
while i < len(all_used_copy):
    z = all_used_copy.iloc[i, 0] #select a hashtag from the ones used by both bots and humans
    if (z in hashtags_with_more_than_50_occurances): #see if hashtag is in list of >50 occurances
        more_than_temp = pd.DataFrame(all_used_copy.iloc[i,]).transpose() #if in list, save the hashtag and associated data to a dataframe
        more_than = pd.concat([more_than, more_than_temp], axis=0) #combine previously saved data with current hashtag
    i = i + 1
more_than = more_than.iloc[1:, :]
more_than.to_csv('hashtag_timeline_more_than_50.csv')

#Loop for graphing
i = 0
while (i< len(all_used_counts)):
    hashtag_in_question = hashtags_with_more_than_50_occurances[i] #pick a hashtag from the more than 50 occurances list CHANGE 0 TO i FOR LOOP LATER
    hashtag_in_question_occurances = (more_than[more_than['hashtag'] == hashtag_in_question]).reset_index(drop=True) #save all occurances of picked hashtag in a new dataframe?

	#changing time to somethin python can read
    hashtag_in_question_occurances['posted_at'] = pd.to_datetime(hashtag_in_question_occurances['posted_at']) #sets value to datetime index
    both_used = pd.DataFrame(hashtag_in_question_occurances["posted_at"]).reset_index(drop=True) #makes a copy of the dates for later

	#Split bot and human hashtag usages?
    human_used = hashtag_in_question_occurances[hashtag_in_question_occurances['class']=='human'] #save all rows with 'human' in class column separately
    human_used = pd.concat([both_used, human_used], axis = 1, keys= "posted_at", ignore_index=True) #Combine the human_used data with the timeline from both (because human only will be missing time segments)
    human_used.iloc[:,0] = pd.to_datetime(human_used.iloc[:,0]) #convert the time column to the datetime data type
    human_used.set_index(human_used.iloc[:,0], inplace=True) #replace the row names with the datetime made previously
    human_used.set_axis(['timestamp','hashtag','timeagain','class'],axis=1,inplace=True) #set column names for easier graphing

    bot_used = hashtag_in_question_occurances[hashtag_in_question_occurances['class']=='bot']
    bot_used = pd.concat([both_used, bot_used], axis = 1, keys= "posted_at", ignore_index=True)
    bot_used.iloc[:,0] = pd.to_datetime(bot_used.iloc[:,0])
    bot_used.set_index(bot_used.iloc[:,0], inplace=True)
    bot_used.set_axis(['timestamp','hashtag','timeagain','class'],axis=1,inplace=True)

    #chaning type of big lists index post merge with bot and human usages, inorder to support graphing later
    hashtag_in_question_occurances.set_index('posted_at', inplace=True, drop= False) #sets datetime as index (row names) ---- works despite error

    #constructing segments to be used on x axis
    over15min_timeline = hashtag_in_question_occurances.groupby(pd.Grouper(freq='15T')).count() #group all occurences by segments of 20mins (the useful part is grouping our overall timeline) | .count() isn't neccessary here?
    over15min_human = human_used.groupby(pd.Grouper(freq='15T')).count() #group all human used hashtag occurances by segments of (# before 't') mins
    
	#if wanted, making occurrences cummulative
	# over15min_human['cum_sum'] = over15min_human['hashtag'].cumsum()
    # over15min_human = over15min_human.loc[over15min_timeline_start:over15min_timeline_end]

    over15min_bot = bot_used.groupby(pd.Grouper(freq='15T')).count()
    # over15min_bot['cum_sum'] = over15min_bot['hashtag'].cumsum()
    # over15min_bot = over15min_bot.loc[over15min_timeline_start:over15min_timeline_end]
    # graph
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

	#can have a finely detailed X axis if wanted, takes forever and loses data outside of hours for some reason
    # x = over15min_timeline.index
    # plt.xticks(np.arange(min(x), max(x), 3600000000)) #9*10^9 microseconds in 15min.
    # plt.xticks(rotation=45)
    # date_format = dates.DateFormatter('%H:%T')
    # plt.gca().xaxis.set_major_formatter(date_format)
    # plt.tight_layout()
    # plt.locator_params(axis='x', nbins=100)
	
	#Continue graphing
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.grid(b=True, which='major', color='#999999', linestyle='-', alpha=0.5)
    f.set_figwidth(18) #sets size, too small makes precise visual analysis more difficult, hence the bigger size
    f.set_figheight(9)
    plt.savefig((str(hashtag_in_question)+'.png')) #save figure
    i += 1 #reset loop
