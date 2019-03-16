'''
    Alter the columns of a table.
'''

__author__ = "rexcheng"

import mysql.connector as connector

def alter_sequence(db, table, value):
    cur = db.cursor()
    sql = "ALTER TABLE " + table + " AUTO_INCREMENT = %s"
    cur.execute(sql, (value, ))
    cur.close()
