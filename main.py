"""main file"""
import os
from datetime import datetime
import csv
from pprint import pprint
from pymongo import MongoClient

# absolute path of this file
PATH = os.path.dirname(os.path.abspath(__file__))


def load_applicants():
    # connect to the database
    MONGODB_URI = os.environ["MONGODB_URI"]
    DB_NAME = os.environ["DB_NAME"]
    BASE_URL = os.environ["BASE_URL"]

    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    users = db["users"]

    # create a csv directory, if not already there
    os.makedirs(f"{PATH}/csv", exist_ok=True)

    applicants = [user for user in users.find()
                  if user["status"]["completedProfile"] and not user["status"]["admitted"]]

    with open(f"{PATH}/csv/applicants{datetime.now()}.csv", "w", newline="") as applicants_file:
        wr = csv.writer(applicants_file, quoting=csv.QUOTE_ALL)

        for applicant in applicants:
            # get info for each applicant
            applicant_id = applicant["_id"]
            name = applicant["profile"]["name"]
            url = f"{BASE_URL}/admin/users/{applicant_id}"

            # add to the csv file
            wr.writerow([applicant_id, name, url])

    print(f"File was create successfully in {PATH}/csv")


if __name__ == "__main__":
    # load the environment variables
    from dotenv import load_dotenv
    load_dotenv(override=True)

    load_applicants()
