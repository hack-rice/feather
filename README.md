# feather
> IN DEVELOPMENT: a minimalist python API for interacting with the quill registration tool

[![Build Status](https://travis-ci.com/hack-rice/feather.svg?branch=master)](https://travis-ci.com/hack-rice/feather)
[![codecov](https://codecov.io/gh/hack-rice/feather/branch/master/graph/badge.svg)](https://codecov.io/gh/hack-rice/feather)
[![Known Vulnerabilities](https://snyk.io//test/github/hack-rice/feather/badge.svg?targetFile=requirements.txt)](https://snyk.io//test/github/hack-rice/feather?targetFile=requirements.txt)

[Quill](https://github.com/techx/quill) is amazing. But it wasn't built for HackRice, and there 
are features we need that it just doesn't provide. Enter Feather.

We use Feather to streamline our application evaluation process, conduct email campaigns, 
and much more. See below for more details.

## API

More thorough documentation is in development. For now, go through the code.

## Scripts

### How to Get Started

This will cover how to run the scripts available in the package. First, go into the `scripts`
directory and copy-and-paste `example.env` into a `.env` file. Change the variables as
necessary to configure your project.

```
# start in the feather/ directory
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

### evaluate_applicants.py

This script will let you accept, reject, and waitlist applicants by uploading a csv with necessary
information on each applicant.

`python3 -m scripts.evaluate_applicants`

### load_applicants.py

This script will load a csv with necessary information on submitted users whose applications haven't
been evaluated yet.

`python3 -m scripts.load_applicants`


### send_reminders.py

This script will send emails to all of the registered users who haven't completed their application.

`python3 -m scripts.send_reminders`
