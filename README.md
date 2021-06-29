# Single Vendor Ecommerce Django (API)
This is a single vendor ecommerce api developed with Django(DRF) and a PostgreSQL database.

#### Table of Contents
* [Overview](#overview)
* [Features](#features)
* [Settings.py](#settings)
* [Readme Files](#readme)
* [Project Apps](#projectApps)
* [Run the Project](#run)


## <a name="overview"></a> Overview

This project is intended as an abstract template for any _Single Vendor Ecommerce Website_, and so it is divided in three different apps, one that manages user account's creation and updating, the second that manages the store sales and payments, and the third app that is only available for the store owner (Admin User) to have control over the store and users

## <a name="features"></a> Features

#### User account management features:
- User Account's Activation functionality via email (the url sent to the user email gets invalid after it is accessed from the browser for the first time)
- Password Reset functionality is implemented with same method as User Account's Activation
- The User can save payment info such as
  -  _Stripe account info_ and
  -  _Default billing/shipping address_
  to make automatic payments without the need of entering any data during checkout.
- The User can
  - Update both personal and payment information,
  - See payment and order history and ask for refund, and
  - Have multiple billing and shipping addresses

#### Store sales features:
- The customer can
  - Be either a logged user or an anonymous user (all features are available for both except user account management functionalities),
  - Filter products by category and/or filter by giving a keyword or any keyword substring,
  - View the details and set the amount of the product before add it to the cart
- Cart functionalities such as _Add item_, _Modify amount of item_, _Delete item_, and _Delete cart_ are available

- Customer is always given the option to change the payment info during __checkout__ (previous to make the payment). The user can change the default _billing/shipping_ address to any other address created previous the checkout or else can choose to create a new one
- Payments are handled via __stripe__. Anonymous users can also make a purchase
- Refunds can be asked for any completed (already paid) order

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

Inside the __Readme__ folder of each app are the __Readme-{some topic}.md__ files of the app for explaining models, views, serializers, ... only when considered required.

## <a name="projectApps"></a> Project Apps

- The __ecommerce_backend__ manages the client iteration with the products of the store, i.e., view a product, add it to the cart, buy it, apply for refund and coupons. It also handles all related to payments and store services.

- The __eccommerce_accounts_app__ manages the user-client operations such as login/out, sign up and edit user credentials and data of the user account and also view its orders. This also manages the admin (store owner) account and allows it to make CRUD operations over the products (and models as Category, Coupons, Orders, Refunds, ...) of the store.

- The __ecommerce_administration_app__ acts like a _User Management System_ for the store, so the _Admin User_ can access and modify/create data such as _products_, _orders_, ... . It also displays some statistics from the sales as  _yearly_, _monthly_, and _weekly_ and keeps the record of the _Users_ and _Payments_

## <a name="run"></a> Run the Project

Steps for running the project locally:
1. Install python3.8 and pip3
1. Install postgreSQL and create database
3. Install packages from __requirements.txt__
4. Create virtualenv
5. Create __.env__ file and add the variables specified in the __Settings.py File Section__
6. Run the migrations
7. Run server
