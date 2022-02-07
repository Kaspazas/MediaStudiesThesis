import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#import data
df = pd.read_csv("sentiment_analysis_test_sample.csv")

#a function to clean text up
def clean(text):
    text = re.sub(r'http\S+', '', text)
    #re.sub("â€™", "(?<=[a-z])'(?=[a-z])", text) #ACTUALLY NOT NEEDED, THE ERROR THE TEXT DISTORTION THAT APPEARS IN EXCEL DOES NOT EXIST HERE
    return text

df['cleaned'] = df['text'].apply(clean)

#vader is actually used by others
analyzer = SentimentIntensityAnalyzer()

#create function
def vadersentimentanalysis(tweet):
    sentiment = (analyzer.polarity_scores(tweet))
    return sentiment

#use function
df['sentiment'] = df['cleaned'].apply(vadersentimentanalysis)

#save results
df.to_csv('sentiment_done_with_time.csv')
