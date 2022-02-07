#install packages
install.packages("rtweet")
install.packages("httpuv")

library(rtweet)
library(httpuv)

app = "xxxxxxxxxxxxxxxxxxxxx" #app name
consumer_key = "xxxxxxxxxxxxxxxxxxxxx" #API key
consumer_secret = "xxxxxxxxxxxxxxxxxxxxx" #API secret key
access_token="xxxxxxxxxxxxxxxxxxxxx" #Access token
access_secret="xxxxxxxxxxxxxxxxxxxxx" #Access token secret


#create a signature(token/whatever) that gets passed on to Twitter when Botometer makes calls
myapp = oauth_app("twitter", key = consumer_key, secret = consumer_secret)
sig = sign_oauth1.0(myapp, token=access_token, token_secret=access_secret)


#dowloading tweets
tweets <- search_tweets2("antivaxx OR antivaxxers OR #antivax OR #VAXXEDvsANTIVAXX", n = 25000, retryonratelimit = TRUE, lang = "en") 
save_as_csv(tweets, 'dataset.csv')