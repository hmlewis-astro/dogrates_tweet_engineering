#!/bin/bash

# Replace ~/anaconda/ with the path to your miniconda/anaconda installation.
# You can find that out by running: conda info | grep -i 'base environment'
source ~/anaconda/etc/profile.d/conda.sh
conda activate metis

echo "Getting new Tweets..."
python twitter_api.py

mongod --dbpath ~/data/db

echo "Updating MongoDB..."
python create_mongo_db.py

echo "Getting model predictions..."
python final_model_prediction.py

echo "Done!"
