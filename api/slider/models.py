from django.db import models

# Create your models here.
class Slider(models.Model):
    title=models.CharField(max_length=40)
    subtitle=models.CharField(max_length=200)
    text=models.TextField()
    image=models.ImageField(upload_to='images/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add = True)
    updated_at=models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return self.title
