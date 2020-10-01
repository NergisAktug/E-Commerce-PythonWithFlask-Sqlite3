"""Flask Login Example and instagram fallowing find"""

from flask import Flask, url_for, render_template, request, redirect, session, escape, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'any random string'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eticaret.db'
db = SQLAlchemy(app)


class Kullanici(db.Model):
    __tablename__ = 'Kullanici'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    sifre = db.Column(db.String(80))
    rolId = db.Column(db.Integer, db.ForeignKey('rol.rolId', ondelete='CASCADE'))

    def __init__(self, email, sifre, rolId):
        self.email = email
        self.sifre = sifre
        self.rolId = 0


class Roller(db.Model):
    __tablename__ = 'rol'
    rolId = db.Column(db.Integer, primary_key=True)
    rolIsım = db.Column(db.String(80))


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


class sepet(db.Model):
    __tablename__ = 'sepet'
    sepetId = db.Column(db.Integer, primary_key=True)
    urunId = db.Column(db.Integer(), db.ForeignKey('urunler.urun_id', ondelete='CASCADE'))

    def __init__(self, urunId):
        self.urunId = urunId

db.create_all()
@app.route('/')
def index():
    if not session.get('giris_yap'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            return render_template('index.html')
        return render_template('index.html')


@app.route('/uye')
def uye():
    return render_template('uye.html')


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
            return render_template('index.html')


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
            mesaj = "kayıt başarıyla sağlanmıştır."
            return render_template('index.html', mesaj=mesaj)

    return render_template('kayit.html')


@app.route("/cıkıs")
def cıkıs():
    session['giris_yap'] = False
    return redirect(url_for('index'))


@app.route("/admin")
def admin():
    return render_template("admin.html")


if __name__ == '__main__':
    
    app.run(debug=True)