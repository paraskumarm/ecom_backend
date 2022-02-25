# Generated by Django 3.2.7 on 2022-02-22 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_variation_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='size',
        ),
        migrations.AddField(
            model_name='variation',
            name='stockL',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='variation',
            name='stockM',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='variation',
            name='stockS',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='variation',
            name='stockXL',
            field=models.PositiveIntegerField(default=0),
        ),
    ]