'''
    Driver program.
'''

__author__ = "rexcheng"

import pandas
from database import login_server, create_database
from database.create_tables import create_all
from database.drop_tables import drop_all
from database.parse.collect import filter_emails
from machine_learning.analyze import analyze
import machine_learning as ml


# Login the mysql server.
usr, pwd, enron = login_server()

# Create Enron database.
enron = create_database(usr, pwd, enron)

# Uncomment the following line if you want to drop all the tables.
drop_all(enron)

# Create all the tables needed.
create_all(enron)

# Fetch and process all the emails.
employeeFolders = filter_emails(enron)

# import os
# datasetDir = os.path.join(os.path.abspath('.'), "maildir")
# employeeFolders = [os.path.join(datasetDir, f) for f in os.listdir(datasetDir)]

# Fetch file paths for "mail.txt".
# employees, files = ml.fetch_files(employeeFolders)

# Create pandas DataFrame for the machine learning data.
# mlDF = pandas.DataFrame(data={
#     "employee": employees,
#     "words": list(map(ml.read_file, files))
# })

# analyze(mlDF)

enron.close()
