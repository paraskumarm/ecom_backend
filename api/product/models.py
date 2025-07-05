from django.db import models


class Variation(models.Model):
    name = models.CharField(max_length=40, default="variation name")
    color = models.CharField(max_length=40, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    stockS = models.PositiveIntegerField(default=0)
    stockM = models.PositiveIntegerField(default=0)
    stockL = models.PositiveIntegerField(default=0)
    stockXL = models.PositiveIntegerField(default=0)
    stockXXL = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=40)
    price = models.CharField(max_length=40)
    discount = models.PositiveIntegerField(default=10)
    offerEnd = models.DateTimeField(null=True)
    new = models.BooleanField(default=True)
    saleCount = models.PositiveIntegerField(null=True)
    category = models.JSONField()
    tag = models.JSONField()
    variation = models.ManyToManyField(Variation)
    image1 = models.ImageField(upload_to="images/", blank=True, null=True)
    image2 = models.ImageField(upload_to="images/", blank=True, null=True)
    image3 = models.ImageField(upload_to="images/", blank=True, null=True)
    image4 = models.ImageField(upload_to="images/", blank=True, null=True)
    image5 = models.ImageField(upload_to="images/", blank=True, null=True)
    shortDescription = models.CharField(max_length=1000, null=True)
    fullDescription = models.CharField(max_length=2000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
