"""File that contains the load_applicants function."""

from os import path
from datetime import datetime
import csv

from config import Config
from quill_dao import QuillDao


def _main() -> None:
    """Create a csv in the outbox directory with information on all users whose submitted
    applications haven't been evaluated.

    IMPORTANT: A user will be included in this csv if (a) they've submitted an application and
        (b) they haven't been accepted. For compatibility with our current Quill version, we
        have to delete rejected applicants from the users collection.

    EXAMPLE ENTRIES:
        "jsmith@mit.edu","John","Smith","http://example.herokuapp.com/admin/users/abcdefgh"
        "jdoe@wustl.edu","Jane","Doe","http://example.herokuapp.com/admin/users/ijklmnop"
    """
    # connect to the database and get the users collection
    dao = QuillDao()

    csv_filename = path.join(Config.OUTBOX_PATH, f"applicants{datetime.now()}.csv")

    # create and populate the csv file
    with open(csv_filename, "w", newline="") as applicants_file:
        wr = csv.writer(applicants_file, quoting=csv.QUOTE_ALL)

        # add column headers
        wr.writerow(["Email", "First Name", "Last Name", "Application Link"])

        for applicant in dao.get_unevaluated_applicants():
            # this is how quill creates urls for each user
            application_url = f"{Config.BASE_URL}/admin/users/{applicant.id}"

            # add user info to the csv file
            wr.writerow(
                [applicant.email, applicant.first_name, applicant.last_name, application_url]
            )

    print(f"File was created successfully in {Config.OUTBOX_PATH}")


if __name__ == "__main__":
    _main()
