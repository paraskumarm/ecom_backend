# Generated by Django 3.2.7 on 2022-03-30 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20220127_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='session_token',
            field=models.CharField(default=0, max_length=1000),
        ),
    ]