from importlib.util import module_for_loader
from statistics import quantiles

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User
from django.db import models
from django.utils.translation import gettext_lazy as _

from main_store.models import Product
from .managers import UserManager



class UserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name=_("Email Address"))
    first_name = models.CharField(max_length=150, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=150, verbose_name=_("Last Name"))
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email



class CartModels(models.Model):
    user_id = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)
    product_id = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=111, )

    def __str__(self):
        return f"{self.product_id}, {self.quantity}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

# Cart modeli
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.cart_items = None

    def __str__(self):
        return f"Cart of {self.user.username}"


    @property
    def total_price(self):
        total = sum(item.total_price for item in self.cart_items.all())
        return total


    @property
    def total_items(self):
        return sum(item.quantity for item in self.cart_items.all())

# CartItem modeli
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} in {self.cart.user.username}'s cart"

    # Mahsulotning umumiy narxini hisoblash (quantity * product price)
    @property
    def total_price(self):
        return self.product.price * self.quantity