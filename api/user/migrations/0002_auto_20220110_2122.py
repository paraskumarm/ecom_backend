# Generated by Django 3.2.7 on 2022-01-10 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='firstname',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='lastname',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
