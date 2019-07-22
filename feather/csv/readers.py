import csv
from typing import Iterator
from os import path

from config import Config
from feather.models import Evaluation


def read_evaluations(csv_filename: str) -> Iterator[Evaluation]:
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
    filepath = path.join(Config.INBOX_PATH, csv_filename)

    with open(filepath, "r") as evaluations_file:
        reader = csv.DictReader(evaluations_file)
        for row in reader:
            yield Evaluation(
                row["email"],
                row["first name"],
                row["decision"]
            )