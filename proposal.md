# Project Proposal
## TITLE GOES HERE

### Question & Background:
Though the WeRateDogs (@dog_rates)

In these cases, deep learning can play an important role. Specifically, a neural net trained to extract road maps from satellite images can be applied to images taken before and after a disaster to identify roads that have become inaccessible following a disaster.

In this project, I aim to **create a deep neural network to extract road maps from satellite images**. Given sufficient time, I will apply this neural network to images of disaster zones collected before and after the onset of major crisis events.


### Data description:
Data will be scraped from the WeRateDogs (@dog_rates) Twitter account.

These data are (currently) composed of the ~3,000 most recent Tweets from this account (as of October 2021); however, because the deployed application will use the Twitter API to check for new Tweets each time it is used, the available Tweets in the dataset will continue to grow. For this particular account, which rates people's dogs, we use the Twitter API to extract only those Tweets containing ratings (i.e., not Tweets in response to other users, Tweets about merchandise, etc.).

Given sufficient time, I will apply a dog breed identification neural network to the images included in these Tweets to recommend Tweets including ratings of dogs of a specific breed.


### Tools:
Data will be obtained using the Twitter API, along with tweepy in Python, and will be stored in a MongoDB database.

The web application will be launched as a Flask App on an online platform (e.g., Heroku).

### MVP:

The minimal viable product (MVP) for this project will

be a baseline neural network that incorporates transfer learning (i.e., pretrained on ImageNet). This baseline model will be scored&mdash;likely using F1, the typical metric for aerial image segmentation models&mdash;and future iterations of the model will aim to improve this score by adding/removing nodes or layers, using dropout, tuning the decision threshold, etc.
