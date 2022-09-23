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


#dataset.to_csv('hashtags_lowercased.csv', index=False) #making stuff lower case for gephi
#first time setup
hashtag_timeline = pd.DataFrame({'id': ['nan'], 'hashtag': ['nan'], 'posted_at': ['nan'], 'class': ['nan']}) #creates a dataframe that combines the tweeters username with the username of the mentioned

#creating a timeline of hashtags and poster class
i=0
print('gonna run', (len(dataset)-1),'iterations')

while i < len(dataset):
    current_id = dataset.iloc[i,0]
    current_time = dataset.iloc[i,1] #saves the time of tweet posted
    current_class = dataset.iloc[i,2] #saves the class of the user that tweeted
    current_hashtags = dataset.iloc[i,3] #saves the hashtags used cell
    current_hashtags = current_hashtags.split() #creates a list of hashtags used, separates cell contents by space if needed
    current_lenght = len(current_hashtags) #counts how many hashtags were used

    if current_lenght < 2: #if only one hashtag is used
        relevant_hashtag = str(current_hashtags[0]) #selects the first (in this case only) mentioned hashtag
        temporary_step = pd.DataFrame({'hashtag': [str(relevant_hashtag)], 'posted_at': [(current_time)], 'class': [str(current_class)], 'id': [str(current_id)]}) #creates a dataframe that combines the time of post, class of poster and hashtag
        hashtag_timeline = pd.concat([hashtag_timeline, temporary_step], axis=0) #combines the dataframe created in previous line with our blanc datatable created on line ~8

    else: #if more than one hashtag is used
        y = 0 #creates arbritrary variable to use for loop, where y serves to identify which of the mentioned hashtags we're currently working with

        while y < current_lenght: #loops through each hashtag used and saves them alongside other relevant variables
            relevant_hashtag = str(current_hashtags[y])

            temporary_step = pd.DataFrame({'hashtag': [str(relevant_hashtag)], 'posted_at': [(current_time)], 'class': [str(current_class)], 'id': [str(current_id)]})  # creates a dataframe that combines the time of post, class of poster and hashtag
            hashtag_timeline = pd.concat([hashtag_timeline, temporary_step], axis=0)  # combines the dataframe created in previous line with our blank datatable created on line ~8

            y = y + 1

    i = i + 1

hashtag_timeline = hashtag_timeline.iloc[1:, :]
#hashtag_timeline.to_csv("hashtag_timeline.csv")
#selecting hashtags that were posted by both bots and humans #TERRIBLY WRITTEN CODE

hashtag_timeline_copy = hashtag_timeline.copy() #just in case, saves a copy
hashtag_poster_class = hashtag_timeline.copy()
hashtag_poster_class.drop("posted_at", inplace = True, axis = 1)

#selects hashtags that are not posted by both
hashtags_unique_class = hashtag_poster_class.copy()
hashtags_unique_class = hashtags_unique_class.iloc[:, 1] #makes a list of all hashtags
hashtags_unique_class.drop_duplicates(keep=False, inplace = True) #drops hashtags if they OCCUR WITH WITH BOTH CLASS MODIFIERS. We determine this by previously identifying unique entries, meaning that a hashtag was not filtered because it occured in two rows - it had two different classes
hashtag_poster_class.drop_duplicates(inplace = True)


hashtag_poster_class_test = ~hashtag_poster_class.hashtag.isin(hashtags_unique_class)
hashtag_poster_class = hashtag_poster_class[hashtag_poster_class_test]

hashtags_posted_by_both = list(hashtag_poster_class.iloc[:, 1])


#Identifying hashtags posted by both classes
all_used = pd.DataFrame({'hashtag': ['nan'], 'posted_at': ['nan'], 'class': ['nan']})


i=0
while i < len(hashtag_timeline):
    x = hashtag_timeline.iloc[i, 1] #select a hashtag from our timeline
    if (x in hashtags_posted_by_both): #see if hashtag is in list of used by both
        used_temp = pd.DataFrame(hashtag_timeline.iloc[i,]).transpose() #if used by both, save the hashtag
        all_used = pd.concat([all_used, used_temp], axis=0) #combine previously saved data with current hashtag
    i = i + 1

all_used = all_used.iloc[1:, :]
all_used_copy = all_used[all_used['class'] == "human"]

#count human hashtags, to identify most popular
human_used_counts = pd.DataFrame(all_used_copy.value_counts('hashtag')) #counts occurances and makes a dataframe with hashtag and occurances
human_used_counts = human_used_counts.rename_axis("hashtag").reset_index() #moves hashtags from row names to first column (previous step messes it up for some reason)
human_used_counts.columns = ['hashtag','occurrences'] #renames column titles to something more relevant

hashtags_of_interest = human_used_counts[human_used_counts['occurrences'] > 15] #removes hashtags if they have less than 30 occurances

hashtags_with_more_than_15_occurrences = list(hashtags_of_interest.iloc[:, 0]) #makes a list of relevant hashtags


more_than = pd.DataFrame({'hashtag': ['nan'], 'posted_at': ['nan'], 'class': ['nan']})

i=0
while i < len(all_used):
    y = all_used.iloc[i, 0] #select a hashtag from the ones used by both bots and humans
    if (y in hashtags_with_more_than_15_occurrences): #see if hashtag is in list of >50 occurances
        more_than_temp = pd.DataFrame(all_used.iloc[i,]).transpose() #if in list, save the hashtag and associated data to a dataframe
        more_than = pd.concat([more_than, more_than_temp], axis=0) #combine previously saved data with current hashtag
    i = i + 1

more_than = more_than.iloc[1:, :]
more_than.to_csv('hashtag_timeline_more_than_50.csv')

more_than = more_than.drop(columns="id")
all_used = all_used.drop(columns="id")

#######actual graphs##########
bots = ["simple","sophisticated"]

i = 0
while (i< len(human_used_counts)):
hashtag_in_question = hashtags_with_more_than_15_occurrences[i] #pick a hashtag from the more than 50 occurances list CHANGE 0 TO i FOR LOOP LATER
hashtag_in_question_occurrences = (more_than[more_than['hashtag'] == hashtag_in_question]).reset_index(drop=True) #save all occurances of picked hashtag in a new dataframe?

# #changing time to somethin python can read
hashtag_in_question_occurrences['posted_at'] = pd.to_datetime(hashtag_in_question_occurrences['posted_at']) #sets value to datetime index
both_used = pd.DataFrame(hashtag_in_question_occurrences["posted_at"]).reset_index(drop=True) #makes a copy of the dates for later

#Split bot and human hashtag usages?
human_used = hashtag_in_question_occurrences[hashtag_in_question_occurrences['class']=='human'] #save all rows with 'human' in class column separately
human_used = pd.concat([both_used, human_used], axis = 1, keys= "posted_at", ignore_index=True) #Combine the human_used data with the timeline from both (because human only will be missing time segments)
human_used.iloc[:,0] = pd.to_datetime(human_used.iloc[:,0]) #convert the time column to the datetime data type
human_used.set_index(human_used.iloc[:,0], inplace=True) #replace the row names with the datetime made previously
human_used.set_axis(['timestamp','hashtag','timeagain','class'],axis=1,inplace=True) #set column names for easier graphing

bot_used = hashtag_in_question_occurrences[hashtag_in_question_occurrences['class'].isin(bots)]
bot_used = pd.concat([both_used, bot_used], axis = 1, keys= "posted_at", ignore_index=True)
bot_used.iloc[:,0] = pd.to_datetime(bot_used.iloc[:,0])
bot_used.set_index(bot_used.iloc[:,0], inplace=True)
bot_used.set_axis(['timestamp','hashtag','timeagain','class'],axis=1,inplace=True)

#chaning type of big lists index post merge with bot and human usages, inorder to support graphing later
#sets datetime as index (row names) ---- works despite error
text = pd.read_csv('textual_content.csv')

humans = text[text['class'] == "human"]
bot = text[text['class'].isin(bots)]

text = pd.DataFrame(text["created_at"])
humans = pd.concat([text, humans], axis = 1, keys= "created_at", ignore_index=True)
bot = pd.concat([text, bot], axis = 1, keys= "created_at", ignore_index=True)

humans[0] = pd.to_datetime(humans.iloc[:,0])
humans.set_index('created_at', inplace=True, drop= False)

bot[0] = pd.to_datetime(bot.iloc[:,0])
bot.set_index([0], inplace=True, drop= False)

text["created_at"] = pd.to_datetime(text['created_at'])
#constructing segments to be used on x axis
text.

timeline = text.groupby(pd.Grouper(freq='15T')).count() #group all occurences by segments of 20mins (the useful part is grouping our overall timeline) | .count() isn't neccessary here?

over15min_human = human_used.groupby(pd.Grouper(freq='15T')).count() #group all human used hashtag occurances by segments of (# before 't') mins
over15min_human['cum_sum'] = over15min_human['hashtag'].cumsum()
# over15min_human = over15min_human.loc[over15min_timeline_start:over15min_timeline_end]

over15min_bot = bot_used.groupby(pd.Grouper(freq='15T')).count()
over15min_bot['cum_sum'] = over15min_bot['hashtag'].cumsum()
# over15min_bot = over15min_bot.loc[over15min_timeline_start:over15min_timeline_end]



# graph
f = plt.figure() #saves figure to be shown into 'f', allows for exporting later
#plt.plot(over15min_timeline.index, over15min_human.hashtag, label = "human") #plot using human occurance counts as y, and the overall timeline segments as x
plt.plot(over15min_timeline.index, over15min_human.cum_sum, label="human")#FOR CUMULATIVE
#plt.plot(over15min_timeline.index, over15min_bot.hashtag, label = "bot")
plt.plot(over15min_timeline.index, over15min_bot.cum_sum, label="bot")#FOR CUMULATIVE


plt.legend() #introduces a legend into the figure
plt.title(str(hashtag_in_question)) #gives graph a title - the hashtag in question
plt.xlabel("time") #labels the x axis
plt.ylabel("occurrence count")
plt.minorticks_on()


plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.grid(b=True, which='major', color='#999999', linestyle='-', alpha=0.5)
f.set_figwidth(18) #sets size, too small makes precise visual analysis more difficult, hence the bigger size
f.set_figheight(9)

plt.savefig((str(hashtag_in_question)+'.png')) #save figure

i += 1 #reset loop


###########################################
######EXPLORING HASHTAGS OF INTEREST!######
###########################################

#check if any new hashtags were introduced by bots, alongside hashtags of interest
#if so, graph their usage -
#are these hashtags introduced when bots start using the hashtag of interest?
import pandas as pd
import numpy as np
import collections
from collections import Counter

dataset = pd.read_csv("hashtags from dataset.csv") #Requires columns:time|class|hashtags (file is comma delimited, multiple hashtags in same cell delimited by space)

#making all hashtags lowercase
i=0
while i < len(dataset):
    dataset["hashtags"][i] = dataset["hashtags"][i].lower()
    print(i)
    i = i + 1

hoi_list = ['urineidiot','unvaccinated','vaccination','trumpvirus','quebec','freedom',
            'science','canada','america','deltacron','vaccinemandates','funny',
            'delta']

urineidiot = pd.DataFrame()
unvaccinated = pd.DataFrame()
vaccination = pd.DataFrame()
trumpvirus = pd.DataFrame()
quebec = pd.DataFrame()
freedom = pd.DataFrame()
science = pd.DataFrame()
canada = pd.DataFrame()
america = pd.DataFrame()
deltacron = pd.DataFrame()
vaccinemandates = pd.DataFrame()
funny = pd.DataFrame()
delta = pd.DataFrame()

hoi_df_list = [urineidiot,unvaccinated,vaccination,trumpvirus,quebec,freedom,
            science,canada,america,deltacron,vaccinemandates,funny,
            delta]


i = 0
y = 0
hashtag_counter = pd.DataFrame(columns=['status_id','created_at','class','hashtags','text'])
while i< len(hoi_list):
    y = 0
    hashtag_counter = pd.DataFrame(columns=['status_id', 'created_at', 'class', 'hashtags', 'text'])
    while y<len(dataset):
        if hoi_list[i] in dataset["hashtags"].iloc[y]:
            counter = dataset.iloc[y]
            hashtag_counter = hashtag_counter.append(counter, ignore_index=True)
            y=y+1
        else:
            y=y+1
    hoi_df_list[i] = hashtag_counter
    i=i+1




bots = ["simple","sophisticated"]


urineidiot = hoi_df_list[0]
urineidiot_1 = pd.DataFrame(columns=['id','hashtag','posted_at','class','text'])
i=0
while i < len(urineidiot['status_id']):
    y = 0
    current_id = urineidiot['status_id'][i]
    while y < len(hashtag_timeline['id']):
        potential_id = hashtag_timeline.iloc[y,0]
        if str(current_id) == str(potential_id):
            urineidiot_1 = pd.concat([urineidiot_1, pd.DataFrame(hashtag_timeline.iloc[y]).transpose()], axis=0)
            y = y+1
        else:
            y=y+1
    i=i+1

urineidiot_humans = Counter(urineidiot_1[urineidiot_1['class']=='human'].iloc[:,1])
urineidiot_bots = Counter(urineidiot_1[urineidiot_1['class'].isin(bots)].iloc[:,1])



unvaccinated = hoi_df_list[1]
unvaccinated_1 = pd.DataFrame(columns=['id','hashtag','posted_at','class','text'])
i=0
while i < len(unvaccinated['status_id']):
    y = 0
    current_id = unvaccinated['status_id'][i]
    while y < len(hashtag_timeline['id']):
        potential_id = hashtag_timeline.iloc[y,0]
        if str(current_id) == str(potential_id):
            unvaccinated_1 = pd.concat([unvaccinated_1, pd.DataFrame(hashtag_timeline.iloc[y]).transpose()], axis=0)
            y = y+1
        else:
            y=y+1
    i=i+1

unvaccinated_humans = Counter(unvaccinated_1[unvaccinated_1['class']=='human'].iloc[:,1])
unvaccinated_bots = Counter(unvaccinated_1[unvaccinated_1['class'].isin(bots)].iloc[:,1])



vaccination = hoi_df_list[2]
vaccination_1 = pd.DataFrame(columns=['id','hashtag','posted_at','class','text'])
i=0
while i < len(vaccination['status_id']):
    y = 0
    current_id = vaccination['status_id'][i]
    while y < len(hashtag_timeline['id']):
        potential_id = hashtag_timeline.iloc[y,0]
        if str(current_id) == str(potential_id):
            vaccination_1 = pd.concat([vaccination_1, pd.DataFrame(hashtag_timeline.iloc[y]).transpose()], axis=0)
            y = y+1
        else:
            y=y+1
    i=i+1

vaccination_humans = Counter(vaccination_1[vaccination_1['class']=='human'].iloc[:,1])
vaccination_bots = Counter(vaccination_1[vaccination_1['class'].isin(bots)].iloc[:,1])



trumpvirus = hoi_df_list[3]
trumpvirus_1 = pd.DataFrame(columns=['id','hashtag','posted_at','class','text'])
i=0
while i < len(trumpvirus['status_id']):
    y = 0
    current_id = trumpvirus['status_id'][i]
    while y < len(hashtag_timeline['id']):
        potential_id = hashtag_timeline.iloc[y,0]
        if str(current_id) == str(potential_id):
            trumpvirus_1 = pd.concat([trumpvirus_1, pd.DataFrame(hashtag_timeline.iloc[y]).transpose()], axis=0)
            y = y+1
        else:
            y=y+1
    i=i+1

trumpvirus_humans = Counter(trumpvirus_1[trumpvirus_1['class']=='human'].iloc[:,1])
trumpvirus_bots = Counter(trumpvirus_1[trumpvirus_1['class'].isin(bots)].iloc[:,1])


quebec = hoi_df_list[4]
quebec_1 = pd.DataFrame(columns=['id','hashtag','posted_at','class','text'])
i=0
while i < len(quebec['status_id']):
    y = 0
    current_id = quebec['status_id'][i]
    while y < len(hashtag_timeline['id']):
        potential_id = hashtag_timeline.iloc[y,0]
        if str(current_id) == str(potential_id):
            quebec_1 = pd.concat([quebec_1, pd.DataFrame(hashtag_timeline.iloc[y]).transpose()], axis=0)
            y = y+1
        else:
            y=y+1
    i=i+1

quebec_humans = Counter(quebec_1[quebec_1['class']=='human'].iloc[:,1])
quebec_bots = Counter(quebec_1[quebec_1['class'].isin(bots)].iloc[:,1])


freedom = hoi_df_list[5]
freedom_1 = pd.DataFrame(columns=['id','hashtag','posted_at','class','text'])
i=0
while i < len(freedom['status_id']):
    y = 0
    current_id = freedom['status_id'][i]
    while y < len(hashtag_timeline['id']):
        potential_id = hashtag_timeline.iloc[y,0]
        if str(current_id) == str(potential_id):
            freedom_1 = pd.concat([freedom_1, pd.DataFrame(hashtag_timeline.iloc[y]).transpose()], axis=0)
            y = y+1
        else:
            y=y+1
    i=i+1

freedom_humans = Counter(freedom_1[freedom_1['class']=='human'].iloc[:,1])
freedom_bots = Counter(freedom_1[freedom_1['class'].isin(bots)].iloc[:,1])


science = hoi_df_list[6]
science_1 = pd.DataFrame(columns=['id','hashtag','posted_at','class','text'])
i=0
while i < len(science['status_id']):
    y = 0
    current_id = science['status_id'][i]
    while y < len(hashtag_timeline['id']):
        potential_id = hashtag_timeline.iloc[y,0]
        if str(current_id) == str(potential_id):
            science_1 = pd.concat([science_1, pd.DataFrame(hashtag_timeline.iloc[y]).transpose()], axis=0)
            y = y+1
        else:
            y=y+1
    i=i+1

science_humans = Counter(science_1[science_1['class']=='human'].iloc[:,1])
science_bots = Counter(science_1[science_1['class'].isin(bots)].iloc[:,1])



canada = hoi_df_list[7]
canada_1 = pd.DataFrame(columns=['id','hashtag','posted_at','class','text'])
i=0
while i < len(canada['status_id']):
    y = 0
    current_id = canada['status_id'][i]
    while y < len(hashtag_timeline['id']):
        potential_id = hashtag_timeline.iloc[y,0]
        if str(current_id) == str(potential_id):
            canada_1 = pd.concat([canada_1, pd.DataFrame(hashtag_timeline.iloc[y]).transpose()], axis=0)
            y = y+1
        else:
            y=y+1
    i=i+1

canada_humans = Counter(canada_1[canada_1['class']=='human'].iloc[:,1])
canada_bots = Counter(canada_1[canada_1['class'].isin(bots)].iloc[:,1])


america = hoi_df_list[8]
america_1 = pd.DataFrame(columns=['id','hashtag','posted_at','class','text'])
i=0
while i < len(america['status_id']):
    y = 0
    current_id = america['status_id'][i]
    while y < len(hashtag_timeline['id']):
        potential_id = hashtag_timeline.iloc[y,0]
        if str(current_id) == str(potential_id):
            america_1 = pd.concat([america_1, pd.DataFrame(hashtag_timeline.iloc[y]).transpose()], axis=0)
            y = y+1
        else:
            y=y+1
    i=i+1

america_humans = Counter(america_1[america_1['class']=='human'].iloc[:,1])
america_bots = Counter(america_1[america_1['class'].isin(bots)].iloc[:,1])


deltacron = hoi_df_list[9]
deltacron_1 = pd.DataFrame(columns=['id','hashtag','posted_at','class','text'])
i=0
while i < len(deltacron['status_id']):
    y = 0
    current_id = deltacron['status_id'][i]
    while y < len(hashtag_timeline['id']):
        potential_id = hashtag_timeline.iloc[y,0]
        if str(current_id) == str(potential_id):
            deltacron_1 = pd.concat([deltacron_1, pd.DataFrame(hashtag_timeline.iloc[y]).transpose()], axis=0)
            y = y+1
        else:
            y=y+1
    i=i+1

deltacron_humans = Counter(deltacron_1[deltacron_1['class']=='human'].iloc[:,1])
deltacron_bots = Counter(deltacron_1[deltacron_1['class'].isin(bots)].iloc[:,1])


vaccinemandates = hoi_df_list[10]
vaccinemandates_1 = pd.DataFrame(columns=['id','hashtag','posted_at','class','text'])
i=0
while i < len(vaccinemandates['status_id']):
    y = 0
    current_id = vaccinemandates['status_id'][i]
    while y < len(hashtag_timeline['id']):
        potential_id = hashtag_timeline.iloc[y,0]
        if str(current_id) == str(potential_id):
            vaccinemandates_1 = pd.concat([vaccinemandates_1, pd.DataFrame(hashtag_timeline.iloc[y]).transpose()], axis=0)
            y = y+1
        else:
            y=y+1
    i=i+1

vaccinemandates_humans = Counter(vaccinemandates_1[vaccinemandates_1['class']=='human'].iloc[:,1])
vaccinemandates_bots = Counter(vaccinemandates_1[vaccinemandates_1['class'].isin(bots)].iloc[:,1])


funny = hoi_df_list[11]
funny_1 = pd.DataFrame(columns=['id','hashtag','posted_at','class','text'])
i=0
while i < len(funny['status_id']):
    y = 0
    current_id = funny['status_id'][i]
    while y < len(hashtag_timeline['id']):
        potential_id = hashtag_timeline.iloc[y,0]
        if str(current_id) == str(potential_id):
            funny_1 = pd.concat([funny_1, pd.DataFrame(hashtag_timeline.iloc[y]).transpose()], axis=0)
            y = y+1
        else:
            y=y+1
    i=i+1

funny_humans = Counter(funny_1[funny_1['class']=='human'].iloc[:,1])
funny_bots = Counter(funny_1[funny_1['class'].isin(bots)].iloc[:,1])


delta = hoi_df_list[12]
delta_1 = pd.DataFrame(columns=['id','hashtag','posted_at','class','text'])
i=0
while i < len(delta['status_id']):
    y = 0
    current_id = delta['status_id'][i]
    while y < len(hashtag_timeline['id']):
        potential_id = hashtag_timeline.iloc[y,0]
        if str(current_id) == str(potential_id):
            delta_1 = pd.concat([delta_1, pd.DataFrame(hashtag_timeline.iloc[y]).transpose()], axis=0)
            y = y+1
        else:
            y=y+1
    i=i+1

delta_humans = Counter(delta_1[delta_1['class']=='human'].iloc[:,1])
delta_bots = Counter(delta_1[delta_1['class'].isin(bots)].iloc[:,1])


#check the sentiment over time in tweets related to the hastag of interest,
#does increased bot usuage happen around the same time as any shift in sentiment?
import pandas as pd
import researchpy as rp
import numpy as np
import matplotlib.pyplot as plt
import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import scipy.stats as stats

hoi_list = ['urineidiot','unvaccinated','vaccination','trumpvirus','quebec','freedom',
            'science','canada','america','deltacron','vaccinemandates','funny',
            'delta',]

dataset = pd.read_csv("hashtags from dataset.csv") #Requires columns:time|class|hashtags (file is comma delimited, multiple hashtags in same cell delimited by space)

#making all hashtags lowercase
i=0
while i < len(dataset):
    dataset["hashtags"][i] = dataset["hashtags"][i].lower()
    print(i)
    i = i + 1

#first time setup
hashtag_timeline = pd.DataFrame({'id': ['nan'], 'hashtag': ['nan'], 'posted_at': ['nan'], 'class': ['nan'], 'text': ['nan']}) #creates a dataframe that combines the tweeters username with the username of the mentioned

#creating a timeline of hashtags and poster class
i=0
print('gonna run', (len(dataset)-1),'iterations')

while i < len(dataset):
    current_id = dataset.iloc[i,0]
    current_time = dataset.iloc[i,1] #saves the time of tweet posted
    current_class = dataset.iloc[i,2] #saves the class of the user that tweeted
    current_hashtags = dataset.iloc[i,3]#saves the hashtags used cell
    current_text = dataset.iloc[i,4]
    current_hashtags = current_hashtags.split() #creates a list of hashtags used, separates cell contents by space if needed
    current_lenght = len(current_hashtags) #counts how many hashtags were used

    if current_lenght < 2: #if only one hashtag is used
        relevant_hashtag = str(current_hashtags[0]) #selects the first (in this case only) mentioned hashtag
        temporary_step = pd.DataFrame({'hashtag': [str(relevant_hashtag)], 'posted_at': [(current_time)], 'class': [str(current_class)], 'id': [str(current_id)], 'text': [str(current_text)]}) #creates a dataframe that combines the time of post, class of poster and hashtag
        hashtag_timeline = pd.concat([hashtag_timeline, temporary_step], axis=0) #combines the dataframe created in previous line with our blanc datatable created on line ~8

    else: #if more than one hashtag is used
        y = 0 #creates arbritrary variable to use for loop, where y serves to identify which of the mentioned hashtags we're currently working with

        while y < current_lenght: #loops through each hashtag used and saves them alongside other relevant variables
            relevant_hashtag = str(current_hashtags[y])

            temporary_step = pd.DataFrame({'hashtag': [str(relevant_hashtag)], 'posted_at': [(current_time)], 'class': [str(current_class)], 'id': [str(current_id)], 'text': [str(current_text)]})  # creates a dataframe that combines the time of post, class of poster and hashtag
            hashtag_timeline = pd.concat([hashtag_timeline, temporary_step], axis=0)  # combines the dataframe created in previous line with our blank datatable created on line ~8

            y = y + 1

    i = i + 1
hashtag_timeline = hashtag_timeline.iloc[1:, :]




more_than = pd.DataFrame({'hashtag': ['nan'], 'posted_at': ['nan'], 'class': ['nan'], 'text':['nan']})

i=0
while i < len(hashtag_timeline):
    y = hashtag_timeline.iloc[i, 1]
    if (y in hoi_list): #see if hashtag is in list
        more_than_temp = pd.DataFrame(hashtag_timeline.iloc[i,]).transpose() #if in list, save the hashtag and associated data to a dataframe
        more_than = pd.concat([more_than, more_than_temp], axis=0) #combine previously saved data with current hashtag
    i = i + 1


more_than = more_than.iloc[1:, :]

#Run VADER sentiment analysis
analyzer = SentimentIntensityAnalyzer()

#create function
def vadersentimentanalysis(tweet):
    sentiment = (analyzer.polarity_scores(tweet))
    return sentiment

more_than['sentiment'] = more_than['text'].apply(vadersentimentanalysis)
split_cols = pd.concat([more_than, more_than["sentiment"].apply(pd.Series)], axis=1)
split_cols = split_cols.drop(columns="sentiment")


split_cols['posted_at'] = pd.to_datetime(split_cols['posted_at']) #sets value to datetime index
both_used = split_cols[["posted_at","class","hashtag","compound"]]

kruskal_results = pd.DataFrame()

i=0
while i< len(hoi_list): #Comparing means of hashtags USE SIGN TEST? COMPARE HUMAN ONLY TO HUMAN + BOTS
# 1,2,3,4 6,7,~8,10,11,12 (indeces) is not feasible statistically
    #kruskal_temp = pd.DataFrame()
    current_hashtag = both_used[both_used["hashtag"] == hoi_list[i]]

    bot_used = current_hashtag.where(~(current_hashtag['class'] == 'human'))
    bot_used = bot_used[bot_used["hashtag"] == hoi_list[i]]
    human_used = current_hashtag.where(~(current_hashtag['class'] != 'human'))
    human_used = human_used[human_used["hashtag"] == hoi_list[i]]

    data = [current_hashtag["compound"],bot_used["compound"],human_used["compound"]]

    fig = plt.figure(figsize=(5, 1.3))
    ax = fig.add_subplot(111)

    # Creating axes instance
    #ax = fig.add_axes([0,0,1, 1])
    # Creating plot
    bp = ax.boxplot(data, patch_artist = False,
                    vert = 0, showmeans = True)
    ax.set_yticklabels(['combined','bot', 'human'])

    plt.title("#"+str(hoi_list[i]))
    # Removing top axes and right axes
    # ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    plt.subplots_adjust(bottom=0.25, top=0.75, left=0.17)
    # show plot
    plt.show()
    plt.savefig("boxplot_"+(str(hoi_list[i])+'.png'))
    # show plot
    i +=1
    data = []
    #check distributions
    # plt.hist(human_used['compound'], bins=20)
    # plt.hist(bot_used['compound'], bins=20)
    # plt.show()






