#!/usr/bin/env python
# coding: utf-8

import os
import json
from tqdm import tqdm

from twitter_api_key import key

import tweepy

import pandas as pd

################################################################################
# Twitter API keys
consumer_key = key["consumer_key"]
consumer_secret = key["consumer_secret"]
access_token = key["access_token"]
access_token_secret = key["access_token_secret"]

# Access Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Get Tweets from given Twitter handle
handle = 'dog_rates'

# Write Tweets to file with given name
outfile = handle + '.json'
################################################################################


################################################################################
def retrieve_existing(outfile):
    existing_tweets = dict()
    if os.path.exists(outfile):
        with open(outfile) as out:
            existing_tweets = pd.read_json(out)

    return existing_tweets
################################################################################


# Define columns to drop from each json document
cols_to_drop = ['id_str', 'truncated', 'favorited', 'retweeted']

# Get API cursor
if os.path.exists(outfile):
    existing_tweets = retrieve_existing(outfile)
    try:
        existing_tweets.drop(cols_to_drop, axis=1, inplace=True)
        existing_tweets['created_at'] = pd.to_datetime(existing_tweets['created_at'])
    except:
        pass

    max_api_calls = 900

    cursor = tweepy.Cursor(api.user_timeline,
                           id=handle
                           ).items(max_api_calls)

else:
    existing_tweets = []
    max_api_calls = 3200

    cursor = tweepy.Cursor(api.user_timeline,
                           id=handle
                           ).items()


# Get most recent Tweets
new_tweets = []

#for tweet in tqdm(cursor, total=max_api_calls):
for tweet in cursor:
    status = api.get_status(tweet._json['id'], tweet_mode='extended')
    if ('media' in status._json['entities']) and ('/10' in status._json['full_text']):
        new_tweets.append(status._json)

new_tweets = pd.DataFrame(new_tweets)

# Drop columns from each json document
new_tweets.drop(cols_to_drop, axis=1, inplace=True)
new_tweets['created_at'] = pd.to_datetime(new_tweets['created_at'])

# Merge existing Tweets with new Tweets, and update favorite/retweet counts
for i,tweet in new_tweets.iterrows():
    if tweet['id'] in list(existing_tweets['id']):
        existing_tweets.loc[existing_tweets['id'] == tweet['id'], ['favorite_count']] = tweet['favorite_count']
        existing_tweets.loc[existing_tweets['id'] == tweet['id'], ['retweet_count']] = tweet['retweet_count']

    else:
        existing_tweets = existing_tweets.append(tweet, ignore_index=True)
        existing_tweets.sort_values('id', ascending=False, inplace=True)
        existing_tweets.reset_index(drop=True)

# Write all Tweets to file with given name
with open(outfile, 'w') as out:
    existing_tweets.to_json(out, date_format='iso', orient='records')
