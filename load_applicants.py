"""Script that loads unevaluated applicants from the database and places them
in a csv file in the outbox directory.
"""
from feather import QuillDao
from feather.csv import write_applicants_to_csv


if __name__ == "__main__":
    dao = QuillDao()
    write_applicants_to_csv("applicants", dao.get_applicants())
