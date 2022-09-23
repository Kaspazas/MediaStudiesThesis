import pandas as pd
import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import seaborn as sns
from datetime import datetime
import time
import matplotlib.pyplot as plt
import researchpy as rp
import scipy.stats as stats

#Import time_created,text and class fields from originally downloaded data
text = pd.read_csv('textual_content.csv')

#Setup VADER
analyzer = SentimentIntensityAnalyzer()

    #create function
def vadersentimentanalysis(tweet):
    sentiment = (analyzer.polarity_scores(tweet))
    return sentiment

#Run VADER on text field, append output as columns to previously imported table
text['sentiment'] = text['text'].apply(vadersentimentanalysis)

split_cols = pd.concat([text, text["sentiment"].apply(pd.Series)], axis=1)
split_cols = split_cols.drop(columns="sentiment")

#save results
            #split_cols.to_csv('sentiment_done_with_time.csv')
split_cols = pd.read_csv('sentiment_done_with_time.csv')
split_cols = split_cols.iloc[:,1:]
#Segment data into 24 hour periods
split_cols.iloc[:, 0] = pd.to_datetime(split_cols.iloc[:, 0])
split_cols = split_cols.set_index(split_cols['created_at'])
split_cols = split_cols.sort_index()
split_cols = split_cols.loc[split_cols['class'] != "missing"]

first_period = split_cols['2022-01-09T00:00:00':'2022-01-10T00:00:00']
second_period = split_cols['2022-01-10T00:00:00':'2022-01-11T00:00:00']
third_period = split_cols['2022-01-11T00:00:00':'2022-01-12T00:00:00']
fourth_period = split_cols['2022-01-12T00:00:00':'2022-01-12T12:00:00']

# fifth_period = split_cols['2022-01-10T00:00:00':'2022-01-10T06:00:00']
# sixth_period = split_cols['2022-01-10T06:00:00':'2022-01-10T12:00:00']
# seventh_period = split_cols['2022-01-10T12:00:00':'2022-01-10T18:00:00']
# eight_period = split_cols['2022-01-10T18:00:00':'2022-01-11T06:00:00']
# ninth_period = split_cols['2022-01-11T06:00:00':'2022-01-11T12:00:00']
# tenth_period = split_cols['2022-01-11T12:00:00':'2022-01-11T18:00:00']
# eleventh_period = split_cols['2022-01-11T18:00:00':'2022-01-12T00:00:00']
# twelfth_period = split_cols['2022-01-12T00:00:00':'2022-01-12T06:00:00']
# thirteenth_period = split_cols['2022-01-12T06:00:00':'2022-01-12T12:00:00']

# segments = [first_period, second_period, third_period,fourth_period,fifth_period,sixth_period,seventh_period,eight_period,ninth_period,tenth_period,eleventh_period,twelfth_period,thirteenth_period]
segments = [first_period, second_period, third_period,fourth_period]
# #Run T-tests between classes in each 6-hour segment
# t_test = pd.DataFrame()
#
# i=0
# while i < len(segments):
#     t_test_temp = pd.DataFrame()
#     test = rp.ttest(group1= segments[i]['compound'][segments[i]['class'] == 'human'], group1_name= "human",
#         group2= segments[i]['compound'][segments[i]['class'] == 'simple'], group2_name= "simple")
#     t_test_temp = t_test_temp.append(test)
#     test = rp.ttest(group1= segments[i]['compound'][segments[i]['class'] == 'human'], group1_name= "human",
#         group2= segments[i]['compound'][segments[i]['class'] == 'sophisticated'], group2_name= "sophisticated")
#     t_test_temp = t_test_temp.append(test)
#     test = rp.ttest(group1= segments[i]['compound'][segments[i]['class'] == 'simple'], group1_name= "simple",
#         group2= segments[i]['compound'][segments[i]['class'] == 'sophisticated'], group2_name= "sophisticated")
#     t_test_temp = t_test_temp.append(test)
#     t_test_temp = t_test_temp.set_index(segments[i].iloc[0:39,0])
#     t_test = t_test.append(t_test_temp)
#
#     i = i+1
# t_test.to_csv('sentiment_t-tests.csv')
entire_set = pd.DataFrame()
statistic, pvalue = stats.kruskal(split_cols['compound'][split_cols['class'] == 'human'],
                                  split_cols['compound'][split_cols['class'] == 'simple'],
                                  split_cols['compound'][split_cols['class'] == 'sophisticated'])
temp_results = pd.DataFrame([(str(statistic)), str(pvalue)]).transpose()
entire_set = entire_set.append(temp_results)


kruskal_w_results = pd.DataFrame()
i = 0
while i <len(segments):
   statistic , pvalue = stats.kruskal(segments[i]['compound'][segments[i]['class'] == 'human'],
                                    segments[i]['compound'][segments[i]['class'] == 'simple'],
                                    segments[i]['compound'][segments[i]['class'] == 'sophisticated'])
   temp_results = pd.DataFrame([str(segments[i].iloc[1,0]),str(statistic), str(pvalue)]).transpose()
   kruskal_w_results = kruskal_w_results.append(temp_results)
   i += 1

import scikit_posthocs as sp
dunn_test = pd.DataFrame()
i=0
while i < len(segments):
    x = kruskal_w_results.iloc[i,2]
    dunn_temp = pd.DataFrame()
    if float(x) < 0.05:
        #replace all these with Dunn
        import scikit_posthocs as sp
        # using the posthoc_dunn() function
        data = [(segments[i]['compound'][segments[i]['class'] == 'human']),
                (segments[i]['compound'][segments[i]['class'] == 'simple']),
                (segments[i]['compound'][segments[i]['class'] == 'sophisticated'])]

        p_values = sp.posthoc_dunn(data, p_adjust='holm')
        p_values = pd.DataFrame(["timeframe", (kruskal_w_results.iloc[i,0]),kruskal_w_results.iloc[i,0],kruskal_w_results.iloc[i,0]]).transpose().append(p_values)
        dunn_test = dunn_test.append(p_values)
        print(i, "was tested pairwise")
        i += 1
        continue
    else:
        i += 1
dunn_test.to_csv("dunn_test_timeframes")



i = 0
while i <len(segments):
    plt.hist(segments[i]['compound'][segments[i]['class'] == 'human'] , bins=20)
    plt.hist(segments[i]['compound'][segments[i]['class'] == 'simple'] , bins=20)
    plt.hist(segments[i]['compound'][segments[i]['class'] == 'sophisticated'] , bins=20)
    #plt.plot(h)
    plt.ylabel('frequency')
    plt.xlabel('compound sentiment')
    plt.show()
    i += 1

descriptives = pd.DataFrame()
i = 0
while i < len(segments):
     timeframe = pd.DataFrame()
     humans = (segments[i]['compound'][segments[i]['class'] == 'human']).describe()
     timeframe = timeframe.append(humans)
     simple = (segments[i]['compound'][segments[i]['class'] == 'simple']).describe()
     timeframe = timeframe.append(simple)
     sophisticated = (segments[i]['compound'][segments[i]['class'] == 'sophisticated']).describe()
     timeframe = timeframe.append(sophisticated)

     descriptives = descriptives.append(timeframe)
     i += 1
descriptives.to_csv("timesegment_descriptives.csv")

# def shapiro_test(x):
#     a = 0.05
#     test = stats.shapiro(x)
#     if test.pvalue <= 0.05:
#         return f'The distribution departed from normality significantly, W= {round(test.statistic,2)}, P value= {round(test.pvalue,2)}'
#     else:
#         return f"Shapiro Wilk Test result didn't show non-normality, W= {round(test.statistic,2)}, P value= {round(test.pvalue,2)}. There is no evidence to reject the null hypothesis of normality."
#
# i = 0
# unique_classes = split_cols['class'].unique()
# while i < len(segments):
#     for classes in unique_classes:
#
#         print(shapiro_test(segments[i][segments[i]['class'] == classes]['compound']))
#     i += 1
#
#
# import matplotlib.pyplot as plt
# h = list(split_cols['compound'])
# h.sort()
# i = 1
# plt.hist(segments[i]['compound'][segments[i]['class'] == 'human'] , bins=20)
# plt.hist(segments[i]['compound'][segments[i]['class'] == 'simple'] , bins=20)
# plt.hist(segments[i]['compound'][segments[i]['class'] == 'sophisticated'] , bins=20)
# #plt.plot(h)
# plt.ylabel('frequency')
# plt.xlabel('compound sentiment')
# plt.show()
#
# i = 0
# unique_classes = split_cols['class'].unique()
# while i < len(segments):
#     for classes in unique_classes:
#         stats.probplot(segments[i][segments[i]['class'] == classes]['compound'], dist="norm", plot=plt)
#         plt.title("Probability Plot - " +  classes)
#         plt.show()
#     i += 1



# #Graph sentiment per class over time
# timeline = pd.DataFrame(split_cols["created_at"])
#
# human_sentiment = split_cols[split_cols['class'] == 'human']  # save all rows with 'human' in class column separately
# human_sentiment = pd.concat([human_sentiment, timeline], axis=1, keys="created_at",ignore_index=True)
# human_sentiment.iloc[:, 7] = pd.to_datetime(human_sentiment.iloc[:, 7])  # convert the time column to the datetime data type
# human_sentiment.set_index(human_sentiment.iloc[:, 7], inplace=True)  # replace the row names with the datetime made previously
# human_sentiment.set_axis(['human_time','class', 'text','neg', 'neu','pos','compound','overall_time'], axis=1,inplace=True)  # set column names for easier graphing
#
# simple_sentiment = split_cols[split_cols['class'] == 'simple']  # save all rows with 'simple' in class column separately
# simple_sentiment = pd.concat([simple_sentiment, timeline], axis=1, keys="created_at",ignore_index=True)
# simple_sentiment.iloc[:, 7] = pd.to_datetime(simple_sentiment.iloc[:, 7])  # convert the time column to the datetime data type
# simple_sentiment.set_index(simple_sentiment.iloc[:, 7], inplace=True)  # replace the row names with the datetime made previously
# simple_sentiment.set_axis(['simple_time','class', 'text','neg', 'neu','pos','compound','overall_time'], axis=1,inplace=True)
#
# sophisticated_sentiment = split_cols[split_cols['class'] == 'sophisticated']  # save all rows with 'sophisticated' in class column separately
# sophisticated_sentiment = pd.concat([sophisticated_sentiment, timeline], axis=1, keys="created_at",ignore_index=True)
# sophisticated_sentiment.iloc[:, 7] = pd.to_datetime(sophisticated_sentiment.iloc[:, 7])  # convert the time column to the datetime data type
# sophisticated_sentiment.set_index(sophisticated_sentiment.iloc[:, 7], inplace=True)  # replace the row names with the datetime made previously
# sophisticated_sentiment.set_axis(['sophisticated_time','class', 'text','neg', 'neu','pos','compound','overall_time'], axis=1,inplace=True)
#
# #constructing segments to be used on x axis
# timeline.iloc[:, 0] = pd.to_datetime(timeline.iloc[:, 0])
# timeline.set_index(timeline.iloc[:,0], inplace=True)
# over15min_timeline = timeline.groupby(pd.Grouper(freq='15T')).sum()  # group all occurences by segments of 15mins (the useful part is grouping our overall timeline) | .count() isn't neccessary here?
# over15min_human = human_sentiment.groupby(pd.Grouper(freq='15T')).mean()  # group all human used hashtag occurances by segments of (# before 't') mins
# over15min_simple = simple_sentiment.groupby(pd.Grouper(freq='15T')).mean()
# over15min_sophisticated = sophisticated_sentiment.groupby(pd.Grouper(freq='15T')).mean()
#
#
# #Graphing
# f = plt.figure() #saves figure to be shown into 'f', allows for exporting later
# plt.plot(timeline.index, human_sentiment["compound"], label = "human")
# plt.plot(timeline.index, simple_sentiment["compound"], label = "simple")
# plt.plot(timeline.index, sophisticated_sentiment["compound"], label = "sophisticated")
# plt.ylim(-1, 1)
#
# #plt.plot(over15min_timeline.index, over15min_bot.cum_sum, label="bot")#FOR CUMULATIVE
# plt.plot(over15min_timeline.index, over15min_timeline.screen_name, label = "combined", )
#
# timeline = pd.DataFrame(split_cols["created_at"])
#
# human_sentiment = split_cols[split_cols['class'] == 'human']  # save all rows with 'human' in class column separately
# human_sentiment = pd.concat([human_sentiment, timeline], axis=1, keys="created_at",ignore_index=True)
# human_sentiment.iloc[:, 7] = pd.to_datetime(human_sentiment.iloc[:, 7])  # convert the time column to the datetime data type
# human_sentiment.set_index(human_sentiment.iloc[:, 7], inplace=True)  # replace the row names with the datetime made previously
# human_sentiment.set_axis(['human_time','class', 'text','neg', 'neu','pos','compound','overall_time'], axis=1,inplace=True)  # set column names for easier graphing
#
# simple_sentiment = split_cols[split_cols['class'] == 'simple']  # save all rows with 'simple' in class column separately
# simple_sentiment = pd.concat([simple_sentiment, timeline], axis=1, keys="created_at",ignore_index=True)
# simple_sentiment.iloc[:, 7] = pd.to_datetime(simple_sentiment.iloc[:, 7])  # convert the time column to the datetime data type
# simple_sentiment.set_index(simple_sentiment.iloc[:, 7], inplace=True)  # replace the row names with the datetime made previously
# simple_sentiment.set_axis(['simple_time','class', 'text','neg', 'neu','pos','compound','overall_time'], axis=1,inplace=True)
#
# sophisticated_sentiment = split_cols[split_cols['class'] == 'sophisticated']  # save all rows with 'sophisticated' in class column separately
# sophisticated_sentiment = pd.concat([sophisticated_sentiment, timeline], axis=1, keys="created_at",ignore_index=True)
# sophisticated_sentiment.iloc[:, 7] = pd.to_datetime(sophisticated_sentiment.iloc[:, 7])  # convert the time column to the datetime data type
# sophisticated_sentiment.set_index(sophisticated_sentiment.iloc[:, 7], inplace=True)  # replace the row names with the datetime made previously
# sophisticated_sentiment.set_axis(['sophisticated_time','class', 'text','neg', 'neu','pos','compound','overall_time'], axis=1,inplace=True)
#
#
# over15min_human = human_sentiment.groupby(pd.Grouper(freq='360T')) # group all human used hashtag occurances by segments of (# before 't') mins
# over15min_simple = simple_sentiment.groupby(pd.Grouper(freq='360T'))
# over15min_sophisticated = sophisticated_sentiment.groupby(pd.Grouper(freq='360T'))
#
#
#
#
# f = plt.figure() #saves figure to be shown into 'f', allows for exporting later
# plt.plot(first_period.index, first_period["compound"][first_period["class"]=="human"], label = "human")
# plt.plot(timeline.index, simple_sentiment["compound"], label = "simple")
# plt.plot(timeline.index, sophisticated_sentiment["compound"], label = "sophisticated")
# plt.ylim(-1, 1)


timeline = pd.DataFrame(split_cols["created_at"])
#timeline.iloc[:, 0] = pd.to_datetime(timeline.iloc[:, 0])

human_sentiment = split_cols[split_cols['class'] == 'human']  # save all rows with 'human' in class column separately
human_sentiment = pd.concat([human_sentiment, timeline], axis=1, keys="created_at",ignore_index=True)
human_sentiment.index = pd.to_datetime(timeline.iloc[:, 0])
human_sentiment = human_sentiment.groupby(pd.Grouper(freq='60T')).mean()

simple_sentiment = split_cols[split_cols['class'] == 'simple']  # save all rows with 'human' in class column separately
simple_sentiment = pd.concat([simple_sentiment, timeline], axis=1, keys="created_at",ignore_index=True)
simple_sentiment.index = pd.to_datetime(timeline.iloc[:, 0])
simple_sentiment = simple_sentiment.groupby(pd.Grouper(freq='60T')).mean()

sophisticated_sentiment = split_cols[split_cols['class'] == 'sophisticated']  # save all rows with 'human' in class column separately
sophisticated_sentiment = pd.concat([sophisticated_sentiment, timeline], axis=1, keys="created_at",ignore_index=True)
sophisticated_sentiment.index = pd.to_datetime(timeline.iloc[:, 0])
sophisticated_sentiment= sophisticated_sentiment.groupby(pd.Grouper(freq='60T')).mean()

timeline.index = pd.to_datetime(timeline.iloc[:, 0])
timeline = timeline.groupby(pd.Grouper(freq='60T')).mean()

#data = [human_sentiment["compound"],simple_sentiment["compound"],sophisticated_sentiment["compound"]]
f = plt.figure() #saves figure to be shown into 'f', allows for exporting later
plt.plot(timeline.index, human_sentiment.iloc[:,3], label = "human")
plt.plot(timeline.index, simple_sentiment.iloc[:,3], label = "simple")
plt.plot(timeline.index, sophisticated_sentiment.iloc[:,3], label = "sophisticated")
plt.title("Compound sentiment over time")
plt.legend()
plt.grid()
plt.ylim(-.6, .6)
plt.show()





text["counter"] = 1
#######actual graphs##########
bots = ["simple","sophisticated"]


    hashtag_in_question = hashtags_with_more_than_15_occurrences[i] #pick a hashtag from the more than 50 occurances list CHANGE 0 TO i FOR LOOP LATER
    hashtag_in_question_occurrences = (more_than[more_than['hashtag'] == hashtag_in_question]).reset_index(drop=True) #save all occurances of picked hashtag in a new dataframe?

    #changing time to somethin python can read
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
    hashtag_in_question_occurrences.set_index('posted_at', inplace=True, drop= False) #sets datetime as index (row names) ---- works despite error


    more_than[more_than['hashtag'] == hashtag_in_question
    #constructing segments to be used on x axis
    over15min_timeline = hashtag_in_question_occurrences.groupby(pd.Grouper(freq='15T')).count() #group all occurences by segments of 20mins (the useful part is grouping our overall timeline) | .count() isn't neccessary here?

    over15min_human = human_used.groupby(pd.Grouper(freq='15T')).count() #group all human used hashtag occurances by segments of (# before 't') mins
    over15min_human['cum_sum'] = over15min_human['hashtag'].cumsum()

    over15min_bot = bot_used.groupby(pd.Grouper(freq='15T')).count()
    over15min_bot['cum_sum'] = over15min_bot['hashtag'].cumsum()

    # graph
    f = plt.figure() #saves figure to be shown into 'f', allows for exporting later
    plt.plot(over15min_timeline.index, over15min_human.cum_sum, label="human")#FOR CUMULATIVE
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



