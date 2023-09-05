import sqlite3 as sql


with sql.connect('database.db') as con:
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS projects')
    cur.execute(""" CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """)
    
    cur.execute(" INSERT into projects (id,name,begin_date,end_date) VALUES (?,?,?,?)",(1,'bob',2021,2023))