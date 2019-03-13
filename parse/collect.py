'''
    Collect all the emails in Enron dataset from "maildir" directory.
    Insert the important information in the emails into the database.
'''

__author__ = "rexcheng"

import sys, os, re
from . import nlp_wrapper as nlp

regex = re.compile(r'^[\w\d\.\s\:\-\*<>@]+?Date: ([\w\d\s\,\:\-()]+?)\*\-\*.*?X-From: (.*?)\*\-\*X-To: (.*?)\*\-\*.*?FileName: (.*)$')

def process_content(content):
    """
        Process the content and pick out any verbs and nouns that may be important.

        Arguments:
            - content: a string of message
    """
    Processor = nlp.StanfordNLP()
    result = Processor.pos(content)
    words = [w[0] for w in result if (len(w[0]) > 1 and len(w[0]) < 21) and ("VB" in w[1] or "NN" in w[1])]
    return words

def insert_database(db, info):
    """
        Insert info into the database.

        Arguments:
            - db: database
            - info: a dictionary of information, e.g.
                    {
                        "date": 'Wed, 13 Dec 2000 07:04:00 -0800 (PST)',
                        "sender": 'Phillip K Allen',
                        "receiver": ['Christi L Nicolay', ...],
                        "body": 'Attached are two files ...'
                    }
    """
    print(info)

def parse_mail(email, db):
    """
        Parse the information in the emails using regualr expression.

        Arguments:
            - email: raw content of an email
            - db: database
    """
    m = regex.match(email)
    try:
        date, sender, receiver, body = m.group(1), m.group(2), m.group(3), m.group(4)
    except AttributeError as e:
        db.close()
        print("Regular expression can't match anything. Some formatting issues in the raw emails occurred!")
        print("The email that caused the error:", email)
        print("Error code: ", e)
        exit()

    contentList = [x.replace("   ", '') for x in body.split("*-*") if x != ''][1:]
    # msg is the well-formatted body message of the emails, which will be stored in the database.
    msg = '\n'.join(contentList).replace("  ", ' ')
    # Insert the information into the database.
    insert_database(db, {
        "date": date,
        "sender": sender,
        "receiver": receiver,
        "body": msg
    })
    # content is what we feed into the NLP process.
    content = ' '.join(contentList).replace("  ", ' ')
    words = process_content(content)
    return words

def filter_emails(db):
    """
        Retrieve all the emails from the dataset.
    """
    # Get the absolute path for the current directory.
    currentDir = os.path.abspath('.')
    # Join the daataset folder to the path of the current directory.
    datasetDir = os.path.join(currentDir, "maildir")
    # Get all the folders in the dataset.
    employeeFolders = [os.path.join(datasetDir, f) for f in os.listdir(datasetDir)]
    # For each employee, fetch all his/her emails.
    for pathToFolder in employeeFolders:
        if "sent" in os.listdir(pathToFolder):
            emailFolder = os.path.join(pathToFolder, "sent")
        elif "_sent_mail" in os.listdir(pathToFolder):
            emailFolder = os.path.join(pathToFolder, "_sent_mail")
        else:
            continue
        emails = [x for x in map(
            lambda f: os.path.join(emailFolder, f),
            os.listdir(emailFolder)
            )
            if os.path.isfile(x)
        ]
        # Words to be written into the csv file.
        words = []
        for email in emails:
            with open(email, 'r') as f:
                words = words + parse_mail(f.read().replace('\\', ' ').replace('\n', "*-*"), db)
        # Write words to a csv file.
        # with open(os.path.join(pathToFolder, "mail.csv"), 'w') as f:
        #     f.write(", ".join(words))

    return employeeFolders
