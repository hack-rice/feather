
from pprint import pprint
from feather import QuillDao
from scripts.constants import Constants

if __name__ == "__main__":
    dao = QuillDao(Constants.MONGODB_URI, Constants.DB_NAME)
    email = input("User's email: ")
    user_json = dao.get_user_json(email)

    if user_json:
        pprint(user_json)  # format ane print the dict
    else:
        print("User not found!")
