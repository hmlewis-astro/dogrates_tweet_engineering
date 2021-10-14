# How To:
### Running the code in this repo

The code for this analysis is broken into multiple pieces to avoid re-running pieces that take a significant amount of time.

#### Deep learning model:
- `dog_breed_classification_model.ipynb` &mdash; [this notebook](https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/dog_breed_classification_model.ipynb) contains the code that produced the final trained dog breed classification model; the trained weights and model architecture are stored in the `trained_model/dog_breed_classifier.h5` file, the training history is saved in the `trained_model/dog_breed_classifier_epoch_history.csv` file for reference, and some sample predictions from the test data set are in the `/figures` directory (`predicted_dog_breed_*.png`)

#### Data collection, processing, and storage
- `twitter_api.py` &mdash; [this script](https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/twitter_api.py) utilizes the Twitter API and tweepy to retrieve the most recent Tweets from the given account; new Tweets (i.e., those not already in the existing database) are added to a `.json` file and the favorite/retweet counts for for Tweets already existing in the database are updated
- `create_mongo_db.py` &mdash; [this script](https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/create_mongo_db.py) reads the created/updated `.json` file and updates the `tweets` and `media` collections in the `dog_rates_images` MongoDB database
- `final_model_predictions.py` &mdash; breed prediction are made (from the dog breed classification model) for all images and video thumbnails in the `media` collection of the `dog_rates_images` MongoDB database in [this script](https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/final_model_predictions.py)

#### Automated processes
- `dogrates_pipeline.sh` &mdash; [this shell script](https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/dogrates_pipeline.sh) runs each of the scripts required for data collection, processing, and storage automatically, and then runs `mongoimport` to serve the updated `tweets` and `media` collections to a cloud database on MongoDB Atlas; this cloud database is accessible by the deployed Streamlit app

#### Streamlit webapp
- The source code for the deployed webapp is available [here](https://github.com/hmlewis-astro/dogrates_tweet_app).
