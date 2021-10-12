#!/usr/bin/env python
# coding: utf-8

import os
import glob
from tqdm import tqdm
import re
import requests
import csv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from io import BytesIO

import tensorflow as tf

from tensorflow.keras import models

import tensorflow_datasets as tfds

from pymongo import MongoClient

client = MongoClient()

################################################################################
# Get Tweets from given Twitter handle
handle = 'dog_rates'
################################################################################


################################################################################
# Get MongoDB
db = client[f'{handle}_images']

# Get 'tweets' and 'media' collections
tweets = db.tweets
tweets_media = db.media
################################################################################


################################################################################
def split_breed_name(name):
    name = name.split('-')[1].split('_')
    name = ' '.join(name)
    return name.title()

def breed_pred(dog, save_fig=False):

    dat, image = preprocess(dog)
    image_reshape = tf.expand_dims(image, 0)

    predict_breeds = trained_model(image_reshape)

    return predict_breeds
################################################################################


# Load data to get breed names
with open('breed_name.csv', 'r') as f:
    names = f.read().split('\n')

breed_name = tfds.features.ClassLabel(names=names).int2str

# Load trained model weights
print('Loading previously trained model.')
trained_model = models.load_model('trained_model/dog_breed_classifier.h5')

# Include image preprocessing steps
image_size = 224
image_shape = (image_size, image_size, 3)
num_breeds = 120

def preprocess(url):

    dat = tf.image.decode_jpeg(requests.get(url).content, channels=3, name="jpeg_reader")

    # convert images to floats, resize for ImageNet
    image = tf.image.convert_image_dtype(dat, dtype=tf.float64)
    image = tf.image.resize(image, (image_size, image_size), method='nearest')

    return dat, image


# If True, gets model predictions for all Tweeted media, even if predictions already exist
# If False, gets model predictions for only media without existing predictions
get_all_pred = False

# Get model predictions for Tweeted media
for tweet in tqdm(tweets.find(), total=tweets.estimated_document_count()):

    # Do not get model predictions if predictions already exist
    if not get_all_pred:
        if 'predicted_breed' in tweet.keys():
            continue

    med =  tweets_media.find({'tweet_id':tweet['id']}, )
    med = list(med)[0]
    predicted_breeds = []
    for key in med.keys():
        if re.search('media', key):
            med_url = med[key]['url']
            med_top_breeds = breed_pred(med_url)
            predicted_breeds.append(med_top_breeds.numpy())

            med_top_components = tf.reshape(tf.math.top_k(med_top_breeds, k=3).indices,shape=[-1])
            med_top_breeds = [breed_name(i) for i in med_top_components]
            med_top_breeds = list(map(split_breed_name, med_top_breeds))
            tweets_media.update_one({'tweet_id':tweet['id']}, {"$set": {"predicted_breed": med_top_breeds}})

    predicted_breeds = sum(predicted_breeds)

    top_components = tf.reshape(tf.math.top_k(predicted_breeds, k=3).indices,shape=[-1])
    top_breeds = [breed_name(i) for i in top_components]
    top_breeds = list(map(split_breed_name, top_breeds))
    tweets.update_one({'id': tweet['id']}, {"$set": {"predicted_breed": top_breeds}})
