# Models inside the ecommerce_backend app

#### Category Model

The category model registers the category of a product which will help for features such as filtering items (products), and so it has as a property the name of the category


#### Product Model

The product model initailly takes as parameters the title(name of product), price, category, discount price, image to show, and the description of itself. It is intended to be an abstract represntation of a general product, and so it can be further modified to adapt to a more particular scenario

#### Order Item Model

The objective of this model is to help the CRUD operations of the client's cart, and to help simplifying the __Order Model__. It manages the amount of a product in the __Cart__, and it is linked to the __User__ (can be **null** if user is not logged in).

It is automaticaly created when a user adds an item to the __Cart__



<span style="color: #03C588">Note: We shall call an __Order__ a __Cart__ if and only if the __Order__ has not been completed yet</span>

#### Order Model

This model manages the Order made by the user. It takes the list of products (__OrderItems__) from the __Cart__, the __User__ payment info such as shipping address and stripe account (in case those exist), the __Payment__ info (only after the payment takes place), and it has extra fields for checking the order status


#### The Payment Model

This handlers the payment made by the user, which can be anonymous.

#### Coupon and Refund

These models are to manage the store coupons and if a client ask to refund an __Order__

#### Address Model

The address model can be either a billing address or a shipping address. It is linked to the user whence the user is not **null**, and it can be set to default in each case
