# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

import datetime
from flask import Flask, request, render_template_string,render_template,redirect,url_for
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin

# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """
   
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
    
    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///eticaret.sqlite'    # File-based SQL database
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

    # Initialize Flask-BabelEx
    babel = Babel(app)
    # Initialize Flask-SQLAlchemy
    @babel.localeselector
    def get_locale():
       translations = [str(translation) for translation in babel.list_translations()]
    #   return request.accept_languages.best_match(translations)
    # @babel.localeselector
    #def get_locale():
    #   if request.args.get('lang'):
    #       session['lang'] = request.args.get('lang')
    #       return session.get('lang', 'tr')

    db = SQLAlchemy(app)

    # Define the User data-model.
    # NB: Make sure to add flask_user UserMixin !!!
    class User(db.Model, UserMixin):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

        # User authentication information. The collation='NOCASE' is required
        # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
        email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
        email_confirmed_at = db.Column(db.DateTime())
        password = db.Column(db.String(255), nullable=False, server_default='')

        # User information
        first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
        last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

        # Define the relationship to Role via UserRoles
        roles = db.relationship('Role', secondary='user_roles')

    # Define the Role data-model
    class Role(db.Model):
        __tablename__ = 'roles'
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

    # Define the UserRoles association table
    class UserRoles(db.Model):
        __tablename__ = 'user_roles'
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

    
     # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)

    # Create all database tables
    db.create_all()

   



    # The Home page is accessible to anyone
    @app.route('/')
    def index():
        veriler=User.query.all()
        return render_template("index.html",veriler=veriler)

    @app.route('/üye')
    def uye():
        return render_template("üye.html")
    @app.route('/add',methods=["POST"])
    def adduser():
        email=request.form.get("e-mail")
        sifre=request.form.get("sifre")
        email_confirmed_at=datetime.datetime.utcnow()
        newuser=User(email=email,password=sifre,email_confirmed_at=email_confirmed_at)
        db.session.add(newuser)
        db.session.commit()
        return  redirect(url_for("uye"))

    return app







# Start development web server
if __name__ == '__main__':
    app = create_app()
   # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='127.0.0.1', port=5000, debug=True)
