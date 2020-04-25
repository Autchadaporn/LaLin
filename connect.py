from flask import Flask, render_template, redirect, request, url_for, session,flash
from flask_mysqldb import MySQL, MySQLdb
from sqlalchemy import text
import bcrypt

# Start connect DB
app = Flask(__name__)

app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_DB']='calendar'
app.config['MYSQL_CURSORCLASS']='DictCursor'
# Stop connect
mysql = MySQL(app)

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/test")
def test():
    return render_template('test.html') 

@app.route("/calendar")
def calendar(): 
        cur = mysql.connection.cursor()
        cur.execute("SELECT topic.Topic, calendar.Term, calendar.Start_Date, calendar.Finish_Date, calendar.Year FROM topic INNER JOIN calendar ON topic.Topic_ID = calendar.Topic_ID  ")
        rows=cur.fetchall()
        return render_template('calendar.html',datas=rows)

@app.route("/formsearch")
def formsearch():
    return render_template('formsearch.html')


@app.route("/search" ,methods=['GET', 'POST'])
def search():
    topic =  request.form['Topic']
    term =  request.form['Term']
    # print(topic)
    # print(term)
    cur = mysql.connection.cursor() #เชื่อมdatabase
    cur.execute("SELECT Start_Date,Finish_Date FROM calendar WHERE Topic_ID = '"+topic+"' AND Term = '"+term+"'")
    rows=cur.fetchall()
    return render_template('search.html',datas = rows)
    
    
app.run(debug=True)