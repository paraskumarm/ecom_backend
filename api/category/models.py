from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=40)
    description=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add = True)
    updated_at=models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return self.name

