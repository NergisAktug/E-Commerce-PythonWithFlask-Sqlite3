from flask import Flask,render_template,request
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