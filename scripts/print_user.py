
from pprint import pprint
from feather import QuillDao
from scripts.constants import Constants

if __name__ == "__main__":
    dao = QuillDao(Constants.MONGODB_URI, Constants.DB_NAME)
    email = input("User's email: ")
    try:
        pprint(dao.get_user_json(email))  # format ane print the dict
    except ValueError:  # the dao throws this when a user isn't found
        print("User not found!")
