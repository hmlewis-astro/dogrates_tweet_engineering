#!/bin/bash

# In your .bashrc file, create an environment variable "MONGODB_ATLAS_CLUSTER" with the Atlas connection string
# Atlas connection string example: "mongodb+srv://<username>:<password>@<cluster>.mh4jb.mongodb.net/<database>?retryWrites=true&w=majority"
source ~/.bashrc

# Replace ~/anaconda/ with the path to your miniconda/anaconda installation.
# Find the path of your install by running: conda info | grep -i 'base environment'
source ~/anaconda/etc/profile.d/conda.sh
conda activate metis

echo "Getting new Tweets..."
python twitter_api.py

/usr/local/bin/mongod --dbpath ~/data/db --quiet

echo "Updating MongoDB..."
python create_mongo_db.py

echo "Getting model predictions..."
python final_model_predictions.py

echo "Sending new Tweets to Atlas database to be served to Heroku..."
/usr/local/bin/mongoimport --uri $MONGODB_ATLAS_CLUSTER --collection tweets --drop --type json --jsonArray --file dog_rates_tweets.json
/usr/local/bin/mongoimport --uri $MONGODB_ATLAS_CLUSTER --collection media --drop --type json --jsonArray --file dog_rates_tweets_media.json

echo "Done!"
