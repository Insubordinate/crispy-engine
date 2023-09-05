import sqlite3 as sql


with sql.connect('database.db') as con:
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS projects')
    cur.execute("""CREATE TABLE IF NOT EXISTS projects (id integer PRIMARY KEY,name text NOT NULL,email NOT null); """)

    cur.execute(" INSERT into projects (name,email) VALUES (?,?)",('bob','something@multiverse.com'))
    cur.execute(" INSERT into projects (name,email) VALUES (?,?)", ('bill','notsomething@multiverse.com'))
    cur.execute(" INSERT into projects (name,email) VALUES (?,?)", ('ted','definitelysomething@multiverse.com'))