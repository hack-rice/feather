
from pprint import pprint
from feather import QuillDao
from scripts.constants import Constants

if __name__ == "__main__":
    dao = QuillDao(Constants.MONGODB_URI, Constants.DB_NAME)
    email = input("User's email: ")
    try:
        pprint(dao.get_user_json(email))
    except TypeError:
        print("User not found!")
