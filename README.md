# SMW
Simple Monograph Workflow

# Context
SMW is an Open Source application designed to assist with the Monograph publishing life cycle. Stages include:

- optional proposal
- submission
- internal review
- peer review
- copy editing
- production
- publication

# Technology
SMW is written in Python using the Django Web Application framework and follows a MTV (that is, “model”, “template”, and “view.”) style. The template system is simple, easy to modify and uses Twitter Bootstrap 3.

# Development
If you want to hack on SMW, getting it set up is easy. You'll need a *nix machine (you can set it up on Windows if you're super hard core). We recommend you use [VirtualEnvironment](https://virtualenv.pypa.io/en/latest/) with [VirtualEnvWrapper](https://virtualenvwrapper.readthedocs.org/en/latest/). Once these are installed, clone the repo with:

	$ git clone https://github.com/ajrbyers/smw.git 

Make a virtual environment:

	$ mkvirtualenv smw

And install the requirements (requirements.txt is found in the root folder of the repo):

	$ pip install -r requirements.txt

This will install a small number of requirements including Django. By default the program uses SQLite in development but for production it's recommended you make use of MySQL or Postgresql.

Sync and migrate the SQLite DB (from the src folder):

	$ python manage.py syncdb
	$ python manage.py migrate

To start hacking run (from the src folder):
	
	$ python manage.py runserver

You'll now be able to access the server from http://localhost:8000

# Credit
Originally started by a team of volunteer developers, this project is now supported by [Ubiquity Press](http://ubiquitypress.com/).

Core developers:

- Andy Byers
- Mauro Sanchez
- Paige MacKay
