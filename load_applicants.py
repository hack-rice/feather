"""File that contains the load_applicants function."""

from utils.csv.writers import write_users_to_csv
from utils.quill_dao import QuillDao


if __name__ == "__main__":
    dao = QuillDao()
    write_users_to_csv("applicants", dao.get_unevaluated_applicants())
