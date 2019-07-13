"""File that contains the evaluate_applicants function."""
import os
from os import path
import csv
from collections import namedtuple

from pymongo import MongoClient

from config import Config

# absolute path of this file
PATH = os.path.dirname(os.path.abspath(__file__))


Applicant = namedtuple("Applicant", "email first_name decision")


def evaluate_applicants(csv_filename: str) -> None:
    # connect to the database and get the users collection
    client = MongoClient(Config.MONGODB_URI)
    db = client[Config.DB_NAME]
    users = db["users_test"]

    # connect to (or create) collection for rejected applicants
    rejected_users = db["rejected_users"]

    with open(csv_filename, "r") as applicants_file:
        reader = csv.DictReader(applicants_file)

        for applicant in reader:
            if applicant["decision"] == "reject":
                profile = users.find_one_and_delete({"email": applicant["email"]})
                rejected_users.insert_one(profile)

            if applicant["decision"] == "accept":
                users.find_one_and_update()


if __name__ == "__main__":
    input_message = """
    Please input the name of the csv in inbox (e.g. evals.csv).
    Remember that this file MUST have email, first name, and
    decision columns. Of course, email must be a valid email
    address and decision must be either accept, reject, or
    waitlist.
    
    Filename: """
    filename = input(input_message)
    filepath = path.join(PATH, "inbox", filename)

    evaluate_applicants(filepath)
