import pandas as pd
import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import seaborn as sns
from datetime import datetime
import time
import matplotlib.pyplot as plt
import researchpy as rp
import scipy.stats as stats

#Import text, class, hashtags from originally downloaded data
#topic_tweet = pd.read_csv('tweet_id_topic.csv').iloc[:,1:]
dataset = pd.read_csv("topic_modeling_results.csv")
#dataset["topic"] = topic_tweet['topic']

#Run VADER sentiment analysis
analyzer = SentimentIntensityAnalyzer()

#create function
def vadersentimentanalysis(tweet):
    sentiment = (analyzer.polarity_scores(tweet))
    return sentiment

dataset['sentiment'] = dataset['text'].apply(vadersentimentanalysis)

split_cols = pd.concat([dataset, dataset["sentiment"].apply(pd.Series)], axis=1)
split_cols = split_cols.drop(columns="sentiment")

#separate by topic group
topic_0 = split_cols[split_cols.topic == "0.0"]
topic_1 = split_cols[split_cols.topic == "1.0"]
topic_2 = split_cols[split_cols.topic == "2.0"]
topic_3 = split_cols[split_cols.topic == "3.0"]
topic_4 = split_cols[split_cols.topic == "4.0"]
topic_5 = split_cols[split_cols.topic == "5.0"]
topic_6 = split_cols[split_cols.topic == "6.0"]
topic_7 = split_cols[split_cols.topic == "7.0"]
topic_8 = split_cols[split_cols.topic == "8.0"]
topic_9 = split_cols[split_cols.topic == "9.0"]
topic_10 = split_cols[split_cols.topic == "10.0"]
topic_11 = split_cols[split_cols.topic == "11.0"]
topic_12 = split_cols[split_cols.topic == "12.0"]
#Run T tests on VADER data of each segment, comparing classes of users
segments = [topic_0,topic_1,topic_2,topic_3,topic_4,topic_5,topic_6,topic_7,topic_8,topic_9,topic_10,topic_11,topic_12]

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
t_test.to_csv('topic_sentiment_t-tests.csv')

