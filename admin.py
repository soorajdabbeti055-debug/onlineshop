from django.contrib import admin
from .models import shopkeeper
from .models import addproduct
from .models import signup
from .models import buy

# Register your models here.
admin.site.register(shopkeeper)
admin.site.register(addproduct)
admin.site.register(signup)
admin.site.register(buy)


