'''
    Retrieve data from the database.
'''

__author__ = "rexcheng"

import mysql.connector as connector

def get_current_id(db, table):
    cur = db.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM %s
        """,
        (table, )
    )
    result = cur.fetchall()
    cur.close()
    return result[0][0]

def fetch_eid(db, name):
    cur = db.cursor()
    try:
        cur.execute("""
            SELECT eid FROM Employees
            WHERE name = %s
            """,
            (name, )
        )
        result = cur.fetchall()
    except connector.errors.DataError as e:
        print("No matching row with " + name + " found in the database!")
        confirm = input("Do you want to exit the program? (y/n): ")
        if confirm != 'n':
            print("Program terminated by the user.")
            cur.close()
            db.close()
            exit()
    cur.close()
    return result[0][0]
