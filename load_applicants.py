"""main file"""

import os
from os import path
from datetime import datetime
import csv
from typing import Tuple

from pymongo import MongoClient

from config import Config

# absolute path of this file
PATH = os.path.dirname(os.path.abspath(__file__))


def _split_name(name: str) -> Tuple[str, str]:
    """
    Split a name into two pieces--the first name, and everything that follows. If there are
    no spaces in the input name, the second element in the returned tuple will be the empty
    string.

    :param name: A person's name (e.g. "John Smith")
    :return: a 2-tuple with the person's first name as the first element, and everything
        else in the second element (e.g. tuple("John", "Smith"))
    """
    # split into two pieces at the first space
    names = name.split(" ", maxsplit=1)
    return names[0], names[1] if len(names) == 2 else ""


def load_applicants():
    """Create a csv in /csv with information on all users whose submitted applications haven't
    been evaluated.

    IMPORTANT: A user will be included in this csv if (a) they've submitted an application and
        (b) they haven't been accepted. For compatibility with our current Quill version, we
        have to delete rejected applicants from the database.

    CSV EXAMPLE:
        "abcdefgh","John","Smith","http://example.herokuapp.com/admin/users/abcdefgh"
        "ijklmnop","Jane","Doe","http://example.herokuapp.com/admin/users/ijklmnop"
    """
    # connect to the database and get the users collection
    client = MongoClient(Config.MONGODB_URI)
    db = client[Config.DB_NAME]
    users = db["users"]

    # create a nested csv directory, if it doesn't already exist
    os.makedirs(path.join(PATH, "csv"), exist_ok=True)

    csv_filename = path.join(PATH, "csv", f"applicants{datetime.now()}.csv")

    # create and populate the csv file
    with open(csv_filename, "w", newline="") as applicants_file:
        wr = csv.writer(applicants_file, quoting=csv.QUOTE_ALL)

        applicants = [user for user in users.find()
                      if user["status"]["completedProfile"] and not user["status"]["admitted"]]

        for applicant in applicants:
            applicant_id = applicant["_id"]
            first_name, last_name = _split_name(applicant["profile"]["name"])
            application_url = f"{Config.BASE_URL}/admin/users/{applicant_id}"

            # add user info to the csv file
            wr.writerow([applicant_id, first_name, last_name, application_url])

    print(f"File was created successfully in {PATH}/csv")


if __name__ == "__main__":
    load_applicants()
