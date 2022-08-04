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

#Segment data into 6 hour periods
split_cols.iloc[:, 0] = pd.to_datetime(split_cols.iloc[:, 0])
split_cols = split_cols.set_index(split_cols['created_at'])
split_cols = split_cols.sort_index()

first_period = split_cols['2022-01-09T00:00:00':'2022-01-09T06:00:00']
second_period = split_cols['2022-01-09T06:00:00':'2022-01-09T12:00:00']
third_period = split_cols['2022-01-09T12:00:00':'2022-01-09T18:00:00']
fourth_period = split_cols['2022-01-09T18:00:00':'2022-01-10T00:00:00']
fifth_period = split_cols['2022-01-10T00:00:00':'2022-01-10T06:00:00']
sixth_period = split_cols['2022-01-10T06:00:00':'2022-01-10T12:00:00']
seventh_period = split_cols['2022-01-10T12:00:00':'2022-01-10T18:00:00']
eight_period = split_cols['2022-01-10T18:00:00':'2022-01-11T06:00:00']
ninth_period = split_cols['2022-01-11T06:00:00':'2022-01-11T12:00:00']
tenth_period = split_cols['2022-01-11T12:00:00':'2022-01-11T18:00:00']
eleventh_period = split_cols['2022-01-11T18:00:00':'2022-01-12T00:00:00']
twelfth_period = split_cols['2022-01-12T00:00:00':'2022-01-12T06:00:00']
thirteenth_period = split_cols['2022-01-12T06:00:00':'2022-01-12T12:00:00']

segments = [first_period, second_period, third_period,fourth_period,fifth_period,sixth_period,seventh_period,eight_period,ninth_period,tenth_period,eleventh_period,twelfth_period,thirteenth_period]
#Run T-tests between classes in each 6-hour segment
t_test = pd.DataFrame()

i=0
while i < len(segments):
    t_test_temp = pd.DataFrame()
    test = rp.ttest(group1= segments[i]['compound'][segments[i]['class'] == 'human'], group1_name= "human",
        group2= segments[i]['compound'][segments[i]['class'] == 'simple'], group2_name= "simple")
    t_test_temp = t_test_temp.append(test)
    test = rp.ttest(group1= segments[i]['compound'][segments[i]['class'] == 'human'], group1_name= "human",
        group2= segments[i]['compound'][segments[i]['class'] == 'sophisticated'], group2_name= "sophisticated")
    t_test_temp = t_test_temp.append(test)
    test = rp.ttest(group1= segments[i]['compound'][segments[i]['class'] == 'simple'], group1_name= "simple",
        group2= segments[i]['compound'][segments[i]['class'] == 'sophisticated'], group2_name= "sophisticated")
    t_test_temp = t_test_temp.append(test)
    t_test_temp = t_test_temp.set_index(segments[i].iloc[0:39,0])
    t_test = t_test.append(t_test_temp)

    i = i+1
t_test.to_csv('sentiment_t-tests.csv')








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