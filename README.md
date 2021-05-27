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

### Project Apps

- The ecommerce_backend manages the client iteration with the products of the store, i.e., view a product, add it to the cart, buy it, apply for refund and coupons. It also handles all related to payments and store services.

- The eccommerce_accounts_app manages the user-client operations such as login/out, sign up and edit user credentials and data of the user account and also view its orders. This also manages the admin (store owner) account and allows it to make CRUD operations over the products (and models as Category, Coupons, Orders, Refunds, ...) of the store.
