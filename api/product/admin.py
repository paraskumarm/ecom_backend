from django.contrib import admin

from .models import Product, Variation

admin.site.register(Variation)
admin.site.register(Product)
