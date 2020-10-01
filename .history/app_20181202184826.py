"""Flask Login Example and instagram fallowing find"""

from flask import Flask, url_for, render_template, request, redirect, session, escape
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = 'any random string'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
	""" Create user table"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))

	def __init__(self, username, password):
		self.username = username
		self.password = password


@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/üye')
def uye():

    return render_template('/üye.html')





if __name__ == '__main__':
	
	db.create_all()
	app.run(debug=True)