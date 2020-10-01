import time
import os
from flask import Flask,flash, request, render_template
from flask import Flask, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import table, column, select
import hashlib



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

    UPLOAD_FOLDER = os.path.basename('uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        urunresmi = db.Column(db.String(256))
        urunstok=db.Column(db.Integer)
        popular = db.Column(db.Text)
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
        kactanesatinalınmıs = db.Column(db.Text, nullable=False)
        siparisTarihi = db.Column(db.Text,nullable=False)
        

        def __init__(self, musteriId, urunId, kactanesatinalınmıs, siparisTarihi):
            self.musteriId = musteriId
            self.urunId = urunId
            self.kactanesatinalınmıs =kactanesatinalınmıs
            self.siparisTarihi = siparisTarihi
           
      
    db.create_all()
  
    AlısverisCantasi=[]
    
    
    @app.route('/')
    def anasayfa():
        
        marka=markalar.query.all()
        Urun=urunler.query.all()
        tumVeri=urunler.query.all()

        return render_template('index.html',tumVeri=tumVeri,Urun=Urun,marka=marka)

    @app.route('/yukle', methods=['POST'])
    def yukle():
        file= request.files['image']
        f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(f)
        return redirect(url_for('anasayfa'))

    @app.route('/kayit', methods=['GET', 'POST'])
    def kayit():
        if request.method == 'POST':
            mail = request.form['email']
            parola = request.form['sifre']
            sifrelenmis = hashlib.sha256(parola.encode("utf8")).hexdigest()
            yeniKullanici = Kullanici(email=mail, sifre=sifrelenmis ,rolId=0)
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
            sifrelenmis = hashlib.sha256(sifre.encode("utf8")).hexdigest()
            data = Kullanici.query.filter_by(email=email, sifre=sifrelenmis ).first()
            if data is not None:

                if Kullanici.query.filter_by(email=email, sifre=sifre, rolId=1).first():
                    session['admin_giris'] = True
                    return render_template('admin.html',rolId = 1, gir = session['admin_giris'])
                else:
                    session['uye_giris'] = True
                    session['sepett'] = AlısverisCantasi
                    session['id'] =data.id
                    session['name']=data.email
                    return redirect(url_for('anasayfa',rolId = 0, gir = session['uye_giris']))
            else:
                return render_template('uyeGiris.html')
    @app.route('/cikis')
    def cikis():
        session['admin_giris'] = False
        session['uye_giris'] = False
        session.pop('sepett', None)
        return redirect(url_for("anasayfa"))
    @app.route('/urunEkle')
    def urunGoster():
        tumVeri=urunler.query.all()
        return render_template("urunEkle.html",tumVeri=tumVeri)
   
    
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
    @app.route('/sepett')
    def sepett():
        if 'uye_giris' in session:
            if (session['uye_giris']==True):
                al=session['sepett']
                return render_template('sepet.html',sepet=al)
            else:
                return redirect(url_for('anasayfa'))
        else:
            session['uye_giris']=False
            return redirect(url_for('anasayfa'))  
    @app.route('/sepet/<string:id>',methods=['POST','GET'])
    def sepet(id):
        if 'uye_giris' in session:
            if (session['uye_giris']==True):
                urun = urunler.query.filter_by(urun_id=id).first()
                marka = markalar.query.filter_by(markaId=id).first()
                durum = False
                AlısverisCantasi=session['sepett']
                for herbirsatir in AlısverisCantasi:
                    if (herbirsatir['id']==str(id)):
                        durum=True
                if AlısverisCantasi==[]:
                    adet=1
                    toplam=adet*urun.urunFiyati
                    sepeturun={
                        'id':urun.urun_id,
                        'urunresmi':urun.urunresmi 
                        'isim':urun.urunismi,
                        'urunFiyati':urun.urunFiyati,
                        'urunmodeli':marka.marka_modeli,
                        'adet': adet,
                        'toplam': toplam
                    }
                    AlısverisCantasi.append(sepeturun)
                    session['sepett']=AlısverisCantasi
                elif  durum==True:
                    bossepet=[]
                    for satir in AlısverisCantasi:
                        if str(satir['id'])==str(id):
                            adet=int(satir['adet'])
                            adet+=1
                            fiyat=int(satir['urunFiyati'])
                            toplam=adet*fiyat
                            satir['adet'] = str(adet)
                            satir['toplam'] = str(toplam)
                            bossepet.append(satir)
                        else:
                            bossepet.append(satir)
                else:
                    adet=1
                    toplam=adet*urun.urunFiyati
                    sepeturun={
                        'id':urun.urun_id,
                        'isim':urun.urunismi,
                        'urunFiyati':urun.urunFiyati,
                        'urunmodeli':marka.marka_modeli,
                        'adet': adet,
                        'toplam': toplam
                    }
                    AlısverisCantasi.append(sepeturun)
                session['sepett']=AlısverisCantasi
                return redirect(url_for('sepett'))
            else:
                return redirect(url_for('giris'))
        else:
            session['uye_giris']=False
            return redirect(url_for('giris'))

      
    @app.route('/Markalar',methods=['POST','GET'])
    def Markalar():
       tumMarka=markalar.query.all()
       return render_template("marka.html",tumMarka=tumMarka)

    
    @app.route('/markaEklemeYap',methods=['POST'])
    def markaEklemeYap():
        ad=request.form['markaadi']
        model=request.form['markamodeli']
        yenimarka=markalar(markaadi=ad,marka_modeli=model)
        db.session.add(yenimarka)
        db.session.commit()
        return redirect(url_for("Markalar"))
    @app.route('/sepetguncelle/<string:urunid>',methods=['POST','GET'])
    def sepetguncelle(urunid):
        if 'uye_giris' in session:
            if (session['uye_giris']==True):
                if request.method=='GET':
                    return redirect(url_for('anasayfa'))
                else:
                    adet=int(request.form['adet'])#form dan yeni adet bilgisi çekiliyor.
                    guncellsepet=[]
                    guncellsepet=session['sepett']
                    AlısverisCantasi.clear()
                    for degistir in guncellsepet:
                        if str(degistir['id'])==str(urunid):
                            fiyat=int(degistir['urunFiyati'])
                            toplam=(fiyat*adet)
                            degistir['adet']=str(adet)
                            degistir['toplam']=str(toplam)
                        AlısverisCantasi.append(degistir)
                    session['sepett']=AlısverisCantasi
                    return redirect(url_for('sepett'))
            else:
                return redirect(url_for('giris'))
        else:
            session['uye_giris']=False
            return render_template('uyeGiris.html')
    @app.route('/sepetisil/<string:urunid>',methods=['POST','GET'])
    def sepetisil(urunid):
        if 'uye_giris' in session:
            if (session['uye_giris']==True):
                silsepeti=[]
                silsepeti=session['sepett']
                AlısverisCantasi.clear()
                for sil in silsepeti:
                    if str(sil['id'])!=str(urunid):
                        AlısverisCantasi.append(sil)
                session['sepett']=AlısverisCantasi
                return render_template('sepet.html',sepet=session['sepett'])
            else:
                return redirect(url_for('giris'))
        else:
            session['uye_giris']=False
            return redirect(url_for('giris'))
    @app.route('/tumsepetisil',methods=['POST','GET'])
    def tumsepetisil():
        if 'uye_giris' in session:
            if (session['uye_giris']==True):
                AlısverisCantasi.clear()
                session['sepett']=AlısverisCantasi
                return redirect(url_for('sepett'))
            else:
                return redirect(url_for('giris'))
        else:
            session['uye_giris']=False
            return redirect(url_for('giris'))
    @app.route('/satınAl')
    def satınAl():
        if 'uye_giris' in session:
            if (session['uye_giris']==True):
                satinalanid=session['id']
                AlısverisCantasi=session['sepett']
                for urun in AlısverisCantasi:
                    urunidd=int(urun['id'])
                    adet=urun['adet']
                    urunn=urunler.query.filter_by(urun_id=urunidd).first()
                    eski=int(urunn.popular)
                    urunn.popular=str(int(adet)+eski)
                    urunn.urunstok-=int(adet)
                    db.session.add(urunn)
                    db.session.commit()
                    tarih=str(time.strftime("%x")+"-"+time.strftime("%X"))
                    siparisgecmisi=siparis(musteriId=satinalanid,urunId=urunidd,kactanesatinalınmıs=adet,siparisTarihi=tarih)
                    db.session.add(siparisgecmisi)
                    db.session.commit()
                AlısverisCantasi.clear()
                session['sepett']=AlısverisCantasi
                return redirect(url_for('sepett'))
            else:
                return redirect(url_for('giris'))
        else:
            session['uye_giris']=False
            return redirect(url_for('giris'))

    @app.route('/siparisgecmisi')
    def siparisgecmisi():
        if 'uye_giris' in session:
            if (session['uye_giris']==True):
                kullaniciId=session['id']
                gecmissiparis=siparis.query.filter_by(musteriId=kullaniciId)
                gecmissiparisleritut=[]
                for s in gecmissiparis:
                    urunn=urunler.query.filter_by(urun_id=s.urunId).first()
                    model=markalar.query.filter_by(markaId=s.urunId).first()
                    benimsiparisgecmisim={
                            'urunisim':str(urunn.urunismi),
                            'urunresmi':str(urunn.urunresmi),
                            'urunadet':s.kactanesatinalınmıs,
                            'urunFiyati':str(urunn.urunFiyati),
                            'urunModeli':str(model.marka_modeli),
                            'satinalmatarihi':s.siparisTarihi

                            }
                    gecmissiparisleritut.append(benimsiparisgecmisim)
                return render_template('siparisgecmisi.html',sepet=gecmissiparisleritut)
            else:
                return redirect(url_for('giris'))
        else:
            session['uye_giris']=False
            return redirect(url_for('giris'))
       
    
    return app
if __name__ == '__main__':
    app=create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)