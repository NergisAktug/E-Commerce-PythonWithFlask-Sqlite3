"""Flask Login Example and instagram fallowing find"""

from flask import Flask, url_for, render_template, request, redirect, session, escape
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = 'any random string'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kullanicilar.db'
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
	if not session.get('giris_yap'):
		return render_template('index.html')
	else:
		if request.method == 'POST':
			return render_template('index.html')
		return render_template('index.html')
    

@app.route('/üye')
def uye():
	return render_template('/üye.html')
@app.route('/giris', methods=['GET', 'POST'])
def giris():
	if request.method == 'GET':
		return render_template('kayit.html')
	else:
		name = request.form['username']
		passw = request.form['password']
		data = User.query.filter_by(username=name, password=passw).first()
		if data is not None:
			session['giris_yap'] = True
			return redirect(url_for('index'))
		else:
			return  render_template('index.html')
    
@app.route('/kayit', methods=['GET', 'POST'])
def kayit():
	"""Register Form"""
	if request.method == 'POST':
		new_user = User(username=request.form.get('username'), password=request.form.get('password'))
		db.session.add(new_user)
		db.session.commit()
		return render_template('üye.html')
	return render_template('kayit.html')
@app.route("/cıkıs")
def cıkıs():
	session['logged_in'] = False
	return redirect(url_for('index'))


if __name__ == '__main__':
	
	db.create_all()
	app.run(debug=True)