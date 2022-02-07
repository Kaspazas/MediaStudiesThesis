import pandas as pd

mentions_network = pd.read_csv("antivax_mentions.csv") #data needs to presented in a two column format, where column 1 is the tweeter and column 2 is mentioned users (if multiple separated by space)
i = 0
print('gonna run', (len(mentions_network)-1), 'iterations')

## mention CO-OCCURENCE ## #heres some brackets cause your keyboard sucks []
coocurence_list = pd.DataFrame({'created_at': ['nan'],'tweeter': ['nan'], 'mentioned_user': ['nan']}) #creates a blank dataframe that we will append to later(easiest way of doing it for me)

i = 0

while i < len(mentions_network):
    current_tweeter = mentions_network.iloc[i,0] #saves the original tweeters username separetely
    current_mentions = mentions_network.iloc[i,1] #saves the mentioned users cell
    current_mentions = current_mentions.split() #creates a list of those mentioned, separates cell contents if needed
    current_lenght = len(current_mentions) #counts how many users were mentioned

    if current_lenght < 2: #if only one user is mentioned
        tweeter = current_tweeter
        mentioned_user = str(current_mentions[0]) #selects the first (in this case only) mentioned username
        temporary_coocurance = pd.DataFrame({'tweeter': [str(tweeter)], 'mentioned_user': [str(mentioned_user)]}) #creates a dataframe that combines the tweeters username with the username of the mentioned
        coocurence_list = pd.concat([coocurence_list, temporary_coocurance], axis=0) #combines the dataframe created in previous line with our blanc datatable created on line ~8

    else: #if more than one user is mentioned
        y = 0 #creates arbritrary variable to use for loop, where y serves to identify which of the mentioned users we're currently working with

        while y < current_lenght: #loops through each mentioned user, adding them to a dataframe with the user who mentioned them and adding that to our total adjecentcy list
            tweeter = current_tweeter
            mentioned_user = str(current_mentions[y])

            temporary_coocurance = pd.DataFrame({'tweeter': [str(tweeter)], 'mentioned_user': [str(mentioned_user)]})
            coocurence_list = pd.concat([coocurence_list, temporary_coocurance], axis=0)

            y = y + 1

    i = i + 1

export_name_cooc = ('antivax_directed_mentions.csv')
coocurence_list.iloc[1:, :].to_csv(export_name_cooc, index=False)
