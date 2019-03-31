'''
    Driver program.
'''

__author__ = "rexcheng"

import pandas
import mysql.connector as connector
from database import login_server, create_database
from database.create_tables import create_all
from database.drop_tables import drop_all
from database.parse.collect import filter_emails
from machine_learning.analyze import analyze
import machine_learning as ml


try:
    # Login the mysql server.
    usr, pwd, enron = login_server()
except connector.errors.ProgrammingError as e:
    print(e);
    print("Username or password is wrong!")
    exit(1)

# Create Enron database.
enron = create_database(usr, pwd, enron)

# Uncomment the following line if you want to drop all the tables.
# drop_all(enron)

# Create all the tables needed.
create_all(enron)

# Fetch and process all the emails.
employeeFolders = filter_emails(enron)

# Fetch file paths for "mail.txt".
# employees, files = ml.fetch_files(employeeFolders)

# Create pandas DataFrame for the machine learning data.
# mlDF = pandas.DataFrame(data={
#     "employee": employees,
#     "words": list(map(ml.read_file, files))
# })

# analyze(mlDF)

enron.close()
