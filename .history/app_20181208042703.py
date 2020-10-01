from db import datetime
from flask import Flask, request, render_template_string, render_template
from flask import Flask, url_for, render_template, request, redirect, session, escape, render_template_string
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required
from sqlalchemy.sql import table, column, select
from sqlalchemy import MetaData, create_engine
from flask_user import login_required, roles_required, UserManager, UserMixin


class ConfigClass(object):
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///eticaret.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'nergis.aktug2014@gmail.com'
    MAIL_PASSWORD = '05383896877'
    MAIL_DEFAULT_SENDER = '"MyApp" <xyz@gmail.com>'

    USER_ENABLE_EMAIL = True
    USER_ENABLE_USERNAME = False
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"


def create_app():
    """ Flask application factory """

    # Create Flask app load app.config
    app = Flask(__name__)
    app.config.from_object(__name__ + '.ConfigClass')

    db = SQLAlchemy(app)

    class Kullanici(db.Model):
		tarih = db.Column(db.DateTime())
    	__tablename__ = 'Kullanici'
    	id = db.Column(db.Integer, primary_key=True)
		
    	email = db.Column(db.String(80), unique=True)
    	sifre = db.Column(db.String(80))
    	rolId = db.Column(db.Integer, db.ForeignKey('rol.rolId', ondelete='CASCADE'))
    	active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
		

    	def __init__(self, email, sifre):
            self.email = email
            self.sifre = sifre
            self.rolId = 0

    class Roller(db.Model):
        __tablename__ = 'rol'
        rolId = db.Column(db.Integer, primary_key=True)
        rolisim = db.Column(db.String(80))

    class urunler(db.Model):
        __tablename__ = 'urunler'
        urun_id = db.Column(db.Integer, primary_key=True)
        kategori_id = db.Column(db.Integer(), db.ForeignKey('kategori.kategoriId', ondelete='CASCADE'))
        urunresmi = db.Column(db.String(80))
        urunFiyati = db.Column(db.Integer)
        markaId = db.Column(db.Integer(), db.ForeignKey('markalar.markaId', ondelete='CASCADE'))

        def __init__(self, kategori_id, urun_ozellikleri, urun_fiyati):
            self.kategori_id = kategori_id
            self.urun_ozellikleri = urun_ozellikleri
            self.urun_fiyati = urun_fiyati

    class kategori(db.Model):
        __tablename__ = 'kategori'
        kategoriId = db.Column(db.Integer, primary_key=True)
        kategori_adi = db.Column(db.String(80))

        def __init__(self, kategori_adi):
            self.kategori_adi = kategori_adi

    class markalar(db.Model):
        __tablename__ = 'markalar'
        markaId = db.Column(db.Integer, primary_key=True)
        markaadi = db.Column(db.String(80))
        marka_modeli = db.Column(db.String(80))

        def __init__(self, markaadi, marka_modeli):
            self.markaadi = markaadi
            self.marka_modeli = marka_modeli

    class musteri(db.Model):
        __tablename__ = 'musteri'
        musteriId = db.Column(db.Integer, primary_key=True)
        musteriadi = db.Column(db.String(80))
        musterisoyadi = db.Column(db.String(80))
        mail = db.Column(db.String(80), unique=True)
        telefon = db.Column(db.Integer)
        sifre = db.Column(db.String(80))
        il = db.Column(db.String(80))
        ilce = db.Column(db.String(80))
        kullaniciId = db.Column(db.Integer(), db.ForeignKey('Kullanici.id', ondelete='CASCADE'))

        def __init__(self, musteriadi, musterisoyadi, mail, telefon, sifre, il, ilce, kullaniciId):
            self.musteriadi = musteriadi
            self.musterisoyadi = musterisoyadi
            self.mail = mail
            self.telefon = telefon
            self.sifre = sifre
            self.il = il
            self.ilce = ilce
            self.kullaniciId = kullaniciId

    class siparis(db.Model):
        __tablename__ = 'siparis'
        siparisId = db.Column(db.Integer, primary_key=True)
        musteriId = db.Column(db.Integer(), db.ForeignKey('musteri.musteriId', ondelete='CASCADE'))
        urunId = db.Column(db.Integer(), db.ForeignKey('urunler.urun_id', ondelete='CASCADE'))
        siparisno = db.Column(db.Integer)
        siparisTarihi = db.Column(db.Integer)
        odemeId = db.Column(db.Integer())

        def __init__(self, musteriId, urunId, siparisno, siparisTarihi, odemeId):
            self.musteriId = musteriId
            self.urunId = urunId
            self.siparisno = siparisno
            self.siparisTarihi = siparisTarihi
            self.odemeId = odemeId

    user_manager = UserManager(app, db, Kullanici)
    db.create_all()

	if not Kullanici.query.filter(Kullanici.email == request.form['email']).first():
        kullanici = Kullanici(
            email=request.form['email'],
            tarih=datetime.datetime.utcnow(),
            sifre=user_manager.hash_password(request.form['sifre']),
        )
        

    # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
    if not Kullanici.query.filter(Kullanici.email == 'admin@example.com').first():
        kullanici = Kullanici(
            email='admin@example.com',
            tarih=datetime.datetime.utcnow(),
            sifre=user_manager.hash_password('admin'),
        )

    @app.route('/')
    def anasayfa():
        return render_template('index.html')

    @app.route('/kayit', methods=['GET', 'POST'])
    def kayit():
        if request.method == 'POST':
            mail = request.form['email']
            parola = request.form['sifre']
            yeniKullanici = Kullanici(email=mail, sifre=parola)
            db.session.add(yeniKullanici)
            db.session.commit()
            if yeniKullanici is not None:
                mesaj = "Kayıt Başarıyla Sağlanmıştır."
                return render_template("index.html", mesaj=mesaj)
        else:
            return render_template('kayit.html')

    @app.route('/uye', methods=['GET', 'POST'])
    def uye():
        return render_template("uyeGirisi.html")

    @app.route('/giris', methods=['GET', 'POST'])
    def giris():
		session['giris_yap']=False
		if request.method=='GET':
			if(session['giris_yap']==True):
				return redirect(url_for('index'))
			else:
				return render_template('uyeGirisi.html')
        else:
			email=request.form['email']
			parola=request.form['sifre']
			active=0
			try:
				if Kullanici.query.filter_by(email=email,sifre=parola,active=1).first():
						
						session['giris_yap']=True
					kullanici.rol.append(Role(rolisim='Admin'))
					db.session.add(kullanici)
       				db.session.commit()

    @app.route('/admin')
    @roles_required('admin')
    def admin():
        return "naber selin ya"

    return app


if __name__ == '__main__':
    app = create_app()
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='127.0.0.1', port=5000, debug=True)