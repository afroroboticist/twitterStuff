""" Main App/routing file for Twitoff """
from flask import Flask, render_template
from .models import DB, User, Tweet
from .get_tweets import api, update_all_users, insert_sample, add_or_update_user


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

	@app.route("/insert")
	def insert():
		insert_sample()
		print('Completed inserting.... Now updating')
		
		return render_template('base.html', title='Users Inserted', users=User.query.all())

	@app.route("/update")
	def update():
		update_all_users()
		print('Now updating...........')
		return render_template('base.html', title='Users Updated', users=User.query.all())


	return app




