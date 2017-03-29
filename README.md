# teknologr.io
Membership management system tailored for TF use

[![Build Status](https://travis-ci.org/Teknologforeningen/teknologr.io.svg?branch=develop)](https://travis-ci.org/Teknologforeningen/teknologr.io)  

## Installation

First make sure that you have Python 3 installed and virtualenv to go with it.

1. Create virtualenv: `virtualenv -p /usr/bin/python3 venv`
2. Activate venv: `source venv/bin/activate`
3. Install stuff with pip: `pip install -r requirements.txt`

## Code style
pep8 check will be done when doing `python manage.py test`.
Linting only can be run with `python manage.py test test_pep8`.
