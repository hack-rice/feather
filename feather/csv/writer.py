import csv
from datetime import datetime
from os import path
from typing import Iterable
import logging

from feather.models import Evaluation, Applicant

LOGGER = logging.getLogger(__name__)


class CSVWriter:
    def __init__(self, outbox_path=path.dirname(path.abspath(__file__))):
        """
        Init a CSVWriter.
        :param outbox_path: the path to the directory where you want created files to
            be placed. Defaults to the current directory.
        """
        self.outbox_path = outbox_path

    def _write_to_csv(self, title: str, model_objects: Iterable, attr_list: Iterable[str]) -> None:
        """Write the input model objects to a csv in the outbox directory. Their
        data is obtained by calling the attributes listed in attr_list.

        :param title: the title of the file. (e.g. "applicants", "users", etc.) Do NOT
            add a file extension to this title.
        :param model_objects: an iterable of model objects.
        :param attr_list: an iterable of attributes of the model objects to be included
            in the csv. These attributes will also be the names of the columns in the
            output csv.
        """
        csv_filepath = path.join(self.outbox_path, f"{title}{datetime.now()}.csv")

        # create and populate the csv file
        with open(csv_filepath, "w", newline="") as file:
            wr = csv.writer(file, quoting=csv.QUOTE_ALL)

            # add column headers
            wr.writerow(attr_list)

            for obj in model_objects:
                try:
                    # add evaluation info to the csv file
                    wr.writerow(getattr(obj, attr) for attr in attr_list)
                except AttributeError as e:
                    # because we're getting model data via reflection, this error could
                    # happen very easily
                    # we don't want it to break the program
                    LOGGER.error("Given attribute was not found on the model object.")
                    LOGGER.error(f"Model object: {obj}.")
                    LOGGER.error(e)

        LOGGER.info(f"File was created successfully in {self.outbox_path}.")

    def write_evaluations_to_csv(self, title: str, evaluations: Iterable[Evaluation]) -> None:
        """Write the input evaluations to a csv in the outbox directory.

        EXAMPLE ENTRIES:
            "jsmith@mit.edu","John","waitlist"
            "jdoe@wustl.edu","Jane","accept"

        :param title: the title of the file. (e.g. "applicants", "users", etc.) Do NOT
            add a file extension to this title.
        :param evaluations: an iterable of Evaluation model objects.
        """
        attr_list = ["email", "first_name", "decision"]
        return self._write_to_csv(title, evaluations, attr_list)

    def write_applicants_to_csv(self, title: str, applicants: Iterable[Applicant]):
        """Write the input applicants to a csv in the outbox directory.

        EXAMPLE ENTRIES:
            "jsmith@mit.edu","John","Smith","http://example.herokuapp.com/admin/users/abcdefgh"
            "jdoe@wustl.edu","Jane","Doe","http://example.herokuapp.com/admin/users/ijklmnop"

        :param title: the title of the file. (e.g. "applicants", "users", etc.) Do NOT
            add a file extension to this title.
        :param applicants: an iterable of Evaluation model objects.
        """
        attr_list = ["email", "first_name", "last_name", "profile_link"]
        return self._write_to_csv(title, applicants, attr_list)
