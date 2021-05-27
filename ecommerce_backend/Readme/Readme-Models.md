# Models inside the ecommerce_backend app

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
