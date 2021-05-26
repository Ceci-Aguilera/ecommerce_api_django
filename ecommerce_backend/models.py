from django.db import models
from django.contrib.auth.models import User,AbstractUser,AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib import auth

# Create your models here.



ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)




# ==============================================================================
#   USER and USER MANAGER: CUSTOM USER MODEL
# ==============================================================================
class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):

    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=True)
    phone = models.CharField(
        verbose_name='phone',
        max_length=20,
        unique=True,
    )

    last_uid = models.CharField(max_length=256,default='-1')
    last_token = models.CharField(max_length=256,default='-1')
    last_uid_password = models.CharField(max_length=256,default='-1')
    last_token_password = models.CharField(max_length=256,default='-1')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] #email and password are required by default

    def __str__(self):
        return self.email

    objects = UserManager()




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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quatity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quatity} of {self.product.title}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_discount_product_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_product_price() - self.get_total_discount_product_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_product_price()
        return self.get_total_product_price()






# ==============================================================================
#   ORDER
# ==============================================================================
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
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
        return self.user.email

    def get_total_cost(self):
        total_cost = 0.0
        for order_item in self.items.all():
            total_cost += order_item.get_final_price()
        if self.coupon:
            total_cost = max(0, (self.coupon.amount))
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
        return self.user.email





# ==============================================================================
#   COUPON
# ==============================================================================
class Coupon(models.Model):
    code = models.CharField(max_length=15)
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
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email + "-" + address_type

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
        return f"{self.pk}"
