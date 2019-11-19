"""Script that creates a csv with information for each user that attended."""
from feather.csv import CSVWriter
from feather import QuillDao
from scripts.constants import Constants
import datetime


def _main():
    dao = QuillDao(Constants.MONGODB_URI, Constants.DB_NAME)
    writer = CSVWriter(Constants.OUTBOX_PATH)

    writer.write_attendees_to_csv(
        f"ApplicantReport {datetime.datetime.now()}",
        dao.get_attendees()
    )


if __name__ == "__main__":
    _main()
