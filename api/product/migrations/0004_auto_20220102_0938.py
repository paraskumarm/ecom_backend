# Generated by Django 3.2.7 on 2022-01-02 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0003_auto_20220102_0637"),
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
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ManyToManyField(to="product.Images"),
        ),
    ]
