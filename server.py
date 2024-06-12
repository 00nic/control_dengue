from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQLdb
from dotenv import load_dotenv
import os

app = Flask (__name__, static_url_path='/static ')
load_dotenv()
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_CURSORCLASS'] = os.getenv('MYSQL_CURSORCLASS')



if __name__ == '__main__':
    app.run(port = 5000, debug = True)