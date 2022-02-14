from django.contrib import admin
from .models import Product, Size,Variation#,Images#,Tags,Category

# Register your models here.

admin.site.register(Size)
admin.site.register(Variation)
admin.site.register(Product)
# admin.site.register(Images)
# admin.site.register(Tags)
# admin.site.register(Category)