import tweepy
import os
import spacy
from .models import DB, Tweet, User
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_key = os.getenv('ACCESS_KEY')
access_secret = os.getenv('ACCESS_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

nlp = spacy.load("my_model/")


def vectorize_tweet(tweet_text):
	return nlp(tweet_text).vector


def add_or_update_user(username):
	try:
		"""Takes username and pulls user from Twitter API"""
		twitter_user = api.get_user(username)
		db_user = (User.query.get(twitter_user.id)) or User(
			id=twitter_user.id, name=username)
		print('User ID retrieved')
		DB.session.add(db_user)
		print('User added to data Base')
		tweets = twitter_user.timeline(
	        count=200, exclude_replies=True, include_rts=False,
	        tweet_mode="extended", since_id=db_user.newest_tweet_id
	    )
		print('Tweets created')

		if tweets:
			db_user.newest_tweet_id = tweets[0].id
		

		for tweet in tweets:
			tweet_embeddings = vectorize_tweet(tweet.full_text)
			print('Tweet Embeddings Done....')
			db_tweet = Tweet(
				id=tweet.id, text=tweet.full_text[:300], vect=tweet_embeddings)
			print('Embeddings added as VECT to db_Tweet')
			db_user.tweets.append(db_tweet)
			print('Tweets appended')
			DB.session.add(db_tweet)
			print('DB_Tweet added')

	except tweepy.error.TweepError as e:
		print("Error encountered {}>{}".format(username, e))
		raise e

	else:
		DB.session.commit()
		print('Session committed')



####################################################
# Not calling this function yet. It throws an error#
####################################################


# def add_or_update_user(username):
#     """Takes username and pulls user from Twitter API"""
#     try:
#         twitter_user = api.get_user(username)
#         db_user = (User.query.get(twitter_user.id)) or User(
#             id=twitter_user.id, name=username)
#         DB.session.add(db_user)

#         # What does since ID do?
#         tweets = twitter_user.timeline(
#             count=200, exclude_replies=True, include_rts=False,
#             tweet_mode="extended", since_id=db_user.newest_tweet_id
#         )

#         if tweets:
#             db_user.newest_tweet_id = tweets[0].id

#         for tweet in tweets:
#             tweet_embeddings = vectorize_tweet(tweet.full_text)
#             db_tweet = Tweet(
#                 id=tweet.id, text=tweet.full_text[:300], vect=tweet_embeddings)
#             db_user.tweets.append(db_tweet)
#             DB.session.add(db_tweet)

#     except Exception as e:
#         print("Error Processing {}: {}".format(username, e))
#         raise e

#     else:
#         DB.session.commit()

def update_all_users():
	
	users = User.query.all()
	for user in users:
		add_or_update_user(user.name)
	

def insert_sample():
	add_or_update_user('afroroboticist')
	print('inserted afroroboticist')
	add_or_update_user('jnhdny')
	print('inserted jnhdny')
	add_or_update_user('AOC')
	print('inserted AOC')



# for tweet in tweets:
# 	print(tweet.text)

# user = 'afroroboticist'

# users = api.get_user(user)
