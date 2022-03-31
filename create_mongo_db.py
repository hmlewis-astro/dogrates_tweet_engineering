#!/usr/bin/env python
# coding: utf-8

import os
import json

from pymongo import MongoClient
import pymongo

client = MongoClient(os.environ['MONGODB_ATLAS_CLUSTER'])
################################################################################
# Get Tweets from given Twitter handle
handle = 'dog_rates'

# Get Tweets from file with given name
infile = handle + '.json'
################################################################################

################################################################################
# If exists, drop existing database
if f'{handle}_images' in client.list_database_names():
    client.drop_database(f'{handle}_images')

# Load from file with given name
existing_tweets = json.load(open(infile, 'r'))

# Create MongoDB with given Twitter handle
db = client[f'{handle}_images']

# Create 'tweets' collection
tweets = db.tweets

# Insert Tweets to collection
tweets.insert_many(existing_tweets);
################################################################################


# Get Tweets from 'tweet' collection to create new documents for new 'media'
# collection
tweet_media = []
for j,tweet in enumerate(tweets.find()):
    media_dict = {'tweet_id':tweet['id']}

    for i,med in enumerate(tweet['extended_entities']['media']):
        media_dict[f'media_{i}'] = {'url':med['media_url_https']}

    tweet_media.append(media_dict)


# Create 'media' collection
media = db.media

# Insert media to collection
media.insert_many(tweet_media);
