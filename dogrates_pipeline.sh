#!/bin/bash

# Replace ~/anaconda/ with the path to your miniconda/anaconda installation.
# You can find that out by running: conda info | grep -i 'base environment'
source ~/anaconda/etc/profile.d/conda.sh
conda activate metis

echo "Getting new Tweets..."
python twitter_api.py

mongod --dbpath ~/data/db --quiet

echo "Updating MongoDB..."
python create_mongo_db.py

echo "Getting model predictions..."
python final_model_predictions.py

echo "Sending new Tweets to Atlas database to be served to Heroku..."
mongoimport --uri "mongodb+srv://<username>:<password>@engineering-cluster.mh4jb.mongodb.net/dog_rates_images?retryWrites=true&w=majority" --collection tweets --drop --type json --jsonArray --file dog_rates_tweets.json
mongoimport --uri "mongodb+srv://<username>:<password>@engineering-cluster.mh4jb.mongodb.net/dog_rates_images?retryWrites=true&w=majority" --collection media --drop --type json --jsonArray --file dog_rates_tweets_media.json

echo "Done!"
