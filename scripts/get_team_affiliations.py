from feather import QuillDao
from scripts.constants import Constants


def _main():
    dao = QuillDao(Constants.MONGODB_URI, Constants.DB_NAME)
    teams = dao.get_teams()
    for team in teams:
        print(team)
        for member in teams[team]:
            print(f"\t{member}")


if __name__ == "__main__":
    _main()
