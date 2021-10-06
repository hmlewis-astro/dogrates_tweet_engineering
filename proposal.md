# Project Proposal
## TITLE GOES HERE

### Question & Background:
Though the popular Twitter account WeRateDogs ([@dog_rates](https://twitter.com/dog_rates)) is primarily a light-hearted source for adorable dog pics, with witty captions and ratings, the account also frequently posts fundraisers for dogs, dog shelters, and rescues in need. While most of these fundraisers meet their goals within minutes of being shared by the account, some of these dogs get lost in the shuffle and don't get as much love from the Twitter-verse as others.

In this project, I aim to **deploy a web app that highlights Tweets with some of the least loved (i.e., least favorited) dogs posted by the WeRateDogs Twitter account**. By increasing the visibility of these particular dogs, I hope to ensure that all future fundraisers reach their goal. Given sufficient time, I will also implement a deep learning model to identify the breed of the dogs in each post, and show Tweets including dogs of a specific breed in the web app.


### Data description:
Data will be scraped from the WeRateDogs (@dog_rates) Twitter account. I will create a NoSQL database including:
- a collection containing Tweet text (including the rating), links to the included media (i.e., photos/videos), and the number of favorites for each Tweet
- a collection containing the linked media (i.e., image files) for each Tweet

The data are (currently) composed of the ~3,000 most recent Tweets from this account (as of October 2021); however, because the deployed application will use the Twitter API to check for new Tweets each time it is used, the available Tweets in the dataset will continue to grow. For this particular account, I will use the Twitter API to extract only those Tweets containing ratings (e.g., not Tweets in response to other users, Tweets about merchandise, etc.). This brings the number of Tweets in the collection down to ~600, each with 1-4 associated images (2 images on average).


### Tools:
Data will be obtained using the Twitter API, along with `tweepy` in Python, and will be stored in a MongoDB database.

Given sufficient time, I will apply a deep convolutional neural network to the images to identify the breed of dog in each Tweet, and to show Tweets in the app including dogs of a user-selected breed. The neural network will be built, tested, and evaluated using the `tensorflow.keras` library in Python.

The web application will be launched as a Flask App on an online platform (e.g., Heroku).


### MVP:

The minimal viable product (MVP) for this project will be a well-tested (i.e., works with new data, handles errors) NoSQL database, and possibly a pretrained dog classification neural net applied to a subset of the new images included in that database.
