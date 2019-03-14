'''
    Insert data into the database.
'''

__author__ = "rexcheng"

import mysql.connector as connector
from .retrieve_data import get_current_id, fetch_eid

def insert_employee(db, name):
    cur = db.cursor()
    try:
        cur.execute("""
            INSERT INTO Employees (name)
            VALUES (%s)
            """,
            (name, )
        )
        db.commit()
        print(cur.rowcount, "row inserted.")
    except connector.errors.IntegrityError as e:
        return fetch_eid(db, name)
    cur.close()
    return get_current_id(db, "Employees")

def insert_message(db, content):
    cur = db.cursor()
    try:
        cur.execute("""
            INSERT INTO Messages (content)
            VALUES (%s)
            """,
            (content, )
        )
        db.commit()
        print(cur.rowcount, "row inserted.")
    except connector.errors.IntegrityError as e:
        pass
    cur.close()
    return get_current_id(db, "Messages")
