import sqlite3 as sql

import flask
from flask import Flask,request,jsonify
from flask_cors import CORS,cross_origin
import json


app = Flask(__name__)
cors = CORS(app)



@app.route("/user",methods=['POST','DELETE','GET'])
@cross_origin()
def user():
   if flask.request.method == 'POST':
      content = request.get_json(silent=True)
      name = content['name']
      email = content['email']


      con = sql.connect("database.db")
      con.row_factory = sql.Row

      cur = con.cursor()
      cur.execute("""INSERT INTO PROJECTS (name,email) VALUES (?,?)""",(name,email))
      cur.execute("""SELECT * FROM PROJECTS where email=?""",(email,))
      data = cur.fetchall()
      con.close()

      if data == []:
         return {'status':'failure','error':'This was unable to be registered'}

      return {'status':'success'}

   elif flask.request.method == 'DELETE':

      content = request.get_json(silent=True)
      email = content['email']

      con = sql.connect("database.db")
      con.row_factory = sql.Row

      cur = con.cursor()
      cur.execute("""DELETE  FROM  PROJECTS WHERE (email) = ?""", (email,))
      cur.execute("""SELECT * FROM PROJECTS where email=?""", (email,))
      data = cur.fetchall()
      con.close()
      if data != []:
         return {'status': 'failure', 'error': 'This was unable to be registered'}

      return {'status': 'success'}

   elif flask.request.method == 'GET':

      content = request.get_json(silent=True)




      isEmpty=True
      try:
         email=content['email']
         isEmpty=False
      except:
         pass




      con = sql.connect("database.db")
      cur = con.cursor()




      if isEmpty:
         cur.execute("""SELECT * FROM PROJECTS""")
         data = cur.fetchall()
         columns = [column[0] for column in cur.description]
         results = []
         for row in data:
            results.append(dict(zip(columns, row)))
         con.close()
         if data == []:
            return {'status': 'failure', 'error': 'This data was not able to be returned'}
         return jsonify({"response": results, 'status': 'success'})

      else:
         cur.execute("""SELECT * FROM PROJECTS where email=?""", (email,))
         data = cur.fetchall()
         columns = [column[0] for column in cur.description]
         results = []
         for row in data:
            results.append(dict(zip(columns, row)))

         con.close()
         if data == []:
            return {'status': 'failure', 'error': 'This user data was not able to be returned'}
         return jsonify({"response":results,'status':'success'})

