from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib import auth
from ecommerce_accounts_app.models import User

# Create your models here.



ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)



# ==============================================================================
#   CATEGORY : Category of a Product
# ==============================================================================
class Category(models.Model):
    category_name = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural='categories'

    def __str__(self):
        return self.category_name



# ==============================================================================
#   PRODUCT
# ==============================================================================
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    price = models.FloatField(default=0.0)
    discount_price = models.FloatField(default=0.0)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/products/')

    def __str__(self):
        return self.title





# ==============================================================================
#   CART ITEM : Item added to cart
# ==============================================================================
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        helper = 'Deleted object'
        if self.product is not None:
            helper = self.product.title
        return f"{self.quantity} of {helper}"

    def get_total_product_price(self):
        if self.product is not None:
            return self.quantity * self.product.price
        return 0

    def get_amount_saved(self):
        return self.quantity * self.product.discount_price


    def get_total_discount_product_price(self):
        if self.product is not None:
            return self.get_total_product_price() - self.get_amount_saved()
        return 0

    def get_final_price(self):
        if self.product is not None:
            if self.product.discount_price:
                return self.get_total_discount_product_price()
            return self.get_total_product_price()
        return 0






# ==============================================================================
#   ORDER
# ==============================================================================
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        if self.user is not None:
            return self.user.email + '-' + str(self.start_date)
        return 'Anonymous' + '-' + str(self.start_date)

    def get_total_cost(self):
        total_cost = 0.0
        for order_item in self.items.all():
            total_cost += order_item.get_final_price()
        if self.coupon:
            total_cost -= max(0, (self.coupon.amount))
        return total_cost






# ==============================================================================
#   Payment :
# ==============================================================================
class Payment(models.Model):
    user= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user is not None:
            return self.user.email

        return 'Anonymous' + '-' + str(self.timestamp)



# ==============================================================================
#   COUPON
# ==============================================================================
class Coupon(models.Model):
    code = models.CharField(max_length=256)
    amount = models.FloatField(default=0.0)

    def __str__(self):
        return self.code




# ==============================================================================
#   ADDRESS : Can be billing or shipping and user can set it as its default one
# ==============================================================================
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    state_or_province = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email + "-" + self.address_type

    class Meta:
        verbose_name_plural = 'Addresses'





# ==============================================================================
#   REAFUND
# ==============================================================================
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk} - {self.email}"
