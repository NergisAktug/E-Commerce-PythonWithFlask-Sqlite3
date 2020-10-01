import datetime
from flask import Flask, request, render_template
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
import sqlite3

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Nergis/Desktop/e-ticaret/eticaret.db'
db=SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('/index.html')

@app.route('/üye')
def uye():

    return render_template('/üye.html')


class Kullanıcı(db.Model,UserMixin):
    __tablename__='kullanıcılar'    
    id=db.Column(db.Integer,primary_key=True)
    active=db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

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

    kullanici_yonetimi = UserManager(app, db,Kullanıcı User)

    db.create_all()











if __name__=='__main__':
    app.run(debug=True)