import csv
from typing import Iterator
from os import path

from feather.models import Evaluation


class CSVReader:
    def __init__(self, inbox_path=path.dirname(path.abspath(__file__))):
        """
        Init a CSVReader.
        :param inbox_path: the path to the directory of the files you want read.
            Defaults to the current directory.
        """
        self.inbox_path = inbox_path

    def read_evaluated_users(self, csv_filename: str) -> Iterator[Evaluation]:
        """Read evaluations from a csv file and return an iterator of Evaluation
        model objects. Note: this function assumes that the csv file has email,
        first name, and decision columns. These are case sensitive.

        Inspired by Anthony Fox:
            https://medium.com/anthony-fox/parsing-large-csv-files-with-python-854ab8f398ad

        :param csv_filename: name of the csv file of evaluations. Must be located
            in the inbox directory.
        :return: a generator of Evaluation objects.
        """
        # configure file path
        filepath = path.join(self.inbox_path, csv_filename)

        with open(filepath, "r") as evaluations_file:
            reader = csv.DictReader(evaluations_file)
            for row in reader:
                yield Evaluation(
                    row["email"],
                    row["first_name"],
                    row["decision"]
                )
