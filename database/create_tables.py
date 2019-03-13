'''
    Create tables.
'''

__author__ = "rexcheng"

import mysql.connector as connector

def create_employees(db):
    cur = db.cursor()
    try:
        cur.execute("""
            CREATE TABLE Employees (
                eid INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL
                CHECK (name NOT IN (
                    SELECT name FROM Employees
                    )
                )
            )
            """
        )
        print("Successfully created TABLE Employees!")
    except connector.errors.DatabaseError as e:
        print("TABLE Employees already exists. Continue using the previous one.")
    cur.close()

def create_messages(db):
    cur = db.cursor()
    try:
        cur.execute("""
            CREATE TABLE Messages (
                mid INT AUTO_INCREMENT PRIMARY KEY,
                content VARCHAR(1200) NOT NULL
            )
            """
        )
        print("Successfully created TABLE Messages!")
    except connector.errors.DatabaseError as e:
        print("TABLE Messages already exists. Continue using the previous one.")
    cur.close()

def create_send(db):
    cur = db.cursor()
    try:
        cur.execute("""
            CREATE TABLE Send (
                mid INT PRIMARY KEY,
                eid INT NOT NULL UNIQUE,
                date VARCHAR(50) NOT NULL,
                FOREIGN KEY (mid) REFERENCES Messages(mid) ON DELETE CASCADE,
                FOREIGN KEY (eid) REFERENCES Employees(eid) ON DELETE NO ACTION
            )
            """
        )
        print("Successfully created TABLE Send!")
    except connector.errors.DatabaseError as e:
        print("TABLE Send already exists. Continue using the previous one.")
    cur.close()

def create_receive(db):
    cur = db.cursor()
    try:
        cur.execute("""
            CREATE TABLE Receive (
                mid INT,
                eid INT,
                PRIMARY KEY (mid, eid),
                FOREIGN KEY (mid) REFERENCES Messages(mid) ON DELETE NO ACTION,
                FOREIGN KEY (eid) REFERENCES Employees(eid) ON DELETE NO ACTION
            )
            """
        )
        print("Successfully created TABLE Receive!")
    except connector.errors.DatabaseError as e:
        print("TABLE Receive already exists. Continue using the previous one.")
    cur.close()

def create_all(db):
    create_employees(db)
    create_messages(db)
    create_send(db)
    create_receive(db)
