#added this file manually
from django.db.models import fields
from api.address.models import Address
from rest_framework import serializers

class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Address
        fields=("id","user","first_name",
        "last_name",
        "street_address",
        "city",
        "state",
        "pincode",
        "phone",
        "email")