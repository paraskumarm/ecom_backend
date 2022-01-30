from django.db import migrations
from api.user.models import CustomUser


class Migration(migrations.Migration):
    def seed_data(apps, schema_editor):
        user = CustomUser(name="paras",
                          email="parasmahour15@gmail.com",
                          is_staff=True,
                          is_superuser=True,
                          phone="9971092573",
                          gender="Male"
                          )
        user.set_password("123456")
        user.save()

    dependencies = [

    ]

    operations = [
        migrations.RunPython(seed_data),
    ]
