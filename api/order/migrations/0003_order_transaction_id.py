# Generated by Django 3.2.7 on 2022-05-12 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0002_auto_20220512_1550"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="transaction_id",
            field=models.IntegerField(default=0),
        ),
    ]
