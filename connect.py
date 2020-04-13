from flask import Flask,render_template,request,redirect,url_for
import pymysql

# Start connect DB
app = Flask(__name__)
#conn=pymysql.connect('localhost','root','','studentdb')
# Stop connect

@app.route("/login")
def login():
    return render_template('login.html')
app.run(debug=True)   