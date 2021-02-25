""" Main App/routing file for Twitoff """
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .get_tweets import api, update_all_users,\
						insert_sample, add_or_update_user
from .predict import predict_user


def create_app():
	"""Create Flask Application"""
	app = Flask(__name__)

	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_1.sqlite3"
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	DB.init_app(app)



	@app.route("/")
	def root():
		users = User.query.all()
		""" At end point '/'"""
		return render_template('base.html', title='home', users=users)


	@app.route("/reset")
	def reset():
		"""reset DB using drop_all()"""
		DB.drop_all()
		DB.create_all()
		return render_template('base.html', title='RESET', users=User.query.all())

	@app.route("/compare", methods=["POST"])
	def compare():
		user0, user1 = sorted([request.values["user0"],
							  request.values["user1"]])
		if user0 == user1:
			message = "Cannot compare users to themselves!"

		else:
			prediction = predict_user(
				user0, user1, request.values["tweet_text"])
			message = '"{}" is more likely to be said by {}'.format(
				request.values["tweet_text"], prediction)

		return render_template("prediction.html", title="Prediction", message=message)


	@app.route("/insert")
	def insert():
		insert_sample()
		print('Completed inserting.... Now updating')
		
		return render_template('base.html', title='Users Inserted', users=User.query.all())

	@app.route("/user", methods=["POST"])
	@app.route("/user/<name>", methods=["GET"])
	def user(name=None, message=""):
		name = name or request.values["user_name"]
		try:
			if request.method == "POST":
				add_or_update_user(name)
				message = "User {} successfully added!".format(name)

			tweets = User.query.filter(User.name == name).one().tweets

		except Exception as e:
			message = "Error adding {} : {}".format(name, e)
			tweets = []

		return render_template('user.html', title=name, tweets=tweets, message=message)

	@app.route("/update")
	def update():
		update_all_users()
		print('Now updating...........')
		return render_template('base.html', title='Users Updated', users=User.query.all())


	return app




