# Generated by Django 3.2.7 on 2022-01-04 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0007_auto_20220103_0741"),
    ]

    operations = [
        migrations.CreateModel(
            name="Images",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="images/"),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="product",
            name="image",
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name="product",
            name="tag",
            field=models.JSONField(),
        ),
        migrations.RemoveField(
            model_name="product",
            name="variation",
        ),
        migrations.AddField(
            model_name="product",
            name="variation",
            field=models.JSONField(null=True),
        ),
    ]
