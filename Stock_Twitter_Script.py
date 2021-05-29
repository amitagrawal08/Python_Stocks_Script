#! /usr/bin/python3.6

import tweepy
import pandas as pd
import os
from tweepy.streaming import StreamListener

Input_list =[]
input_data= pd.read_csv('/root/script/Alerts.txt', header=None)
for i in input_data[0]:
    Input_list.append(i.strip())
print(Input_list)

output = []

CONSUMER_KEY="HIgeXNsl8uVMWKwGZmcTRnygz"
CONSUMER_SECRET="nyeodxBad7kPsxlNqXMbvKSZpIHolp2ghVgfNx4hzbGoZJym6E"
ACCESS_TOKEN="467586857-O6VdHaNXBkt3MrdaPVLQSnJQJAePO0Q1bS608Lw5"
ACCESS_TOKEN_SECRET="xVYczsZrHaHlHuVWbTMnQ7phlIVFl2quR5L6RGUDCAweJ"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

tweetid = []
tweetdate = []
tweettext = []

new_tweets = api.user_timeline(screen_name = 'BSE_News', count=100)
for tweet in new_tweets:
    tweetid.append(tweet.id)
    tweetdate.append(str(tweet.created_at))
    tweettext.append(tweet.text.split('-')[0].strip())

new_data = pd.DataFrame({'tweetid': tweetid, 'tweetdate':tweetdate, 'tweettext':tweettext})
new_data.columns=['tweetid','tweetdate','tweettext']
column_names=['tweetid','tweetdate','tweettext']
new_data1=set(new_data['tweetid'])
#print(new_data1)

if not os.path.isfile('/root/script/filename.csv'):
    old_data1=set()
else:
    old_data = pd.read_csv('/root/script/filename.csv')
    old_data1=set(old_data['tweetid'])
#    print(old_data1)

main_data = new_data1 - old_data1
#print(main_data)

main_data_txt = []
if len(main_data) != 0:
    for id in main_data:
        ref = new_data[new_data['tweetid'] == id]['tweettext']
        for index, value in ref.items():
            main_data_txt.append(value)
#print(main_data_txt)

compl_tweet={}
for tweet in new_tweets:
    compl_tweet[tweet.text.split('-')[0].strip(), tweet.id] = tweet.text
#print(compl_tweet)

for value in main_data_txt:
    for num in compl_tweet.keys():
        if value in Input_list and value == num[0]:
                output.append(str(compl_tweet[num])[:50])
        else:
            pass
print(set(output))

# if file does not exist write header
if not os.path.isfile('/root/script/filename.csv'):
    new_data.to_csv('/root/script/filename.csv', index=False, header='column_names')
else: # else it exists so append without mentioning the header
    new_data.to_csv('/root/script/filename.csv', mode='w', index=False, header='column_names')


# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure

account_sid = 'AC2a6ee3c21e8cae6a6d11da1a16b6f464'
auth_token = 'eb0d8929d0d45d8ae88f17abfee7ae28'
client = Client(account_sid, auth_token)

# get response
if len(output) == 0:
    print ("No change observed")
else:
    print ("Changes observed")
    message = client.messages.create(body=output, from_='+12057408537', to='+917906334114')
    print(message.sid)
#message = client.messages.create(body=output, from_='+12057408537', to='+917983001266')

#print(message.sid)

