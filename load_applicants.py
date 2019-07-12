"""main file"""

import os
from datetime import datetime
import csv

from pymongo import MongoClient

from config import Config

# absolute path of this file
PATH = os.path.dirname(os.path.abspath(__file__))


def load_applicants():
    """Create a csv in /csv with information on all users whose submitted applications haven't
    been evaluated.

    IMPORTANT: A user would be included in this csv if (a) they've submitted an application and
        (b) they haven't been accepted. For compatibility with Quill, we have to delete
        rejected applicants from the database, so this operation should work.

    CSV EXAMPLE:
        "abcdefgh","John Smith","http://example.herokuapp.com/admin/users/abcdefgh"
        "ijklmnop","Jane Doe","http://example.herokuapp.com/admin/users/ijklmnop"
    """
    # connect to the database and get the users collection
    client = MongoClient(Config.MONGODB_URI)
    db = client[Config.DB_NAME]
    users = db["users"]

    # create a csv directory, if it doesn't already exist
    os.makedirs(f"{PATH}/csv", exist_ok=True)

    applicants = [user for user in users.find()
                  if user["status"]["completedProfile"] and not user["status"]["admitted"]]

    # create and populate the csv file
    with open(f"{PATH}/csv/applicants{datetime.now()}.csv", "w", newline="") as applicants_file:
        wr = csv.writer(applicants_file, quoting=csv.QUOTE_ALL)

        for applicant in applicants:
            applicant_id = applicant["_id"]
            name = applicant["profile"]["name"]
            url = f"{Config.BASE_URL}/admin/users/{applicant_id}"

            # add user info to the csv file
            wr.writerow([applicant_id, name, url])

    print(f"File was created successfully in {PATH}/csv")


if __name__ == "__main__":
    load_applicants()
