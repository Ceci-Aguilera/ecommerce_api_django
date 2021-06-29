# Views inside the ecommerce_backend app

### add_to_cart:

This is the only non-class based view. It simply adds a new amount of a product to the cart. If the cart is empty, then it creates a new Order (Cart in this case).


### AllProductsView, ProductsFromCategory:

This views takes as parameters a Category (__ProductsFromCategory__ is used when Category is not set to _ALL_) and a Keyword, then it returns the products matching those. Note that the Category can be set to _ALL_ (in this case __AllProductsView__ is used) and the Keyword may be an empty string

###  AllCategoriesView, AllAddressesView, AllOrders:

This views return all Categories, Addresses (separated by billing or shipping), and all Orders (made by the requested user) respectively

### ProductDetail:

The view gets the properties of the product, and on _POST_ request adds the product to the cart with the amount specified

### CartView:

In the _GET_ request returns the last __Order__ made by the user (can be anonymous, but in the 'Anonymous case' returns the order based on the local stored info) that is not completed (has a __Payment__). The _POST_ request deletes the selected item, and in the _DELETE_ request, it deletes the complete __Order__ (Cart)

### Checkout:

This view return the __Cart__ (__Order__ to be paid). Here the user can edit the billing/shipping (since the default values are always displayed first if the user has a default address set) info and/or add a coupon. Then proceed to the PaymentView

### OrderRetrieve:

Retrieves an __Order__ based on its _pk_ and checks whether the logged user is the same as the Order's user (simple credentials' validation)

### PaymentView:

Returns the __Order__ info in the _GET_ request. In _POST_ request it tries to make the payment. The user can use the saved payment info of its account or use a new payment info. Also the new payment info can be saved for further payments. Note that a when saving payment info or using the default, the __stripe.Customer__ class is used


### CreateRefund:

This creates a Refund post for an __Order__
