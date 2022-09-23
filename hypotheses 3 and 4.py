import pandas as pd
import spacy
from spacy import tokens
import gensim
import matplotlib.pyplot as plt
import seaborn
from gensim import corpora, models
from pprint import pprint
import re

# #Creating a hashtag adjecency list for Gephi
# hashtags_with_time = pd.read_csv('hashtags.csv')
# hashtags_in_posts = pd.read_csv('hashtags.csv').iloc[:,2:]
# cooccurrence_list = pd.DataFrame({'first': ['nan'], 'second': ['nan']})
#
# i = 0
# while i < len(hashtags_in_posts):
#     current_hashtags = hashtags_in_posts.iloc[i]
#     current_hashtags = current_hashtags[~pd.isnull(current_hashtags)]
#     current_lenght = current_hashtags.count()
#
#     if current_lenght < 2:
#         first_hashtag = current_hashtags[0]
#         second_hashtag = 'nan'
#         temporary_coocurance = pd.DataFrame({'first': [str(first_hashtag)], 'second': [second_hashtag]})
#         cooccurrence_list = pd.concat([cooccurrence_list, temporary_coocurance], axis=0)
#
#     else:
#         x = 0
#
#         while x < current_lenght - 1:
#             y = x + 1
#
#             while y < current_lenght:
#                 first_hashtag = current_hashtags[x]
#                 second_hashtag = current_hashtags[y]
#
#                 temporary_coocurance = pd.DataFrame({'first': [str(first_hashtag)], 'second': [second_hashtag]})
#                 cooccurrence_list = pd.concat([cooccurrence_list, temporary_coocurance], axis=0)
#
#                 y = y + 1
#
#             x = x + 1
#     i = i + 1
#
# cooccurrence_list.to_csv('hashtag_adjecency_list.csv',index=False)
# #making all hashtags lowercase
# i=0
# while i < len(dataset):
#     dataset["hashtags"][i] = dataset["hashtags"][i].lower()
#     print(i)
#     i = i + 1
#
# #Import nodes table with modularity class as metadata
# hashtags = pd.read_csv('')
# #select which topic group is analyzed
# hashtags = hostility
# hashtags = conspiracy
# #Import lists of hashtags belonging to topic group from gephi
#
#
# #Import class and hashtag fields from originally downloaded tweets
#
# #count how many of each class used hashtags belonging to the group being investigated
#
# #perform t test???
#
# #check ratio of humans to bots in topic group

########################Topic modeling##########################
########################### Gensim #############################
################################################################
#requires lematized and tokenized text
import pandas as pd
import re
import spacy
from spacy import tokens
import gensim
from gensim import corpora, models
from pprint import pprint
#https://serials.atla.com/theolib/article/view/2609/3271
#https://github.com/msaxton/tl_topic_model/blob/master/tl_topic_model.py

dataset = pd.read_csv("topic_modeling_data_training.csv")
dataset = pd.read_csv("topic_modeling_data.csv")

def remove_x(status_id):
    status_id = re.sub('x', '', status_id)
    return status_id

dataset['status_id'] = dataset['status_id'].apply(remove_x)


doc_index2article_id = {}
i = 0

for tweet in dataset:
    id = dataset["status_id"]
    doc_index2article_id = {
        i:id
    }
    i +=1


def lowercasing(text):
    text = text.lower()
    return text


dataset['cleaned'] = dataset['text'].apply(lowercasing)
docs = dataset['cleaned']


nlp = spacy.load("en_core_web_sm")
nlp.Defaults.stop_words |= {'find','start','yes','bot','like','tell','tomorrow','amp','view','feel','is','the', 'a', 'an', 'of', 'and', 'or','https', 'as', 'to','by','my','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',}

stop_words = spacy.lang.en.stop_words.STOP_WORDS #load stop words
processed_docs = [] #create a list of tweets thats already processed
for doc in nlp.pipe(docs):
    doc = [token.lemma_ for token in doc if token.is_alpha] #Tokenize tweets
    doc = [token for token in doc if token not in stop_words] #remove stop words
    doc = [token for token in doc if len(token) > 2] #??
    processed_docs.append(doc)

dictionary = corpora.Dictionary(processed_docs)  # create Gensim dictionary which maps word ids to word counts
dictionary.filter_extremes(no_below=10)  # filter out words which are too frequent or too rare
#dictionary.save('tl_corpus.dict')  # save for later use
corpus = [dictionary.doc2bow(doc) for doc in processed_docs]  # initialize Gensim corpus
corpora.MmCorpus.serialize('corpus.mm', corpus)  # save for later use

#Optimize number of groups by coherence value
NUM_TOPICS = 8 #12 was quite good >~.4
chunksize = 2000 #1000 yielded bad results, 1500 was okay ish
passes = 7 #<20 passes for testing, maybe more for final?
iterations = 200 #at 1900 chunksize, 200 iterations, 10 passes best result was with 6 topics
eval_every = 1
temp = dictionary[0]
id2word = dictionary.id2token

model = models.LdaModel(
    corpus=corpus,
    id2word=id2word,
    chunksize=chunksize,
    alpha='auto',
    eta='auto',
    iterations=iterations,
    num_topics=NUM_TOPICS,
    passes=passes,
    eval_every=eval_every
)

def compute_coherence_values(dictionary, corpus, texts,
                             cohere, limit, start, step):

    coherence_values = []
    i=0
    for num_topics in range(start, limit, step):
        print("testing ", (start + i)," topics")

        model = models.LdaModel(corpus=corpus,
                         id2word=dictionary,
                         num_topics=num_topics,
                         chunksize=chunksize,
                         alpha='auto',
                         eta='auto',
                         iterations=iterations,
                         passes=passes,
                         eval_every=eval_every,
                         random_state=42,)

        coherencemodel = models.CoherenceModel(model=model,
                                        texts=processed_docs,
                                        dictionary=dictionary,
                                        coherence=cohere)
        coherence_values.append(coherencemodel.get_coherence())

        print((start + i), " topics has coherence of:", coherencemodel.get_coherence())
        print(model.print_topics())
        i = i +1
    return coherence_values

limit=18
start=7
step=1

#runs testing
coherence_values = compute_coherence_values(dictionary=dictionary,
                                            corpus=corpus,
                                            texts=processed_docs,
                                            cohere='c_v',
                                            start=start,
                                            limit=limit,
                                            step=step)

#at 1900 chunksize, 200 iterations, 10 passes best result was with 6 topics 0.494
#at 1900 chunksize, 150 iterations, 10 passes best result was with 6 topics 0.495


model = models.LdaModel(corpus=corpus,
                        id2word=dictionary,
                        num_topics=13,
                        chunksize=chunksize,
                        alpha='auto',
                        eta='auto',
                        iterations=iterations,
                        passes=passes,
                        eval_every=eval_every,
                        random_state=42, )

model.print_topics()
model.save('lda10.model')
model = models.load('lda10.model')


# assign topic to tweets
i = 0
topic_tweet = pd.DataFrame(columns=['topic','probability']) #in this script the secondary topic group is not saved
for doc in corpus:
    try:
        topics = model.get_document_topics(doc, minimum_probability=0.25) #only get docs with a 30% probability of association
        if len(topics) > 2:
            topics = topics.drop([1])
        if len(topics) == 0:
            topics = {'topic':'inconclusive', 'probability':'na'}
            topic_tweet = topic_tweet.append(topics, ignore_index=True)
            print('doc ', i, '=', topics)
            i=i+1
            continue
        topics = {'topic': topics[0][0], 'probability': topics[0][1]}
        topic_tweet = topic_tweet.append(topics, ignore_index=True)
        print('doc ', i, '=', topics)
    except:
        topics = {'topic': 'inconclusive', 'probability': 'na'}
        topic_tweet = topic_tweet.append(topics, ignore_index=True)
        print('doc ', i, '=', topics)

    i += 1

topic_list = model.print_topics()
topic_tweet.to_csv('tweet_id_topic.csv')

topic_tweet = pd.read_csv('tweet_id_topic.csv').iloc[:,1:]
dataset["topic"] = topic_tweet['topic']
dataset.to_csv('topic_modeling_results.csv')
#dataset12 = dataset[dataset['topic']!= "inconclusive"]

print('number of users in inconclusive: ', dataset["topic"].count('inconclusive'))

#Chi Square test preparation
#count users class per topic
topics_in_tweets = pd.read_csv("topic_modeling_results.csv").iloc[:,1:]
topics = topics_in_tweets["topic"].unique()

users_per_topic = pd.DataFrame()
i = 0
while i < len(topics):
    current = topics_in_tweets[topics_in_tweets["topic"] == topics[i]]
    usercounts = pd.DataFrame([str(topics[i]),len(current[current["class"] == "human"]["class"]),
                              len(current[current["class"] == "simple"]["class"]),
                              len(current[current["class"] == "sophisticated"]["class"])]).transpose()
    users_per_topic = users_per_topic.append(usercounts)
    i += 1

users_per_topic.columns = ["topic","no human", "no simple", "no sophisticated"]
users_per_topic = users_per_topic.sort_values(by=["topic"])
#users_per_topic = users_per_topic.iloc[:13,:]


#calculate expected bot values (bot to human tweet ratio in entire dataset)
expected_users = pd.DataFrame()
i = 0
while i < len(topics):
    current_humans = users_per_topic.iloc[i,1]
    total_users_topic = current_humans + users_per_topic.iloc[i,2] + users_per_topic.iloc[i,3]
    expected_usercounts = pd.DataFrame([str(users_per_topic.iloc[i,0]),
                                        int(current_humans), #humans
                                        round(int(total_users_topic) * 0.1242809771942884), #simple bots
                                        round(int(total_users_topic) * 0.0949786830885836)]).transpose() #sophisticated
    expected_users = expected_users.append(expected_usercounts)
    i += 1
expected_users.columns = ["topic","no human", "no simple", "no sophisticated"]
#expected_users = expected_users.iloc[:13,:]
print(sum(users_per_topic["no simple"]))
print(sum(expected_users["no simple"]))

print(sum(users_per_topic["no sophisticated"]))
print(sum(expected_users["no sophisticated"]))

#do Chi squared tests
import scipy.stats as sp
#issue occurs when rounding expected values: ValueError: For each axis slice, the sum of the observed frequencies must agree with the sum of the expected frequencies to a relative tolerance of 1e-08, but the percent differences are:
#issue occurs because expected value sums are too different than expected results (whether rounding or not)
#chi test function does not accept floats, which could have been used to represent TRUELY expected values

#hence, values are left rounded to nearest int, but for simple bots - two values that were not rounded but had the highest decimal value are to be increased by one (topics 8,12)
#for sophisticated bots - two valies that were rounded but had the lowest decimal value are to be dencreased by one (topics 11,2)

expected_users.iloc[4,2] = int(33) #simple bot count, topic 12
expected_users.iloc[11,2] = int(25) #simple bot count, topic 8

expected_users.iloc[3,3] = int(118) #sophisticated bot count, topic 11
expected_users.iloc[5,3] = int(96) #sophisticated bot count, topic 2

#actual test
#normalize values I guess?
chi_test_simple = sp.chisquare(f_obs= users_per_topic.iloc[:,2],f_exp = expected_users.iloc[:,2]) #???ValueError: For each axis slice, the sum of the observed frequencies must agree with the sum of the expected frequencies to a relative tolerance of 1e-08, but the percent differences are:
chi_test_sophisticated = sp.chisquare(f_obs= users_per_topic.iloc[:,3],f_exp = expected_users.iloc[:,3])

chi_test = sp.chi2_contingency(users_per_topic.iloc[:, 1:])
topic1 = sp.chi2_contingency(list(users_per_topic.iloc[1, 1:]), list(expected_users.iloc[1, 1:]))

#maybe this is the right approach?
topic1 = sp.chi2_contingency([list(users_per_topic.iloc[1, 1:]), list(expected_users.iloc[1, 1:])])

i=0
while i<len(expected_users["topic"]):
    x=0
    while x < len(expected_users.iloc[0,:]):
        print(type(expected_users.iloc[i,x]))
        if isinstance(expected_users.iloc[i,x], str) and x > 0:
            print("fixing")
            expected_users.iloc[i, x] = int(expected_users.iloc[i,x])
            x += 1
        else:
            x += 1
    i += 1



