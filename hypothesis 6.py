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
mean = pd.concat([dataset, dataset["sentiment"].apply(pd.Series)], axis=1)


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

kruskal_broad_results = pd.DataFrame()
i=0
while i< len(segments):
    kruskal_temp = pd.DataFrame()
    statistic, pvalue = stats.kruskal(segments[i]['compound'][segments[i]['class'] == 'human'],
                                      segments[i]['compound'][segments[i]['class'] == 'simple'],
                                      segments[i]['compound'][segments[i]['class'] == 'sophisticated'])
    kruskal_temp = pd.DataFrame([str(segments[i].iloc[0,6]), str(statistic), str(pvalue)]).transpose()
    kruskal_broad_results = kruskal_broad_results.append(kruskal_temp)
    i +=1
kruskal_broad_results.to_csv('kruskal_wallis-tests-broad-topics.csv')

dunn_test = pd.DataFrame()
i=0
while i < len(segments):
    x = kruskal_broad_results.iloc[i,2]
    dunn_temp = pd.DataFrame()
    if float(x) < 0.05:
        #replace all these with Dunn
        import scikit_posthocs as sp
        # using the posthoc_dunn() function
        data = [(segments[i]['compound'][segments[i]['class'] == 'human']),
                (segments[i]['compound'][segments[i]['class'] == 'simple']),
                (segments[i]['compound'][segments[i]['class'] == 'sophisticated'])]

        p_values = sp.posthoc_dunn(data, p_adjust='holm')
        p_values = pd.DataFrame(["topic", (kruskal_broad_results.iloc[i,0]),kruskal_broad_results.iloc[i,0],kruskal_broad_results.iloc[i,0]]).transpose().append(p_values)
        dunn_test = dunn_test.append(p_values)
        print(i, "was tested pairwise")
        i += 1
        continue
    else:
        i += 1
dunn_test.to_csv('dunn-test-topics.csv')

(mean[mean["class"] == "human"]['compound']).describe()
(mean[mean["class"] == "simple"]['compound']).describe()
(mean[mean["class"] == "sophisticated"]['compound']).describe()

(mean[mean["class"] == "human"]['compound']).median()
(mean[mean["class"] == "simple"]['compound']).median()
(mean[mean["class"] == "sophisticated"]['compound']).median()

i = 0
descriptives_table = pd.DataFrame()
while i < len(segments):
    print("topic " + str(i))
    # print(segments[i][segments[i]["class"] == "human"]["compound"].mean())
    # print(segments[i][segments[i]["class"] == "simple"]["compound"].mean())
    # print(segments[i][segments[i]["class"] == "sophisticated"]["compound"].mean())
    descriptives_h = pd.DataFrame(segments[i][segments[i]["class"] == "human"]["compound"].describe()).transpose()
    descriptives_table = descriptives_table.append(descriptives_h)
    descriptives_bb = pd.DataFrame(segments[i][segments[i]["class"] == "simple"]["compound"].describe()).transpose()
    descriptives_table = descriptives_table.append(descriptives_bb)
    descriptives_sb = pd.DataFrame(segments[i][segments[i]["class"] == "sophisticated"]["compound"].describe()).transpose()
    descriptives_table = descriptives_table.append(descriptives_sb)
    i+=1
descriptives_table.to_csv("topic_sentiment_descriptives.csv")





