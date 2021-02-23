from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
	""" Twitter Users that correspond to tweets """
	id = DB.Column(DB.BigInteger, primary_key=True)
	name = DB.Column(DB.String, nullable=False)
	newest_tweet_id = DB.Column(DB.BigInteger)

	def __repr__(self):
		return "<User: {}>".format(self.name)


# Tweet Table Using SQLAlchemy syntax
class Tweet(DB.Model):
    """Twitter Tweets that corresspond to users"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    vect = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        "user.id"), nullable=False)
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)

# def insert_example_users():
	
# 	bobby = User(id=1, name="Bobby")
# 	elon = User(id=2, name="Elon")
# 	nick = User(id=3, name="Nick")
# 	steph = User(id=4, name="Steph")
# 	laurence = User(id=5, name="Laurence")
# 	DB.session.add(elon)
# 	DB.session.add(bobby)
# 	DB.session.add(elon)
# 	DB.session.add(nick)
# 	DB.session.add(steph)
# 	DB.session.add(laurence)
# 	DB.session.commit()

