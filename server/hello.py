"""Used to spin up the server """
import sqlite3 as sql
import flask
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)


def connect_to_db():
    """Opens a connection to the database"""
    con = sql.connect("database.db")
    cur = con.cursor()
    return con, cur


def select_all_from_db(column, value, cursor):
    """Returns all objects from a db with only 1 filter"""
    cursor.execute(f"select * from projects where {column}=?", (value,))
    return cursor.fetchall()


def unpack_data(data, cursor):
    """unpacks the data object"""
    results = []
    columns = [column[0] for column in cursor.description]
    for row in data:
        results.append(dict(zip(columns, row)))
    return results


def add_user_to_db(values, con, cursor):
    """Adds a user to the database"""
    cursor.execute(
        "INSERT INTO PROJECTS (email,name) VALUES (?,?)", (values[0], values[1])
    )
    con.commit()


def delete_user_from_db(email, con, cur):
    """Deletes a user from the database"""
    cur.execute("delete form projects where email =?", (email,))
    con.commit()


def handle_post_request():
    """Handles the post request"""
    if request.args.get("email") is None or request.args.get("name") is None:
        return {"status": "failure", "error": "This was unable to be registered"}

    email = request.args.get("email")
    name = request.args.get("name")

    con, cur = connect_to_db()
    data = select_all_from_db("email", email, cur)
    data = unpack_data(data, cur)

    if data:
        return {"status": "failure", "error": "This email is already registered"}

    add_user_to_db([email, name], con, cur)

    data = select_all_from_db("email", email, cur)
    data = unpack_data(data, cur)

    con.close()

    if not data:
        return {
            "status": "failure",
            "error": "This process was unable to be completed",
        }

    return {"status": "success", "response": data}


def handle_delete_request():
    """Handles the case where the server receives a delete request"""

    if request.args.get("email") is None:
        return {"status": "failure", "error": "Missing Fields"}

    email = request.args.get("email")
    con, cur = connect_to_db()
    data = select_all_from_db("email", email, cur)
    data = unpack_data(data, cur)

    if not data:
        return {"status": "failure", "error": "Email not found"}

    delete_user_from_db(email, con, cur)
    data = select_all_from_db("email", email, cur)
    data = unpack_data(data, cur)

    if not data:
        return {"status": "success", "message": "user deleted"}

    return {"status": "failure", "error": "user not able to be deleted"}


def handle_get_request():
    """Handling the serve getting a get request"""
    is_empty = True

    try:
        email = request.args.get("email")
        if email is not None:
            process_message = "email given"
            is_empty = False
        else:
            process_message = "no email given"
    except TypeError:
        pass

    con, cur = connect_to_db()

    if is_empty:
        cur.execute("""SELECT * FROM PROJECTS""")

        data = cur.fetchall()
        data = unpack_data(data, cur)
        con.close()

        if not data:
            return {
                "status": "failure",
                "error": "This data was not able to be returned",
            }
        return jsonify(
            {
                "response": data,
                "status": "success",
                "body_status": process_message,
            }
        )

    data = select_all_from_db("email", email, cur)
    data = unpack_data(data, cur)
    con.close()
    if not data:
        return {
            "status": "failure",
            "error": "This user data was not able to be returned",
        }
    return jsonify(
        {
            "response": data,
            "status": "success",
            "body_status": process_message,
        }
    )


def handle_update_email(cur, con, new_name, email):
    """handles updating the email"""

    cur.execute("""UPDATE PROJECTS SET name=? WHERE email=?""", (new_name, email))
    con.commit()
    data = select_all_from_db("email", email, cur)
    data = unpack_data(data, cur)
    con.close()

    if data[0]["name"] != new_name:
        return {"status": "failure", "error": "unable to update user "}
    return {"status": "success", "message": "user successfully edited"}


def handle_put_request():
    """Server handling the put request from a user"""
    if (
        request.args.get("email") is None
        or request.args.get("name") is None
        or request.args.get("newName") is None
        or request.args.get("newEmail") is None
    ):
        return {"status": "failure", "error": "Missing Fields"}

    email = request.args.get("email")
    name = request.args.get("name")
    new_name = request.args.get("newName")
    new_email = request.args.get("newEmail")

    con, cur = connect_to_db()
    cur.execute("""SELECT * FROM PROJECTS where email=? and name=?""", (email, name))
    data = cur.fetchall()
    data = unpack_data(data, cur)
    if not data:
        con.close()
        return {"status": "failure", "error": "this user does not exist"}

    if new_email == email:
        handle_update_email(cur, con, new_name, email)

    cur.execute("""UPDATE PROJECTS SET name=? WHERE email=?""", (new_name, email))
    con.commit()
    data = select_all_from_db("email", email, cur)
    data = unpack_data(data, cur)

    if data:
        con.close()
        return {
            "status": "failure",
            "error": "the new email is already registered",
        }

    cur.execute(
        """UPDATE PROJECTS SET name=?,email=? WHERE email=?""",
        (new_name, new_email, email),
    )
    con.commit()
    data = select_all_from_db("email", email, cur)
    data = unpack_data(data, cur)
    con.close()
    if not data:
        return {"status": "failure", "error": "unable to update user "}
    return {"status": "success", "message": "user successfully added"}


@app.route("/user", methods=["POST", "DELETE", "GET", "PUT"])
@cross_origin()
def user():
    """Add A User to the database"""
    if flask.request.method == "POST":
        handle_post_request()
    if flask.request.method == "DELETE":
        handle_delete_request()
    if flask.request.method == "GET":
        handle_get_request()
    if flask.request.method == "PUT":
        handle_put_request()
