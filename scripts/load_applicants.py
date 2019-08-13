"""Script that loads unevaluated applicants from the database and places them
in a csv file in the outbox directory.
"""
from scripts.constants import Constants
from feather import QuillDao
from feather.csv import CSVWriter


if __name__ == "__main__":
    dao = QuillDao(Constants.MONGODB_URI, Constants.DB_NAME)
    writer = CSVWriter(Constants.OUTBOX_PATH)
    writer.write_applicants_to_csv("applicants", dao.get_applicants(Constants.BASE_URL))
