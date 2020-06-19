from flask import Flask, render_template, redirect, request, url_for, session,flash, jsonify
from flask_mysqldb import MySQL, MySQLdb
from sqlalchemy import text
import bcrypt

# Start connect DB
app = Flask(__name__)

# app.config['MYSQL_USER']='root'
# app.config['MYSQL_PASSWORD']=''
# app.config['MYSQL_HOST']='localhost'
# app.config['MYSQL_DB']='lalin'
# app.config['MYSQL_CURSORCLASS']='DictCursor'
# # Stop connect
# mysql = MySQL(app)

@app.route("/")
def login():
    return ('hello ! ')

if __name__== "__main__" :
    app.run(debug=True)