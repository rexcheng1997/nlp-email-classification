'''
    Retrieve the parsed files containing the key words from the folders.
'''

__author__ = "rexcheng"

import os

def fetch_files(employeeFolders):
    """
        Returns the employee folder names and their corresponding "mail.txt" in two lists.
    """
    employees = []
    filePaths = []
    for folder in employeeFolders:
        if "mail.txt" in os.listdir(folder):
            employees.append(os.path.split(folder)[1])
            filePaths.append(os.path.join(folder, "mail.txt"))
    return employees, filePaths

def read_file(file):
    """
        Read the content in file.
    """
    with open(file, 'r') as f:
        words = f.read()
    return words


if __name__ == "__main__":
    datasetDir = os.path.join(os.path.abspath('.'), "maildir")
    employeeFolders = [os.path.join(datasetDir, f) for f in os.listdir(datasetDir)]
    print(fetch_files(employeeFolders))
