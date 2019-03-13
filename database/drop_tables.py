'''
    Drop tables.
'''

__author__ = "rexcheng"

import mysql.connector as connector

def drop_employees(db):
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS Employees")
    print("Successfully dropped TABLE Employees!")
    cur.close()

def drop_messages(db):
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS Messages")
    print("Successfully dropped TABLE Messages!")
    cur.close()

def drop_send(db):
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS Send")
    print("Successfully dropped TABLE Send!")
    cur.close()

def drop_receive(db):
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS Receive")
    print("Successfully dropped TABLE Receive!")
    cur.close()

def drop_all(db):
    confirm = input("Are you sure you want to drop all the tables? (y/n): ")
    if confirm != 'y':
        print("Cancelled dropping tables.")
        return
    drop_send(db)
    drop_receive(db)
    drop_messages(db)
    drop_employees(db)
