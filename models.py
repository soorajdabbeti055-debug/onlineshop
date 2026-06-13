from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.utils.timezone import now

class shopkeeper(models.Model):
    shop_id = models.AutoField(primary_key=True)
    ownername = models.CharField(max_length=50, null=False)
    shopname = models.CharField(max_length=50, null=False)
    shoptype = models.CharField(max_length=50, null=False)
    shopowner = models.ImageField(upload_to='static/', default="")
    shopimage = models.ImageField(upload_to='static/', default="")
    district = models.CharField(max_length=50)
    mandal = models.CharField(max_length=50)
    village = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    number = models.BigIntegerField()  # Ensured consistency with form field
    email = models.EmailField(unique=True)  # Ensured email is unique
    password = models.CharField(max_length=255)  # Increased size for hashed passwords
    is_open = models.BooleanField(default=True)
    
    """ def save(self, *args, **kwargs):
        self.password = make_password(self.password)  # Hash password before saving
        super().save(*args, **kwargs) """

    def __str__(self):
        return f"Shop name: {self.shopname}, ID: {self.shop_id}"
    
class addproduct(models.Model):
    product_id = models.AutoField(primary_key=True)
    shop_id = models.ForeignKey(shopkeeper, on_delete=models.CASCADE,null=True, blank=True,default=None)
    productname = models.CharField(max_length=50)
    productprice = models.FloatField()
    productimageone = models.ImageField(upload_to='static/')
    productimagetwo = models.ImageField(upload_to='static/')
    productinfo=models.TextField()
    is_avaiable = models.BooleanField(default=True)

    def __str__(self):
        return f"Shop id:{self.shop_id},Product name: {self.productname}, ID: {self.product_id}"
    
class signup(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    district= models.CharField(max_length=50,default="Unknown")
    mandal= models.CharField(max_length=50,default="Unknown")
    village= models.CharField(max_length=50,default="Unknown")
    area= models.CharField(max_length=50,default="Unknown")
    near_by=models.TextField(max_length=50,default="Unknown")
    h_no=models.TextField(max_length=50,default="Unknown")
    

    def __str__(self):
        return f"Username:{self.username}"
    
class buy(models.Model):
    STATUS_CHOICES = (
        ('PLACED', 'Placed'),
        ('CANCELLED', 'Cancelled'),
    )

    product = models.ForeignKey(addproduct, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='static/')
    user = models.ForeignKey(signup, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    number = models.CharField(max_length=15
                              )
    total_price = models.FloatField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    otp_created_at = models.DateTimeField(default=now)
    otp_attempts = models.IntegerField(default=0)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PLACED'
    )

    def save(self, *args, **kwargs):
        self.total_price = self.product.productprice * self.quantity
        self.number = format_phone_number(self.number)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.user.username} - {self.product.productname}"

import re

def format_phone_number(number):
    if not number:
        return number

    # keep only digits
    digits = re.sub(r'\D', '', str(number))

    # remove leading zero
    if digits.startswith("0"):
        digits = digits[1:]

    # Indian 10 digit number
    if len(digits) == 10:
        digits = "91" + digits

    # already includes country code 91
    if not digits.startswith("91"):
        digits = "91" + digits[-10:]

    return "+" + digits

