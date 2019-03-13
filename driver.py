'''
    Driver program.
'''

from database import login_server, create_database
from database.create_tables import create_all
from database.drop_tables import drop_all

# Login the mysql server.
usr, pwd, enron = login_server()

# Create Enron database.
enron = create_database(usr, pwd, enron)

# Create all the tables needed.
create_all(enron)

# filter_emails(enron)

# Uncomment the following line if you want to drop all the tables.
# drop_all(enron)
enron.close()