import datetime
from flask import Flask, request, render_template_string,render_template
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required
from sqlalchemy.sql import table,column,select
from sqlalchemy import MetaData,create_engine

class ConfigClass(object):
    """ Flask application config """
   
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
    
    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///basic_app.sqlite'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-Mail SMTP server settings 
    # #USER_ENABLE_EMAIL=True ise bu ayarları yapın. Google güvenlik ayarları bu işlemi yapmanıza izin vermeyebilir.
    #Detaylı bilgiyi https://support.google.com/accounts/answer/6010255?p=lsa_blocked&hl=en-GB&visit_id=636759033269131098-410976990&rd=1 dan edinebilirsiniz. 
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'email@example.com' # gmail adresinizi girin
    MAIL_PASSWORD = 'password' # gmail şifrenizi girin
    MAIL_DEFAULT_SENDER = '"MyApp" <xyz@gmail.com>'

    # Flask-User settings
    USER_APP_NAME = "Bahar'ın Web Sitesi"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True        # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"
   # Daha detaylı bilgi https://flask-user.readthedocs.io/en/latest/configuring_settings.html de bulunabilir.
def create_app():
    """ Flask application factory """
    
    # Create Flask app load app.config
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass') 
   
		db = SQLAlchemy(app)

	class Kullanici(db.Model):
	__tablename__ = 'Kullanici'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(80), unique=True)
	sifre = db.Column(db.String(80))
	rolId=db.Column(db.Integer,db.ForeignKey('rol.rolId', ondelete='CASCADE'))

	def __init__(self, email, sifre,rolId):
		self.email = email
		self.sifre = sifre
		self.rolId=rolId


	class Roller(db.Model):
		__tablename__='rol'
		rolId=db.Column(db.Integer, primary_key=True)
		rolIsım=db.Column(db.String(80))

	class urunler(db.Model):
		__tablename__ = 'urunler'
		urun_id=db.Column(db.Integer,primary_key=True)
		kategori_id=db.Column(db.Integer(), db.ForeignKey('kategori.kategoriId', ondelete='CASCADE'))
		urunresmi=db.Column(db.String(80))
		urunFiyati=db.Column(db.Integer)
		markaId=db.Column(db.Integer(), db.ForeignKey('markalar.markaId', ondelete='CASCADE'))
		def __init__(self, kategori_id, urun_ozellikleri,urun_fiyati):
			self.kategori_id=kategori_id
			self.urun_ozellikleri= urun_ozellikleri
			self.urun_fiyati=urun_fiyati

	class kategori(db.Model):
		__tablename__ = 'kategori'
		kategoriId=db.Column(db.Integer,primary_key=True)
		kategori_adi=db.Column(db.String(80))
		def __init__(self, kategori_adi):
			self.kategori_adi=kategori_adi

	class markalar(db.Model):
		__tablename__ = 'markalar'
		markaId=db.Column(db.Integer,primary_key=True)
		markaadi=db.Column(db.String(80))
		marka_modeli=db.Column(db.String(80))
		def __init__(self, markaadi,marka_modeli):
			self.markaadi=markaadi
			self.marka_modeli=marka_modeli
	class musteri(db.Model):
		__tablename__ = 'musteri'
		musteriId=db.Column(db.Integer,primary_key=True)
		musteriadi=db.Column(db.String(80))
		musterisoyadi=db.Column(db.String(80))
		mail=db.Column(db.String(80), unique=True)
		telefon=db.Column(db.Integer)
		sifre=db.Column(db.String(80))
		il=db.Column(db.String(80))
		ilce=db.Column(db.String(80))
		kullaniciId=db.Column(db.Integer(), db.ForeignKey('Kullanici.id', ondelete='CASCADE'))
		def __init__(self, musteriadi,musterisoyadi,mail,telefon,sifre,il,ilce,kullaniciId):
			self.musteriadi=musteriadi
			self.musterisoyadi=musterisoyadi
			self.mail=mail
			self.telefon=telefon
			self.sifre=sifre
			self.il=il
			self.ilce=ilce
			self.kullaniciId=kullaniciId
	class siparis(db.Model):
		__tablename__ = 'siparis'
		siparisId=db.Column(db.Integer,primary_key=True)
		musteriId=db.Column(db.Integer(), db.ForeignKey('musteri.musteriId', ondelete='CASCADE'))
		urunId=db.Column(db.Integer(), db.ForeignKey('urunler.urun_id', ondelete='CASCADE'))
		siparisno=db.Column(db.Integer)
		siparisTarihi=db.Column(db.Integer)
		odemeId=db.Column(db.Integer(), db.ForeignKey('odeme.id', ondelete='CASCADE'))
		def __init__(self,musteriId,urunId,siparisno,siparisTarihi,odemeId):
			self.musteriId=musteriId
			self.urunId=urunId
			self.siparisno=siparisno
			self.siparisTarihi=siparisTarihi
			self.odemeId=odemeId
	class sepet(db.Model):
		__tablename__ = 'sepet'
		sepetId=db.Column(db.Integer,primary_key=True)
		urunId=db.Column(db.Integer(), db.ForeignKey('urun.id', ondelete='CASCADE'))
		def __init__(self,urunId):
			self.urunId=urunId
if __name__ == '__main__':
    app = create_app()
   # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='127.0.0.1', port=5000, debug=True)