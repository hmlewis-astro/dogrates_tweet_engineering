# Minimum Viable Product
## Highlighting Overlooked Dogs on WeRateDogs Twitter


The goal of this project is to deploy a web app that highlights Tweets with some of the least loved (i.e., least favorited) dogs posted by the WeRateDogs ([@dog_rates](https://twitter.com/dog_rates)) Twitter account, and to show Tweets including pictures/videos containing dogs of a user-specific breed.

To do this, I have used the Twitter API to get the ~3,000 most recent Tweets from this account, and have extracted Tweets containing ratings-based content (e.g., not Tweets in response to other users, Tweets about merchandise, etc.). This brings the number of Tweets in the current collection down to ~600, each with 1-4 associated images (2 images on average, ~1,300 images total), though the database can be added to continuously. These data are stored in a MongoDB database, with collections containing:
- `tweets` &mdash; documents with the Tweet text (including the rating), links to the included media (i.e., photos/videos), included external urls, and the number of favorites for each Tweet, and
- `media` &mdash; documents with the image url(s) included in each Tweet.

Note, these documents all have varying schema, because each Tweet has a different number of included photos/videos, and different included entities (hashtags, emojis, etc.). The database has been well-tested and new Tweet data can easily be added.

For each image in the `media` collection, we use a deep learning convolutional neural net (CNN) to predict the breed of the dog in the image. This CNN uses the MobileNetV2 architecture and pre-trained ImageNet weights as the base model, and is followed by a batch normalization layer, a max pooling layer, a dense layer (with the ReLU activation function), a dropout layer, and, finally, an output layer with 120 neurons (with the softmax activation function). The number of neurons in the output layer is determined by the number of breeds in the [Stanford Dogs dataset](https://www.tensorflow.org/datasets/catalog/stanford_dogs), the dataset used for training this model. The final model attains a precision of 0.8544 and a top_k_categorical_accuracy (_k_ = 3) of 0.9021.


Below are a sample of the predictions from this model for images Tweeted by WeRateDogs:
<p float="left" align="center">
  <img src="https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/figures/american_staffordshire_terrier_example_pred.jpeg" width="256" /><br>
  <b>Predicted breed:</b> American Staffordshire Terrier
</p>

<p float="left" align="center">
  <img src="https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/figures/eskimo_dog_example_pred.jpeg" width="256" /><br>
  <b>Predicted breed:</b> Eskimo Dog
</p>

<p float="left" align="center">
  <img src="https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/figures/bernese_mountain_dog_example_pred.jpeg" width="256" /><br>
  <b>Predicted breed:</b> Bernese Mountain Dog
</p>

<p float="left" align="center">
  <img src="https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/figures/italian_greyhound_example_pred.jpeg" width="256" /><br>
  <b>Predicted breed:</b> Italian Greyhound
</p>

The model performs very well for images that have little or no material obscuring the dog's face/body (a single accessory, e.g., the tie in the first example); however, the model does not perform well when a majority of the dog's face/body are covered (a full costume, e.g., the jersey plus toy in the last example).

### Next steps:
I am currently working on writing a shell script to automate all of the processes outlined here (API, adding new data to the database, breed classification), though I would like to include these steps as part of my Streamlit app (i.e., steps run automatically each time the app is accessed).

I will then begin developing the Streamlit app itself, to show a specific subset of Tweets, based on user inputs.
