# ecommerce_api_django
This is a single vendor ecommerce api developed with Django(DRF) and a PostgreSQL database.

#### Table of Contents
* [Settings.py](#settings)
* [Readme Files](#readme)
* [Project Apps](#projectApps)


## <a name="settings"></a> Settings.py

The settings.py has been replaced with the files __base.py__, __development.py__, and __production.py__ inside of the settings folder, i.e., the settings folder has the following files inside:
 - \_\_init__.py
 - development.py
 - production.py
 - base.py
 - .env

Hence, each environment has a different settings configuration, but they all have the __base.py__ file as base template.

The current setting file in use is specified in settings/__\_\_init\_\___.py file.

Environment variables for __development.py__ had been set in the __.env__ file inside the settings folder using the django-environ package.

The __.env__ file should contain the following variables:

- SECRET_KEY
- DATABASE_NAME
- DATABASE_USER
- DATABASE_PASSWORD
- DATABASE_HOST
- DATABASE_PORT
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD
- STRIPE_PUBLIC_KEY
- STRIPE_SECRET_KEY

The default authentication method used is __knox tokens authentication__.


## <a name="readme"></a> Readme Files

Inside the __Readme__ folder of each app are the Readme-{some topic}.md files of the app.

## <a name="projectApps"></a> Project Apps

- The __ecommerce_backend__ manages the client iteration with the products of the store, i.e., view a product, add it to the cart, buy it, apply for refund and coupons. It also handles all related to payments and store services.

- The __eccommerce_accounts_app__ manages the user-client operations such as login/out, sign up and edit user credentials and data of the user account and also view its orders. This also manages the admin (store owner) account and allows it to make CRUD operations over the products (and models as Category, Coupons, Orders, Refunds, ...) of the store.
