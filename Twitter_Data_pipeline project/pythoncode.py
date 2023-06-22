# in cmd of windows 
# sudo apt-get update
# pip install pandas,numpy
# pip install tweepy
# pip install s3fs (store to read,write data from s3 bucket)

import tweepy
import pandas as pd
import json
from datetime import datetime 
import s3fs
def twitter_etl():
   access_key = "xVo5aetRgiSQumjWpmmtEiKF7"
   access_key_secret="PPUiiL3J9UYXxnfqeIzN4tKYMXtYPeuXu7HMKGVnvdP3SeoN3M"
   access_token = "1644786445847236609-s6b9NEBUlAWVSgPwxTzAnGPlLO2Rup"
   access_token_secret="U81KTI2W9vUcz8sEMtxPWF2ylIkADcpdFujlcEPc7p50o"

   # twitter authentication
   auth = tweepy.OAuthHandler(access_key,access_key_secret)
   auth.set_access_token(access_token,access_token_secret)

   # creating a Api object
   api = tweepy.API(auth)

   tweets = api.user_timeline(screen_name='@elonmusk',
                           #    200 is the maximum allowed count
                              count = 200,
                              include_rts=False,
                           #    necessary to keep full_text
                           # otherwise only the first 140 words are executed
                              tweet_mode = 'extended')

   # for testing purpose 
   # print(tweets) and go to the folder in cmd, where the file is saved, then type python or python3 then name of this file 
   # print(tweets)
   # You currently Ihave access to a subset of Twitter API v2 endpoints and limited v1.1 endpoints (e.g. media post, oauth) only. 
   # If you need access to this endpoint, you may need a different access level. You can learn more here:
   # https://developer.twitter.com/en/portal/product

   # getting the above error it means the code is correct only the access level is not paid one.

   # extracting the data from the tweets
   tweet_list=[]

   for tweet in tweets:
      text = tweet.json["Full_text"]


      refined_tweet = {"user":tweet.user.screen.name,
                        "text":text,
                        "favorite_count":tweet.favorite_count,
                        "retweet_count":tweet.retweet_count,
                        "created_at":tweet.created_at}
      
      tweet_list.append(refined_tweet)


      df = pd.DataFrame(tweet_list)

      # then it will save this dataframe into the bucket
      df.to_csv("s3://bucket-name/elonmusk_twitter_data.csv")