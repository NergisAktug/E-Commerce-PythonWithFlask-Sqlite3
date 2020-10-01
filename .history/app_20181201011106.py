import datetime
from flask import Flask, request, render_template
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
import sqlite3

class ConfigClass(object):
   
    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Users/Nergis/Desktop/e-ticaret/eticaret.db'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'xyz@gmail.com' # gmail adresinizi girin
    MAIL_PASSWORD = 'sifre' # gmail şifrenizi girin
    MAIL_DEFAULT_SENDER = '"MyApp" <xyz@gmail.com>'

    
    USER_ENABLE_EMAIL = True        # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication
    
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"
  
def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    db = SQLAlchemy(app)
    class Kullanıcı(db.Model,UserMixin):
        __tablename__='kullanıcılar'    
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

        email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
        email_confirmed_at = db.Column(db.DateTime())
        sifre = db.Column(db.String(255), nullable=False, server_default='')
        adi = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
        soyadi = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

        roller = db.relationship('Rol', secondary='kullanıcı_rolleri')

        class Rol(db.Model):
            __tablename__ = 'roller'
            id = db.Column(db.Integer(), primary_key=True)
            adi = db.Column(db.String(50), unique=True)
        class KullanıcıRolleri(db.Model):
            __tablename__ = 'kullanıcı_rolleri'
            id = db.Column(db.Integer(), primary_key=True)
            kullanıcı_id = db.Column(db.Integer(), db.ForeignKey('kullanıcılar.id', ondelete='CASCADE'))
            rol_id = db.Column(db.Integer(), db.ForeignKey('roller.id', ondelete='CASCADE'))

        kullanici_yonetimi = UserManager(app, db,Kullanıcı)

        db.create_all()
        if not Kullanıcı.query.filter(Kullanıcı.email == 'member@example.com').first():
            kullanici = Kullanıcı(
                email='member@example.com',
                email_confirmed_at=datetime.datetime.utcnow(),
                sifre=kullanici_yonetimi.hash_password('Password1'),
            )
            db.session.add(kullanici)
            db.session.commit()


        if not Kullanıcı.query.filter(Kullanıcı.email == 'admin@example.com').first():
            kullanici= Kullanıcı(
                email='admin@example.com',
                email_confirmed_at=datetime.datetime.utcnow(),
                sifre=kullanici_yonetimi.hash_password('Password1'),
            )
            kullanici.roller.append(Role(name='Admin'))
            kullanici.roller.append(Role(name='Agent'))
            db.session.add(kullanici)
            db.session.commit()











@app.route('/')
def home():
    return render_template('/index.html')

@app.route('/üye')
def uye():

    return render_template('/üye.html')














if __name__=='__main__':
    app.run(debug=True)