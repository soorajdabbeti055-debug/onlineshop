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

    def __str__(self):
        return f"Username:{self.username}"
    
class buy(models.Model):
    product = models.ForeignKey(addproduct, on_delete=models.CASCADE)
    product_image=models.ImageField(upload_to='static/')
    user = models.ForeignKey(signup, on_delete=models.CASCADE)  # Added user field
    quantity = models.IntegerField()
    number = models.BigIntegerField()
    total_price = models.FloatField(null=True, blank=True)
    def save(self, *args, **kwargs):
        self.total_price = self.product.productprice * self.quantity  # Calculate total price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"User: {self.user.username}, Product: {self.product.productname}, Quantity: {self.quantity}"
     
