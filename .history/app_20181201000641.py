import datetime
from flask import Flask, request, render_template_string
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin

import sqlite3
app=Flask(__name__)

@app.route('/')
def home():
    return render_template('/index.html')

@app.route('/üye')
def uye():
    return render_template('/üye.html')





if __name__=='__main__':
    app.run(debug=True)