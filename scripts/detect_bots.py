# Scrape Users' Bot Scores
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 21:47:39 2023

@author: shimeng
"""

# https://botometer.osome.iu.edu/faq
# Bot scores are displayed on a 0-to-5 scale with zero being most human-like and five being the most bot-like. A score in the middle of the scale is a signal that our classifier is uncertain about the classification. On the Botometer Pro API, this is called display score. The API also provides the raw score in the range 0-1.
# For example, suppose an account has a raw bot score of 0.96/1 (equivalent to 4.8/5 display score on the website) and CAP 90%. This means that 90% of accounts with a raw bot score above 0.96 are labeled as bots, or, as indicated on the website, 10% of accounts with a bot score above 4.8/5 are labeled as humans. In other words, if you use a threshold of 0.96 on the raw bot score (or 4.8 on the display score) to classify accounts as human/bot, you would wrongly classify 10% of accounts as bots -- a false positive rate of 10%.

# Intall the following packages:
#pip install tweepy
#pip install botometer
#pip install pandas

import tweepy
from tweepy.error import TweepError
import botometer
import pandas as pd

df = pd.read_csv("your data") # replace your dataset name; the data contains a list of user names 

rapidapi_key = "your Rapid API key" # get your rapid API from this site: https://rapidapi.com
twitter_app_auth = {
    'consumer_key': 'your consumer key',
    'consumer_secret': 'your consumer secret ',
    'access_token': 'your access token',
    'access_token_secret': 'your access token secret',
  }

bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

# Test: Check a single account by screen name
result1 = bom.check_account('_mgmpt')
print(result1['display_scores']['english']["overall"]) # get the display bot score for this user

# Get a bot score for each user in your dataset

# create a list to store bot scores
score = []
for index, row in df.iterrows():
    try: # if a user has a valid bot score 
        all_result = bom.check_account(row["x"])
        result = all_result['display_scores']['english']["overall"]
    except TweepError: # if a user does not have a valid bot score (e.g., some accounts were deleted before the scraping day; or some accounts are set to be private)
        result = "error" # assign "error" value to those who do not have a valid bot score
    score.append(result) # append values to the score list
    
    
df["score"] = score 
df.to_csv("") # save the dataframe
 
    
    
