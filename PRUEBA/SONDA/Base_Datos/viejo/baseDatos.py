import sqlite3

conn=sqlite3.connect('SondaV5.db')

c=conn.cursor()


##Para crear tablas
c.execute("""CREATE TABLE sensores (
            tiempo DATETIME,
            temp NUMERIC,
            pH NUMERIC,
            ce NUMERIC,
            od NUMERIC,
            opr NUMERIC,
            color NUMERIC   
            )""")

conn.commit()

conn.close()