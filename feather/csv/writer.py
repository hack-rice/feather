import csv
from datetime import datetime
from os import path
from typing import Iterable
import logging

from constants import Constants
from feather.models import Evaluation, Applicant

LOGGER = logging.getLogger(__name__)


class CSVWriter:
    def __init__(self, outbox_path=path.dirname(path.abspath(__file__))):
        self.outbox_path = outbox_path

    def write_evaluations_to_csv(self, title: str, evaluations: Iterable[Evaluation]) -> None:
        """Write the input evaluations to a csv in the outbox directory.

        EXAMPLE ENTRIES:
            "jsmith@mit.edu","John","waitlist"
            "jdoe@wustl.edu","Jane","accept"

        :param title: the title of the file. (e.g. "applicants", "users", etc.) Do NOT
            add a file extension to this title.
        :param evaluations: an iterable of Evaluation model objects.
        """
        csv_filepath = path.join(self.outbox_path, f"{title}{datetime.now()}.csv")

        # create and populate the csv file
        with open(csv_filepath, "w", newline="") as evals_file:
            wr = csv.writer(evals_file, quoting=csv.QUOTE_ALL)

            # add column headers
            wr.writerow(["email", "first name", "decision"])

            for evaluation in evaluations:
                # add evaluation info to the csv file
                wr.writerow(
                    [evaluation.email, evaluation.first_name, evaluation.decision]
                )

        LOGGER.info(f"File was created successfully in {self.outbox_path}.")

    def write_applicants_to_csv(self, title: str, applicants: Iterable[Applicant]):
        """Write the input applicants to a csv in the outbox directory.

        EXAMPLE ENTRIES:
            "jsmith@mit.edu","John","Smith","http://example.herokuapp.com/admin/users/abcdefgh"
            "jdoe@wustl.edu","Jane","Doe","http://example.herokuapp.com/admin/users/ijklmnop"

        :param title: the title of the file. (e.g. "applicants", "users", etc.) Do NOT
            add a file extension to this title.
        :param applicants: an iterable of Evaluation model objects.
        """
        csv_filepath = path.join(self.outbox_path, f"{title}{datetime.now()}.csv")

        # create and populate the csv file
        with open(csv_filepath, "w", newline="") as users_file:
            writer = csv.writer(users_file, quoting=csv.QUOTE_ALL)

            # add column headers
            writer.writerow(["Email", "First Name", "Last Name", "Application Link"])

            for user in applicants:
                # this is how quill creates urls for each user
                application_url = f"{Constants.BASE_URL}/admin/users/{user.id}"

                # add user info to the csv file
                writer.writerow(
                    [user.email, user.first_name, user.last_name, application_url]
                )

        LOGGER.info(f"File was created successfully in {self.outbox_path}.")
