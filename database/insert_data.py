'''
    Insert data into the database.
'''

__author__ = "rexcheng"

import mysql.connector as connector
from .retrieve_data import get_current_id, fetch_eid
from .alter_tables import alter_sequence

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
        print(cur.rowcount, "row inserted in Employees.")
    except connector.errors.IntegrityError as e:
        cur.close()
        alter_sequence(db, "Employees", get_current_id(db, "Employees") + 1)
        return fetch_eid(db, name)
    except connector.errors.DataError as e:
        cur.close()
        db.close()
        print("Employee name that caused the error:", name)
        print("Error code:", e)
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
        print(cur.rowcount, "row inserted in Messages.")
    except connector.errors.IntegrityError as e:
        pass
    except connector.errors.DataError as e:
        cur.close()
        db.close()
        print("Message content that caused the error:", content)
        print("Error code:", e)
    cur.close()
    return get_current_id(db, "Messages")

def insert_send(db, mid, eid, date):
    cur = db.cursor()
    try:
        cur.execute("""
            INSERT INTO Send (mid, eid, date)
            VALUES (%s, %s, %s)
            """,
            (mid, eid, date)
        )
        db.commit()
        print(cur.rowcount, "row inserted in Send.")
    except connector.errors.IntegrityError as e:
        pass
    except connector.errors.DataError as e:
        cur.close()
        db.close()
        print("Sent date that caused the error:", date)
        print("Error code:", e)
    cur.close()

def insert_receive(db, mid, eid):
    cur = db.cursor()
    try:
        cur.execute("""
            INSERT INTO Receive (mid, eid)
            VALUES (%s, %s)
            """,
            (mid, eid)
        )
        db.commit()
        print(cur.rowcount, "row inserted in Receive.")
    except connector.errors.IntegrityError as e:
        pass
    cur.close()
