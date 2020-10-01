"""Flask Login Example and instagram fallowing find"""

from flask import Flask, url_for, render_template, request, redirect, session, escape,render_template_string
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = 'any random string'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kullanicilar.db'
db = SQLAlchemy(app)


class Kullanici(db.Model):
	""" Create user table"""
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(80), unique=True)
	sifre = db.Column(db.String(80))

	def __init__(self, email, sifre):
		self.email = email
		self.sifre = sifre


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
		mail = request.form['email']
		parola = request.form['sifre']
		data = Kullanici.query.filter_by(email=mail, sifre=parola).first()
		if data is not None:
			if Kullanici.query.filter(mail == 'admin@example.com').first():
				if Kullanici.query.filter(parola != 'admin').first():
					return render_template_string("hatalı giriş")
				else:
					return redirect(url_for('admin'))
					
			else:
				session['giris_yap'] = True
				return redirect(url_for('index'))
		else:
			return  render_template('index.html')
    
@app.route('/kayit', methods=['GET', 'POST'])
def kayit():
	"""Register Form"""
	if request.method == 'POST':
		mail = request.form['email']
		parola = request.form['sifre']
		yeni_kullanici = Kullanici(email=mail, sifre=parola)
		db.session.add(yeni_kullanici)
		db.session.commit()
		if yeni_kullanici is not None:
			mesaj="kayıt başarıyla sağlanmıştır."
			return render_template('index.html',mesaj=mesaj)
		
	return render_template('kayit.html')
@app.route("/cıkıs")
def cıkıs():
	session['giris_yap'] = False
	return redirect(url_for('index'))

@app.route("/admin")
def admin():
	return render_template_string("hy")



if __name__ == '__main__':
	
	db.create_all()
	app.run(debug=True)