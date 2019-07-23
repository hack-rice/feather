"""Script that loads unevaluated applicants from the database and places them
in a csv file in the outbox directory.
"""
from feather.csv.writers import write_users_to_csv
from feather.quill_dao import QuillDao


if __name__ == "__main__":
    dao = QuillDao()
    write_users_to_csv("applicants", dao.get_unevaluated_applicants())
