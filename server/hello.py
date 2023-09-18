import sqlite3 as sql

import flask
from flask import Flask,request,jsonify
from flask_cors import CORS,cross_origin
import json


app = Flask(__name__)
cors = CORS(app)



@app.route("/user",methods=['POST','DELETE','GET','PUT'])
@cross_origin()
def user():


   if flask.request.method == 'POST':

      """ Add A User to the database"""

      """Ccheck to see if request is empty"""
      if request.args.get('email') is None or request.args.get('name') is None :
         return {'status': 'failure', 'error': 'This was unable to be registered'}


      email=request.args.get('email')
      name=request.args.get('name')

      """Check to see if email already used"""

      con = sql.connect("database.db")
      cur = con.cursor()


      cur.execute("""SELECT * FROM PROJECTS where email=?""",(email,))
      data = cur.fetchall()
      results=[]
      columns = [column[0] for column in cur.description]
      for row in data:
         results.append(dict(zip(columns, row)))
      if data != []:
         return {'status': 'failure', 'error': 'This email is already registered'}




      cur.execute("""INSERT INTO PROJECTS (name,email) VALUES (?,?)""",(name,email))
      con.commit()

      cur.execute("""SELECT * FROM PROJECTS where email=?""",(email,))
      data = cur.fetchall()
      con.close()


      results=[]
      columns = [column[0] for column in cur.description]
      for row in data:
         results.append(dict(zip(columns, row)))
      con.close()


      if data == []:
         return {'status': 'failure', 'error': 'This process was unable to be completed'}

      return {'status': 'success','response':results}




   elif flask.request.method == 'DELETE':

      """ Delete A User from the database"""


      """Check to see if request is empty"""
      if request.args.get('email') is None:
         return {'status': 'failure', 'error': 'Missing Fields'}

      email=request.args.get('email')

      """Check to see if email exists """

      con = sql.connect("database.db")
      cur = con.cursor()


      cur.execute("""SELECT * FROM PROJECTS where email=?""" ,(email,))
      data = cur.fetchall()
      results=[]
      columns = [column[0] for column in cur.description]
      for row in data:
         results.append(dict(zip(columns, row)))
      if data == []:
         return {'status': 'failure', 'error': 'Email not found'}




      cur.execute("""DELETE from PROJECTS WHERE email=?""",(email,))
      con.commit()




      cur.execute("""SELECT * FROM PROJECTS where email=?""" ,(email,))
      data = cur.fetchall()
      results=[]
      columns = [column[0] for column in cur.description]
      for row in data:
         results.append(dict(zip(columns, row)))


      if data == []:
         return {'status': 'success', 'message':'user deleted'}

      return {'status': 'failure', 'error':'user not able to be deleted'}


   elif flask.request.method == 'GET':

      """Return a single user or all users"""

      isEmpty=True

      try:
         email=request.args.get('email')
         if email is not None:
            process_message='email given'
            isEmpty=False
         else:
            process_message = "no email given"
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
         return jsonify({"response": results, 'status': 'success','body_status':process_message})

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
         return jsonify({"response":results,'status':'success','body_status':process_message})

   elif flask.request.method == 'PUT':

      """Update a User"""



      """Check to see if request is empty"""
      if request.args.get('email') is None or request.args.get('name') is None or request.args.get('newName') is None or request.args.get('newEmail') is None:
         return {'status': 'failure', 'error': 'Missing Fields'}


      email = request.args.get('email')
      name = request.args.get('name')
      newName = request.args.get('newName')
      newEmail = request.args.get('newEmail')



      con = sql.connect("database.db")
      cur = con.cursor()

      """Check to see if old Entry Exists"""

      cur.execute("""SELECT * FROM PROJECTS where email=? and name=?""", (email,name))
      data = cur.fetchall()
      results = []
      columns = [column[0] for column in cur.description]
      for row in data:
         results.append(dict(zip(columns, row)))
      if data == []:
         con.close()
         return {'status': 'failure', 'error': 'this user does not exist'}



      """Check to see if only name is being updated"""
      if newEmail == email:

         """Update the name"""

         cur.execute("""UPDATE PROJECTS SET name=? WHERE email=?""", (newName,email))
         con.commit()
         cur.execute("""SELECT * FROM PROJECTS where email=?""", (email,))
         data = cur.fetchall()
         con.close()

         results = []
         columns = [column[0] for column in cur.description]
         for row in data:
            results.append(dict(zip(columns, row)))

         """Check to see if username was updated"""
         if results[0]['name']!=newName:
            return {'status': 'failure', 'error': 'unable to update user '}
         else:
            return {'status':'success','message':'user successfully edited'}

      else:

         """Check to see that new email doesn't already exist"""

         cur.execute("""SELECT * FROM PROJECTS where email=?""", (newEmail,))
         data = cur.fetchall()
         results = []
         columns = [column[0] for column in cur.description]
         for row in data:
            results.append(dict(zip(columns, row)))
         if data != []:
            con.close()
            return {'status': 'failure', 'error': 'the new email is already registered'}


         """Update the User"""

         cur.execute("""UPDATE PROJECTS SET name=?,email=? WHERE email=?""", (newName,newEmail,email))
         con.commit()
         cur.execute("""SELECT * FROM PROJECTS where email=?""", (newEmail,))
         data = cur.fetchall()
         con.close()

         results = []
         columns = [column[0] for column in cur.description]
         for row in data:
            results.append(dict(zip(columns, row)))

         """Check to see if username was updated"""
         if data==[]:
            return {'status': 'failure', 'error': 'unable to update user '}
         else:
            return {'status': 'success', 'message': 'user successfully added'}




