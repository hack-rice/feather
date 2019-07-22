"""File that contains the evaluate_applicants function."""
from queue import Queue

from feather.csv.readers import read_evaluations
from feather.csv.writers import write_evaluations_to_csv
from feather.email.email_daemon import EmailDaemon
from feather.evaluate_daemon import EvaluateDaemon


def _main() -> None:
    """Main function. (1) Asks the user for the name of a csv that contains applicant
    decisions. (2) Evaluates the applicants accordingly. (3) If there are any
    applicants whose decisions couldn't be parsed, create a new csv with only their
    information.
    """
    # get the csv file from user and read it
    file_message = """
    Please input the name of the csv in inbox (e.g. evals.csv).
    Remember that this file MUST have email, first name, and
    decision columns. Of course, email must be a valid email
    address, and decision must be either accept, reject, or
    waitlist.

    Filename: """
    filename = input(file_message)

    # make sure they actually want to do this
    followup_message = """
    Are you SURE that you want to do this? Running this script
    will update the applicants' profiles in the database and
    email them with their decisions. 
    
    Proceed? (y/n): """
    response = input(followup_message)
    if response != "y":
        return

    evaluations = read_evaluations(filename)

    message_queue = Queue()  # queue for the daemons to communicate
    consumer = EmailDaemon(message_queue)
    producer = EvaluateDaemon(evaluations, message_queue)

    # start the daemons
    consumer.start()
    producer.start()

    # wait for evaluations to finish
    producer.join()

    if producer.unparsed_evaluations:
        write_evaluations_to_csv("unparsed_evals", producer.unparsed_evaluations)

    # wait for emails to finish sending
    consumer.join()


if __name__ == "__main__":
    _main()
