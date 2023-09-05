import sqlite3 as sql
from flask import Flask,g
import json


app = Flask(__name__)



@app.route("/")
def hello_world():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from projects")
   
   results = cur.fetchall()
   results = [tuple(row) for row in results]
   results = json.dumps(results)
   return results