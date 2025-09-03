from django.db import models
from django.utils import timezone
import datetime

class User(models.Model):
    user_name = models.CharField(max_length=100, unique=True)
    user_password = models.CharField(max_length=128,null=True, blank=True)  # For hashed password
    user_email = models.EmailField(max_length=150, blank=True, null=True)
    user_phno = models.CharField(max_length=15, blank=True, null=True)
    user_pincode = models.CharField(max_length=10, blank=True, null=True)
    user_country = models.CharField(max_length=100, blank=True, null=True)
    user_state = models.CharField(max_length=100, blank=True, null=True)
    user_mundale = models.CharField(max_length=100, blank=True, null=True)
    user_city_or_village = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user_name


class Admin(models.Model):
    admin_name = models.CharField(max_length=100, unique=True)
    admin_password = models.CharField(max_length=128,null=True, blank=True)
    admin_shopname = models.CharField(max_length=150, unique=True)
    admin_email = models.EmailField(max_length=150, blank=True, null=True)
    admin_phno = models.CharField(max_length=15, blank=True, null=True)
    admin_pincode = models.CharField(max_length=10, blank=True, null=True)
    admin_country = models.CharField(max_length=100, blank=True, null=True)
    admin_state = models.CharField(max_length=100, blank=True, null=True)
    admin_mundale = models.CharField(max_length=100, blank=True, null=True)
    admin_city_or_village = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.admin_shopname


class Product(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE,default=1)
    product_name = models.CharField(max_length=150)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_quantity=models.IntegerField(default=0)
    product_brand=models.CharField(max_length=155,blank=True)
    product_category=models.CharField(max_length=63,default="")
    product_discount=models.IntegerField(default=0)
    product_url=models.CharField(max_length=155,blank=True)
    
    # Add other fields as needed

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # cart_quantity=models.IntegerField(default=0)

    def __str__(self):
        return f"CartItem - User: {self.user.user_name}, Product: {self.product.product_name}"

class Wishlist(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"WishlistItem - User: {self.user.user_name}, Product: {self.product.product_name}"

    class Meta:
        unique_together = ('user', 'product')

class Sale(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    admin = models.ForeignKey('Admin', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Per-unit price
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user_name} bought {self.quantity} x {self.product.product_name} at {self.price}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Token valid for 15 minutes
        return timezone.now() - self.created_at < datetime.timedelta(minutes=15)

    def __str__(self):
        return f"Token for {self.user.user_name}"