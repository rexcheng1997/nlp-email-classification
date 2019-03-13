'''
    Create a database for storing emails.
'''

__author__ = "rexcheng"

import mysql.connector as connector
from functools import reduce
from getpass import getpass

def login_server():
    print("NOTE: Make sure you start the mysql server manually before running this script!")
    usr = input("Enter your username for your mysql database server: ")
    pwd = getpass("Enter your password for your mysql database server: ")
    db = connector.connect(
        host = "localhost",
        user = usr,
        passwd = pwd
    )
    return usr, pwd, db

def create_database(usr, pwd, db):
    cur = db.cursor()
    dbName = "Enron"
    try:
        cur.execute("CREATE DATABASE " + dbName)
        print("Successfully created database \"%s\"!" % dbName)
    except connector.errors.DatabaseError as e:
        print("Database \"%s\" already exists. Continue using the previous one." % dbName)
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
