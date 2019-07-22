# feather
> IN DEVELOPMENT: a minimalist python API for interacting with the quill registration tool

[Quill](https://github.com/techx/quill) is amazing. But it wasn't built for HackRice, and there 
are features we need that it just doesn't provide. Enter Feather.

We use Feather to streamline our application evaluation process, conduct email campaigns, 
and much more. See below for more details.

## How to get it started

This all assumes that you have a running version of [Quill](https://github.com/techx/quill) 
_somewhere_, as that's kind of the point. You'll also need to copy and paste the `example.env`
file into your own `.env` file in the same directory, changing the environment variables as
necessary.

Note that `MONGODB_URI` and `DB_NAME` refer to the database quill uses on its backend. If you
deployed quill with heroku, you can find some of this info in the generated Config Vars and the
rest by digging around in mLab.

## evaluate.py

This script will let you accept, reject, and waitlist applicants by uploading a csv with necessary
information on each applicant.

## load_applicants.py

This script will load a csv with necessary information on submitted users whose applications haven't
been evaluated yet.
