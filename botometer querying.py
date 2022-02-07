import botometer
import tweepy
import csv
import pandas as pd
import time

#botometer api key
rapidapi_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

twitter_app_auth = {
    'consumer_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'consumer_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'access_token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'access_token_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
  }
#defining the call
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)


###############################SETUP###############################

#make data frame for first time setup
# checker = {'order_no':[],
#         'screen_name':[],
#         'uni_overall':[],
#         'eng_overall':[],
#         }
# checker_df = pd.DataFrame (checker, columns = ['order_no','screen_name','uni_overall','eng_overall'])

#if not first time, load previous results
full_list = pd.read_csv('userlist') #load in csv where column A is order number and column B is usernames
checker_df = pd.read_csv('testing_results.csv') #load in previous checks

order_temp = checker_df.tail(1)#getting back to the position we were in
order_no_check = order_temp.iat[0,0] + 1#still getting back, this and the line above could probably be done differently but idk how

#check remaining botometer calls at https://rapidapi.com/developer/dashboard
#####################################LOOP####################################### 
#The loop takes usernames and an order number (from 0 to last item's position in a list)
#It then passes the username on to botometer and saves the order number in the results dataframe
#The order number is used to identify how far down the list we're on
#Botometer provides the user with a lot of variables, but this only saves universal and english probabilities of the user being a bot (see botometer documentation)

loop_ln = len(full_list)
print("starting loop ", loop_ln," iterations")

i=0
while(i <= loop_ln): #set iteration number, keep in mind you're limited to 2k per day otherwise you pay 0.001$ per user)

    order_temp = checker_df.tail(1)#getting back to the position we were in         
    order_no_check = order_temp.iat[0,0] + 1#still getting back                 

    username = full_list['screen_name'][order_no_check]#getting the username that's next in the list to be checked
    print("got username:", username,)


    try:
        result = bom.check_account(username)#Get bot probability

    # except requests.exceptions.ConnectionError: as e: #NOT TESTED Error handling for internet outage, won't work if internet is completely down
    #   print("Some network error, waiting 30 seconds")
    #   time.sleep(30)
    #   result = bom.check_account(username)  # Get bot probability
    #   temp_results  = {'order_no':order_no_check, 'screen_name':username, 'uni_overall':result['raw_scores']['universal']['overall'], 'eng_overall':result['raw_scores']['english']['overall']}
    #   checker_df = checker_df.append(temp_results, ignore_index=True)
    #   continue

    except tweepy.error.TweepError as e: #wtitter error handling, if something goes wrong this should still provide the username and position, but give 'na' as probability
        print(i, 'is missing')
        temp_results = {'order_no': order_no_check, 'screen_name': username,
                        'uni_overall': 'na',
                        'eng_overall': 'na'}
        checker_df = checker_df.append(temp_results, ignore_index=True)
        i += 1
        continue

    except botometer.NoTimelineError as e: #botometer error handling, if something goes wrong this should still provide the username and position, but give 'na' as probability
        print(i, 'has no tweets')
        temp_results = {'order_no': order_no_check, 'screen_name': username,
                        'uni_overall': 'na',
                        'eng_overall': 'na'}
        checker_df = checker_df.append(temp_results, ignore_index=True)
        i += 1
        continue


###save bot probability in data frame###
    temp_results  = {'order_no':order_no_check, 'screen_name':username, 'uni_overall':result['raw_scores']['universal']['overall'], 'eng_overall':result['raw_scores']['english']['overall']}
    checker_df = checker_df.append(temp_results, ignore_index=True)

########################################
    checker_df.to_csv('testing_results_missing.csv', index=False)
    print("done with number", order_no_check, "overall. This loop, iteration", i, "out of", loop_ln) #tells us which iteration we're on
    i +=1 #changes to next iteration

else:
    print('done with loop') #once iteration number is reached, it says so
    print('we are at', order_no_check,'users done')
    checker_df.to_csv('testing_results.csv',index=False)
