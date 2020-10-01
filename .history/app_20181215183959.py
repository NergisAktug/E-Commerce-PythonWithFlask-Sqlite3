import datetime
from flask import Flask,flash, request, render_template_string, render_template
from flask import Flask, url_for, render_template, request, redirect, session, escape, render_template_string
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required
from sqlalchemy.sql import table, column, select
from sqlalchemy import MetaData, create_engine
from flask_user import login_required, roles_required, UserManager, UserMixin
from flask_login import login_user


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
        def __init__(self, email, sifre,rolId):
            self.email = email
            self.sifre = sifre
            self.rolId =rolId

    class Roller(db.Model):
        __tablename__ = 'rol'
        rolId = db.Column(db.Integer, primary_key=True)
        rolisim = db.Column(db.String(80))

    class urunler(db.Model):
        __tablename__ = 'urunler'
        urun_id = db.Column(db.Integer, primary_key=True)
        urunismi = db.Column(db.String(80))
        urunresmi = db.Column(db.String(80))
        urunstok=db.Column(db.Integer)
        urunFiyati = db.Column(db.Integer)
        markaId = db.Column(db.Integer,db.ForeignKey('markalar.markaId', ondelete='CASCADE'))

        def __init__(self, urunismi, urunresmi, urunFiyati,urunstok,markaId):
            self.urunismi =urunismi
            self.urunresmi = urunresmi 
            self.urunFiyati = urunFiyati
            self.markaId=markaId
            self.urunstok=urunstok
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
        siparisTarihi = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())
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
        
        marka=markalar.query.all()
        Urun=urunler.query.all()
        tumVeri=urunler.query.all()

        return render_template('index.html',tumVeri=tumVeri,Urun=Urun,marka=marka)

    @app.route('/kayit', methods=['GET', 'POST'])
    def kayit():
        if request.method == 'POST':
            mail = request.form['email']
            parola = request.form['sifre']
            yeniKullanici = Kullanici(email=mail, sifre=parola,rolId=0)
            db.session.add(yeniKullanici)
            db.session.commit()
            if yeniKullanici is not None:
                mesaj = "Kayıt Başarıyla Sağlanmıştır."
                return render_template("index.html", mesaj=mesaj)
        else:
            return render_template('kayit.html')
  

    @app.route('/uye', methods=['GET', 'POST'])
    def uye():
        return redirect(url_for('giris'))

    @app.route('/giris', methods=['GET', 'POST'])
    def giris():
        if request.method == 'GET':
            return render_template('uyeGiris.html')
        else:
            email = request.form['email']
            sifre = request.form['sifre']
            data = Kullanici.query.filter_by(email=email, sifre=sifre).first()
            if data is not None:

                if Kullanici.query.filter_by(email=email, sifre=sifre, rolId=1).first():
                    session['admin_giris'] = True
                    return render_template('admin.html',rolId = 1, gir = session['admin_giris'])
                else:
                    session['uye_giris'] = True
                    
                    return redirect(url_for('anasayfa',rolId = 0, gir = session['uye_giris']))
            else:
                return render_template('uyeGiris.html')
    @app.route('/cikis')
    def cikis():
        session.pop('admin_giris',None)
        session.pop('uye_giris',None)
        return redirect(url_for("anasayfa"))
    @app.route('/urunEkle')
    def urunGoster():
        tumVeri=urunler.query.all()
        return render_template("urunEkle.html",tumVeri=tumVeri)
   
    @app.route("/markasil/<string:id>")
    def markasil(id):
        marka=markalar.query.filter_by(urun_id=id).first()
        db.session.delete(marka)
        db.session.commit()
        return redirect(url_for('Markalar'))
    @app.route('/urunEklemeYap',methods=['POST'])
    def urunEklemeYap():
        urunismi=request.form['urunismi']
        urunResmi=request.form['urunresmi']
        urunFiyati=request.form['fiyati']
        urunStok=request.form['urunstok']
        markaId=request.form['markaId']
        yeniUrun=urunler(urunismi=urunismi,urunresmi=urunResmi,urunFiyati=urunFiyati,urunstok=urunStok,markaId=markaId)
        db.session.add(yeniUrun)
        db.session.commit()
        return redirect(url_for("urunGoster"))
    @app.route("/sil/<string:id>")
    def sil(id):
        urun=urunler.query.filter_by(urun_id=id).first()
        db.session.delete(urun)
        db.session.commit()
        return redirect(url_for('urunGoster'))
    @app.route('/guncelle/<string:id>',methods=['POST','GET'])
    def guncelle(id):
        try:
            urunismi = request.form.get("urunİsmi")
            urunresmi = request.form.get("urunresmi")
            urunFiyati = request.form.get("urunFiyati")
            urunStok=request.form.get("urunstok")
            markaId = request.form.get("markaId")
            urun = urunler.query.filter_by(urun_id=id).first()
            urun.urunismi = urunismi
            urun.urunresmi=urunresmi
            urun.urunFiyati=urunFiyati
            urun.urunstok=urunStok
            urun.markaId=markaId
            db.session.commit()
        except Exception as e:
            print("güncelleme yapılamadı")
            print(e)
        return redirect(url_for('urunGoster'))
    @app.route('/sepetGoster')
    def sepetGoster():

        return render_template("sepet.html")
    @app.route('/sepet/<string:id>',methods=['POST','GET'])
    def sepet(id):
        urun=urunler.query.filter_by(urun_id=id).first()
        marka=markalar.query.filter_by(markaId=id).first()
       
        return redirect(url_for('sepetGoster',urun=urun,marka=marka))
    
    
      
    @app.route('/Markalar',methods=['POST','GET'])
    def Markalar():
       tumMarka=markalar.query.all()
       return render_template("marka.html",tumMarka=tumMarka)

     @app.route('/markaguncelle/<string:id>',methods=['POST','GET'])
    def guncelle(id):
        try:
            ad = request.form.get("markaadi")
            model = request.form.get("markamodeli")
            marka=markalar.query.filter_by(markaId=id).first()
            marka.markaadi=ad
            marka.marka_modeli=model
            
            db.session.commit()
        except Exception as e:
            print("güncelleme yapılamadı")
            print(e)
        return redirect(url_for('Markalar'))
    return app
if __name__ == '__main__':
    app=create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)