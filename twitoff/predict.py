""" Module that will predict the tweet of a user """
from .models import DB, User, Tweet
from sklearn.linear_model import LogisticRegression
from .get_tweets import vectorize_tweet
import numpy as np

def predict_user(user0_name, user1_name, tweet):
	""" Determine and return which user is more likely
		To tweet a string
	"""
	user0 = User.query.filter(User.name == user0_name).one()
	user1 = User.query.filter(User.name == user1_name).one()
	user1_vects = np.array([tweet.vect for tweet in user1.tweets])
	user0_vects = np.array([tweet.vect for tweet in user0.tweets])
	data_vects = np.vstack([user0_vects, user1_vects])
	labels = np.concatenate([np.zeros(len(user0.tweets)),
			 np.ones(len(user1.tweets))])

	log_reg = LogisticRegression()
	log_reg.fit(data_vects, labels)

	hypo_tweet_vect = vectorize_tweet(tweet)

	prediction = log_reg.predict(hypo_tweet_vect.reshape(1,-1))

	if prediction[0] == 0:
		return user0.name


	else:
		return user1.name


