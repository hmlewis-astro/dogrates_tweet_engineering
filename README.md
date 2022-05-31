# The Underdogs: a Heroku web app highlighting underappreciated dogs tweeted by WeRateDogs


## Abstract

The goal of this project was to deploy a web app to show some of the least-favorited dogs tweeted by the popular WeRateDogs Twitter account, with the ultimate goal of highlighting fundraising efforts that may have been underfunded when originally posted. I utilized the Twitter API to obtain Tweets from this account, and stored the resulting documents in a cloud database via MongoDB Atlas. I also built a deep learning neural network to classify dog breeds, and applied the model to identify the breed of dog featured in each Tweet. Web app users can choose a specific breed of dog and view Tweets including that breed. These data collection, cleaning, and storage processes have been fully automated (via a cron job), so the database accessed by the active web app is up to date with the most recent WeRateDogs Tweets (within 24 hours or less).


## Design

Though the popular Twitter account WeRateDogs ([@dog_rates](https://twitter.com/dog_rates)) is primarily a light-hearted source for adorable dog pics, with witty captions and ratings, the account also frequently posts fundraisers for dogs, dog shelters, and rescues in need. Most of these fundraisers&mdash;particularly those for individual dogs&mdash;meet their goals within minutes of being shared by the account; however, some of the larger fundraising efforts get lost in the social media shuffle, and the dogs included in them don't get as much love from the Twitter-verse as others.

In this project, I have deployed a web app that highlights Tweets with some of the least loved (i.e., fewest favorites) dogs posted by the WeRateDogs Twitter account&mdash;**The Underdogs**. By increasing the visibility of these particular dogs and associated fundraising efforts, I hope to ensure that all future fundraisers reach their goal. These dogs are highlighted on an [active web app](https://the-underdogs-app.herokuapp.com/).

I have also implemented a deep learning neural network to identify the breed of the dog in each post, allowing web app users to view Tweets including dogs of a breed of their choosing.

## Data

Tweet text, and associated media, hashtags, urls, favorite/retweet counts, etc. from the WeRateDogs Twitter account were obtained using the Twitter API. The Tweet documents were added to collection within a MongoDB database, and the urls pointing to the images and video thumbnails from each Tweet were added to a second collection.

At the time of this publication, the data are composed of ~600 total rating Tweets (i.e., Tweets containing ratings, out of 10 for the featured dog) out of the 3,200 pulled from this account, spanning December 2019 through mid-October 2021. However, the script used to obtain these Tweets has been fully automated to check for new Tweets daily, such that the available Tweets in the dataset will continue to grow. Each Tweet has 1-4 associated images/video thumbnails (average of 2 images per Tweet), and the collection contains ~1,300 images total.

These documents all have varying schema, because each Tweet has a different number of included images, different included entities (hashtags, emojis, etc.). The database has been well-tested and new Tweet data can easily be added with an automated process.


## Algorithms

The data are cleaned, explored, and processed using basic MongoDB queries. Only those Tweets containing "ratings", i.e., out of 10, along with an image and/or video of a featured dog are removed from the database. MongoDB queries are also used to identify Tweets with in the bottom 10% of favorite counts; these Tweets are displayed on the web app (described below).

Further, I built, trained, and tested a deep learning convolutional neural network to identify the breed of dog in each available image. The model uses transfer learning by assuming a MobileNetV2 architecture with the pre-trained ImageNet weights as a base model, followed by a batch normalization layer, a max pooling layer, a dense layer (with the ReLU activation function), a dropout layer, and, finally, an output layer with 120 neurons (with the softmax activation function). The model is trained on the  [Stanford Dogs dataset](https://www.tensorflow.org/datasets/catalog/stanford_dogs), which is composed of more than 20,000 total images containing 120 different dog breeds;
note, the number of neurons in the output layer is determined by the number of breeds in the dataset. The final model attains a precision of 0.8544 and a top _k_ categorical accuracy (_k_ = 3) of 0.9021.

Below are a sample of the predictions from this model for unseen images (i.e., those tweeted by WeRateDogs). The model performs very well for images that have little or no material obscuring the dog's face/body; however, the model does not perform well when a majority of the dog's face/body are covered. The model also

<p float="left" align="center">
  <img src="https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/figures/american_staffordshire_terrier_example_pred.jpeg" height="300" />
  <img src="https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/figures/eskimo_dog_example_pred.jpeg" height="300" />
  <br>
  <b>(Left) predicted breed:</b> American Staffordshire Terrier; <b>(right) predicted breed:</b> Eskimo Dog
</p>

<p float="left" align="center">
  <img src="https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/figures/bernese_mountain_dog_example_pred.jpeg" height="300" />
  <img src="https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/figures/italian_greyhound_example_pred.jpeg" height="300" />
  <br>
  <b>(Left) predicted breed:</b> Bernese Mountain Dog; <b>(right) predicted breed:</b> Italian Greyhound
</p>

MongoDB queries are also used to get a sample of Tweets containing a specific breed in the web app.


### Web Application

The resulting database and deep learning model are deployed in a web app on Heroku. The app shows a sample of 3 Tweets that are among the bottom 10% of favorite counts received by Tweets on this account. The app also allows the user to select a dog breed and displays a sample of up to 3 Tweets containing dogs of the selected breed, where the breed in each Tweet is predicted by the deep learning classification model described above. Finally, the web app provides a working contact form for bug reports, comments, questions, etc.

The web app is currently active, and available at the link below:

<a href='https://the-underdogs-app.herokuapp.com/'>The Underdogs</a>

The code for the web app is available [here](https://github.com/hmlewis-astro/dogrates_tweet_app).


## Tools
- Twitter API and `tweepy` for data collection
- MongoDB for local database storage, MongoDB Atlas for cloud database storage
- Tensorflow and Keras for building, tuning, training, and testing the deep learning model
- Google Colab (with GPU) for computing
- Streamlit for app development
- Twitter Publish oEmbed API for generating Tweet embedding HTML
- FormSubmit API and email service for HTML form
- Heroku for app deployment
