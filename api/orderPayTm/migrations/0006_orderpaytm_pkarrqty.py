# Generated by Django 3.2.7 on 2022-03-15 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderPayTm', '0005_orderpaytm_status_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderpaytm',
            name='pkarrqty',
            field=models.CharField(default='', max_length=500, null=True),
        ),
    ]
