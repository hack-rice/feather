"""File that contains the evaluate_applicants function."""
import os
from os import path
import csv
from typing import Set
from collections import namedtuple
from datetime import datetime

from pymongo import MongoClient

from config import Config

# absolute path of this file
PATH = path.dirname(path.abspath(__file__))


Applicant = namedtuple("Applicant", "email first_name decision")


def evaluate_applicants(csv_filename: str) -> Set[Applicant]:
    # connect to the database and get the users collection
    client = MongoClient(Config.MONGODB_URI)
    db = client[Config.DB_NAME]
    users = db["users"]

    # connect to (or create) collection for rejected applicants
    rejected_users = db["rejected_users"]

    # create a set for applicants whose decisions couldn't be parsed
    unevaluated_applicants = set()

    with open(csv_filename, "r") as applicants_file:
        reader = csv.DictReader(applicants_file)

        for applicant in reader:
            if applicant["decision"] == "reject":
                # move their info to the rejected_users collection
                profile = users.find_one_and_delete({"email": applicant["email"]})
                rejected_users.insert_one(profile)

            elif applicant["decision"] == "accept":
                users.find_one_and_update(
                    {"email": applicant["email"]},
                    {"$set": {
                        "admitted": True,
                        "admittedBy": Config.EMAIL
                    }})

            elif applicant["decision"] == "waitlist":
                # do nothing
                pass

            else:
                unevaluated_applicants.add(
                    Applicant(
                        applicant["email"],
                        applicant["first name"],
                        applicant["decision"]
                    )
                )

    return unevaluated_applicants


def write_applicants_to_csv(applicants: Set[Applicant]) -> None:
    # create a nested csv directory, if it doesn't already exist
    os.makedirs(path.join(PATH, "outbox"), exist_ok=True)

    csv_filename = path.join(PATH, "outbox", f"unevaluated_applicants{datetime.now()}.csv")

    # create and populate the csv file
    with open(csv_filename, "w", newline="") as applicants_file:
        wr = csv.writer(applicants_file, quoting=csv.QUOTE_ALL)

        # add column headers
        wr.writerow(["email", "first name", "decision"])

        for applicant in applicants:
            wr.writerow([applicant.email, applicant.first_name, applicant.decision])

    print(f"\n\tFile was created successfully in {PATH}/outbox")


def _main():
    input_message = """
    Please input the name of the csv in inbox (e.g. evals.csv).
    Remember that this file MUST have email, first name, and
    decision columns. Of course, email must be a valid email
    address, and decision must be either accept, reject, or
    waitlist.
    
    Filename: """
    filename = input(input_message)
    filepath = path.join(PATH, "inbox", filename)

    unevaluated_applicants = evaluate_applicants(filepath)

    if unevaluated_applicants:
        write_applicants_to_csv(unevaluated_applicants)


if __name__ == "__main__":
    _main()
