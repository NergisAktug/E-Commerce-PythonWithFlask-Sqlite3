from flask import Flask,render_template,request
import sqlite3

@app.route('/')
def home():
    return render_template('/index.html')