'''
    Insert data into the database.
'''

__author__ = "rexcheng"

import mysql.connector as connector

def insert_employee(db, name):
    cur = db.cursor()
    # try:
    cur.execute("""
        INSERT INTO Employees (name)
        VALUES (%s)
        """,
        (name, )
    )
    db.commit()
    print(cur.rowcount, "row inserted.")
    cur.close()
