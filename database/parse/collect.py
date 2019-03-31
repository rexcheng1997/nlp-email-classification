'''
    Collect all the emails in Enron dataset from "maildir" directory.
    Insert the important information in the emails into the database.
'''

__author__ = "rexcheng"

import sys, os, re, json
from . import nlp_wrapper as nlp
from ..insert_data import *

regex = re.compile(r'^.*?Date: (.*?)\*\-\*From: (.*?)\*\-\*T?o?:? ?(.*?)\*?\-?\*?Subject: .*?X-To: (.*?)\*\-\*.*?FileName: .*?\*\-\*(.*)$')
pick = re.compile(r'^.*?<\.(.*?)>$')
special = re.compile(r'^.*?Cc: (.*?)\*\-\*.*$')

def process_content(content):
    """
        Process the content and pick out any verbs and nouns that may be important.

        Arguments:
            - content: a string of message
    """
    Processor = nlp.StanfordNLP()
    try:
        result = Processor.pos(content)
        words = [w[0] for w in result if (len(w[0]) > 2 and len(w[0]) < 21) and ("VB" in w[1] or "NN" in w[1])]
    except json.decoder.JSONDecodeError as e:
        words = content.split(' ')
    return words

def insert_database(db, info):
    """
        Insert info into the database.

        Arguments:
            - db: database
            - info: a dictionary of information, e.g.
                    {
                        "date": 'Wed, 13 Dec 2000 07:04:00 -0800 (PST)',
                        "sender": 'phillip.allen@enron.com',
                        "receiver": ['christi.nicolay@enron.com', ...],
                        "body": 'Attached are two files ...'
                    }
    """
    eid = insert_employee(db, info["sender"])
    mid = insert_message(db, info["body"])
    for receiver in info["receiver"]:
        rid = insert_employee(db, receiver)
        insert_receive(db, mid, rid)
    insert_send(db, mid, eid, info["date"])

def parse_mail(email, db):
    """
        Parse the information in the emails using regualr expression.

        Arguments:
            - email: raw content of an email
            - db: database
    """
    m = regex.match(email)
    try:
        date, sender, receiver, backup, body = m.group(1), m.group(2), m.group(3).replace("*-*", '').split(", "), m.group(4).split(", "), m.group(5)
        if receiver[0] == '' and backup[0] != '':
            receiver = backup
        elif receiver[0] == '' and backup[0] == '':
            mm = special.match(email)
            if mm == None:
                receiver = []
            else:
                receiver = mm.group(1).split(", ")
    except AttributeError as e:
        db.close()
        print("Regular expression can't match anything. Some formatting issues in the raw emails occurred!")
        print("The email that caused the error:", email)
        print("Error code:", e)
        exit(1)

    contentList = [x.replace("   ", '') for x in body.split("*-*") if x != '']
    # content is what we feed into the NLP process.
    content = ' '.join(contentList).replace("  ", ' ')
    # msg is the well-formatted body message of the emails, which will be stored in the database.
    msg = '\n'.join(contentList).replace("  ", ' ')

    # Make the employees' email addresses look more pretty.
    zombies = []
    for i in range(len(receiver)):
        if receiver[i] == '':
            zombies.append(receiver[i])
            continue
        if receiver[i][-1] == '>':
            try:
                receiver[i] = pick.match(receiver[i]).group(1)
            except AttributeError as e:
                zombies.append(receiver[i])
        elif receiver[i][-1] == '\'':
            receiver[i] = receiver[i].replace('\'', '')
    for z in zombies:
        receiver.remove(z)

    # Insert the information into the database.
    insert_database(db, {
        "date": date,
        "sender": sender,
        "receiver": receiver,
        "body": msg
    })

    return process_content(content)

def filter_emails(db):
    """
        Retrieve all the emails from the dataset.

        Arguments:
            - db: database
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
        elif "sent_items" in os.listdir(pathToFolder):
            emailFolder = os.path.join(pathToFolder, "sent_items")
        elif "inbox" in os.listdir(pathToFolder):
            emailFolder = os.path.join(pathToFolder, "inbox")
        else:
            continue
        emails = [x for x in map(
            lambda f: os.path.join(emailFolder, f),
            os.listdir(emailFolder)
            )
            if os.path.isfile(x)
        ]
        # Words to be written into the txt file.
        words = []
        for email in emails:
            with open(email, 'r') as f:
                try:
                    words += parse_mail(f.read().replace('\\', ' ').replace('\n', "*-*").replace('\t', "*-*"), db)
                except:
                    pass
        # Write words to a csv file.
        with open(os.path.join(pathToFolder, "mail.txt"), 'w') as f:
            for word in words:
                try:
                    f.write(word + ' ')
                except:
                    pass
            print("Wrote to file", os.path.join(pathToFolder, "mail.txt"))

    return employeeFolders
