import csv
from datetime import datetime
from os import path
from typing import Set

from config import Config
from utils.models import Evaluation


def write_evaluations_to_csv(title: str, evaluations: Set[Evaluation]) -> None:
    csv_filename = path.join(Config.OUTBOX_PATH, f"{title}{datetime.now()}.csv")

    # create and populate the csv file
    with open(csv_filename, "w", newline="") as evals_file:
        wr = csv.writer(evals_file, quoting=csv.QUOTE_ALL)

        # add column headers
        wr.writerow(["email", "first name", "decision"])

        for evaluation in evaluations:
            wr.writerow(
                [evaluation.email, evaluation.first_name, evaluation.decision]
            )

    print(f"\n\tFile was created successfully in {Config.OUTBOX_PATH}")


def write_users_to_csv(title: str, users):
    """Create a csv in the outbox directory with information on all users whose submitted
    applications haven't been evaluated.

    EXAMPLE ENTRIES:
        "jsmith@mit.edu","John","Smith","http://example.herokuapp.com/admin/users/abcdefgh"
        "jdoe@wustl.edu","Jane","Doe","http://example.herokuapp.com/admin/users/ijklmnop"
    """
    csv_filename = path.join(Config.OUTBOX_PATH, f"{title}{datetime.now()}.csv")

    # create and populate the csv file
    with open(csv_filename, "w", newline="") as users_file:
        writer = csv.writer(users_file, quoting=csv.QUOTE_ALL)

        # add column headers
        writer.writerow(["Email", "First Name", "Last Name", "Application Link"])

        for user in users:
            # this is how quill creates urls for each user
            application_url = f"{Config.BASE_URL}/admin/users/{user.id}"

            # add user info to the csv file
            writer.writerow(
                [user.email, user.first_name, user.last_name, application_url]
            )

    print(f"File was created successfully in {Config.OUTBOX_PATH}")