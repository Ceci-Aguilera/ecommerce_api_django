# Models inside the ecommerce_backend app

### User Model

This user model is a custom model from the default one. It manages both clients and admin (in this case the single vendor user). Hence it has the following extra fields:
- Stripe id (in order to process payments)
- Addresses (billing and/or shipping which are both optional)
- On click purchasing if user can purchase without giving extra data
- Phone number
- First and Last Name (always required)

Note that the user's main credential is set to be the email address

The fields related to __uid__ and __token__ are necessary for resetting password and user's account authentication when register. They are generated in the tokens.py file

The __is_active__ prop is only set to __True__ ones the user has been authenticated.

This app does NOT use the default authentication method of DRF neither the allauth's one. Instead, the authentication method is manually configured and uses the email address of the client and the __uid__ and __token__ four properties of the user model.

### Category Model

The category model registers the category of a product which will help for features such as filtering items (products), and so it has as a property the name of the category


### Product Model

The product model takes as parameters the title, price, category, discount price, image to show, and the description of itself

### Order Item Model

The objective of this model is to help the CRUD operations of the client's cart, and to help simplifying the Order Model. It manages the amount of a product in the Cart, and it is linked to the user (can be **null** if user is not logged in) and the product.

It is created when a user adds an item to the Cart


### Order Model

This model manages the Order made by the user. It takes the products from the Cart, the User personal info such as shipping address, the Payment info, and it adds the extra fields for checking the order status


### The Payment Model

This handlers the payment and the user's payment info

### Coupon and Refund

These models are to manage the store coupons and if a client ask for refund an order

### Address Model

The address model can be either a billing address or a shipping address. It is linked to the user whence the user is not **null**
