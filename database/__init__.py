'''
    Create a database for storing emails.
'''

__author__ = "rexcheng"

import mysql.connector as connector
from functools import reduce

def login_server():
    print("NOTE: Make sure you start the mysql server manually before running this script!")
    usr = input("Enter your username for your mysql database server: ")
    pwd = input("Enter your password for your mysql database server: ")
    db = connector.connect(
        host = "localhost",
        user = usr,
        passwd = pwd
    )
    return usr, pwd, db

def create_database(usr, pwd, db):
    cur = db.cursor()
    # Determine whether database "Enron" exist.
    cur.execute("SHOW DATABASES")
    dbName = "Enron"
    existence = reduce(lambda x, y: x or y,
        map(lambda x: dbName in x, cur)
    )
    if not existence:
        cur.execute("CREATE DATABASE " + dbName)
    cur.close()
    db.close()

    db = connector.connect(
        host = "localhost",
        user = usr,
        passwd = pwd,
        database = dbName
    )
    return db


if __name__ == "__main__":
    usr, pwd, db = login_server()
    db = create_database(usr, pwd, db)
    db.close()
