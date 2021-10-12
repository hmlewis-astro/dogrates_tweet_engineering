# Minimum Viable Product
## Highlighting Overlooked Dogs on WeRateDogs Twitter


The goal of this project is to deploy a web app that highlights Tweets with some of the least loved (i.e., least favorited) dogs posted by the WeRateDogs ([@dog_rates](https://twitter.com/dog_rates)) Twitter account, and to show Tweets including pictures/videos containing dogs of a user-specific breed.

To do this, I have used the Twitter API to get the ~3,000 most recent Tweets from this account, and have extracted Tweets containing ratings-based content (e.g., not Tweets in response to other users, Tweets about merchandise, etc.). This brings the number of Tweets in the current collection down to ~600, each with 1-4 associated images (2 images on average, ~1,300 images total). These data are stored in a MongoDB database, with collections containing:
- `tweets` &mdash; documents with the Tweet text (including the rating), links to the included media (i.e., photos/videos), included external urls, and the number of favorites for each Tweet, and
- `media` &mdash; documents with the image url(s) included in each Tweet.

Note, these documents all have varying schema, because each Tweet has a different number of included photos/videos, and different included entities (hashtags, emojis, etc.).

For each image in the `media` collection, we use a deep learning convolutional neural net (CNN) to predict the breed of the dog in the image. This CNN uses the MobileNetV2 architecture and pre-trained ImageNet weights as the base model, and is followed by a batch normalization layer, a max pooling layer, a dense layer (with the ReLU activation function), a dropout layer, and, finally, an output layer with 120 neurons (with the softmax activation function). The number of neurons in the output layer is determined by the number of breeds in the [Stanford Dogs dataset](https://www.tensorflow.org/datasets/catalog/stanford_dogs), the dataset used for training this model. The final model attains a precision of 0.8544 and a top_k_categorical_accuracy (_k_ = 3) of 0.9021.


Below are a sample of the predicted dog breeds from this model. The model performs well for images that have some...:
<p float="left" align="center">
  <img src="https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/figures/american_staffordshire_terrier_example_pred.jpeg" width="400" />
  <br>
  <b>Predicted breed: American Staffordshire Terrier</b>
  <img src="https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/figures/eskimo_dog_example_pred.jpeg" width="400" />
  <br>
  <b>Predicted breed: Eskimo Dog</b>
  <img src="https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/figures/bernese_mountain_dog_example_pred.jpeg" width="400" />
  <br>
  <b>Predicted breed: Bernese Mountain Dog</b>
  <img src="https://github.com/hmlewis-astro/dogrates_tweet_engineering/blob/main/figures/italian_greyhound_example_pred.jpeg" width="400" />
  <br>
  <b>Predicted breed: Italian Greyhound</b>
</p>

The annotated images contain ~4.5% road and ~95.5% background pixels, so it will be important to score the model on F1 rather than accuracy, because high accuracy can be achieved by simply assuming that all pixels are background.

After converting the scoring metric to the F1 score, I will continue to improve the model score by:
1. moving to Google Colab to run on a GPU,
2. adding dropout to avoid over fitting,
3. trying the ELU/LeakyReLU activation functions,
4. trying different optimizers (e.g., `RMSprop`, `SGD`),
5. training for more epochs with early stopping and reduced learning rate on plateau.

Given sufficient time, I will apply this network to images of disaster zones collected before and after the onset of major crisis events.
