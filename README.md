# ecommerce_api_django
This is a single vendor ecommerce api developed with Django(DRF) and a PostgreSQL database.

### Settings.py
The settings.py has been replaced with the files base.py, development.py, and production.py inside of the settings folder, i.e., the settings folder has the following files inside:
 - __init__.py
 - development.py
 - production.py
 - base.py
 - .env

Hence, each environment has a different settings configuration, but they all have the base.py file as base template.

The current setting file in use is specified in settings/__init__.py file.

Environment variables for development.py had been set in the .env file inside the settings folder using the django-environ package.


### Readme files

Inside the Readme folder of each app are the Readme-{some topic}.md files of the app.
