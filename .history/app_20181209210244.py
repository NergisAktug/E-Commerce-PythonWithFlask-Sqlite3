import datetime
import sqlite3 as sql
from flask import Flask,flash, request, render_template_string, render_template
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



    app = Flask(__name__)
    app.config.from_object(__name__ + '.ConfigClass')

    db = SQLAlchemy(app)

    class Kullanici(db.Model):
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
        urunismi = db.Column(db.String(80))
        urunresmi = db.Column(db.String(80))
        urunFiyati = db.Column(db.Integer)
        markaId = db.Column(db.Integer(), db.ForeignKey('markalar.markaId', ondelete='CASCADE'))

        def __init__(self, urunismi, urunresmi, urunFiyati,markaId):
            self.urunismi =urunismi
            self.urunresmi = urunresmi 
            self.urunFiyati = urunFiyati
            self.markaId=markaId



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
    db.create_all()
    
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
    @app.route('/admin')
    def admin():
        return render_template("admin.html")

    @app.route('/uye', methods=['GET', 'POST'])
    def uye():
        return render_template("uyeGirisi.html")

    @app.route('/giris', methods=['GET', 'POST'])
    def giris():
        hata=None
        if request.method=='POST':
            if request.form['email']!='admin@example.com' or request.form['sifre']!='admin':
                if Kullanici.query.filter_by(email=request.form['email'],sifre=request.form['sifre']) is not None:
                    session['uye_giris']=True
                    return redirect(url_for('anasayfa'))
                else: 
                    hata='hatalı giris yaptınız'

            else:
                flash('giriş başarılı')
                session['admin_giris']=True
                return redirect(url_for('admin'))
        return render_template('uyeGiris.html',hata=hata)
    @app.route('/cikis')
    def cikis():

        session.pop('admin_giris',None)
        session.pop('uye_giris',None)
        return render_template("index.html")
    @app.route('/urunEkle')
    def urunEkle():
        tumVeri=urunler.query.all()
        return render_template("urunEkle.html",tumVeri=tumVeri)
    @app.route('/urunEklemeYap',methods=['POST'])
    def urunEklemeYap():
        urunismi=request.form['urunismi']
        urunResmi=request.form['urunresmi']
        urunFiyati=request.form['fiyati']
        markaId=request.form['markaId']
        yeniUrun=urunler(urunismi=urunismi,urunresmi=urunResmi,urunFiyati=urunFiyati,markaId=markaId)
        db.session.add(yeniUrun)
        db.session.commit()
        return redirect(url_for("urunEkle"))
    @app.route("/sil/<string:id>")
    def sil(id):
        urun=urunler.query.filter_by(urun_id=id).first()
        db.session.delete(urun)
        db.session.commit()
        return redirect(url_for("urunEkle"))
    @app.route('/guncelle/<string:id>',methods=['POST','GET'])
    def guncelle(id):
        try:
            urunismi = request.form.get("urunİsmi")
            urunresmi = request.form.get("urunresmi")
            urunFiyati = request.form.get("urunFiyati")
            markaId = request.form.get("markaId")
            urun = urunler.query.filter_by(urun_id=id).first()
            urun.urunismi = urunismi
            urun.urunresmi=urunresmi
            urun.urunFiyati=urunFiyati
            urun.markaId=markaId
            db.session.commit()
        except Exception as e:
            print("Couldn't update book title")
            print(e)
        return redirect(url_for('guncelle'))
    


        
        
       
    @app.route('/Markalar')
    def Markalar():
       tumMarka=markalar.query.all()
       return render_template("marka.html",tumMarka=tumMarka)
    return app
if __name__ == '__main__':
    app=create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)