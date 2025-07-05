from rest_framework import serializers

from api.address.models import Address


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "street_address",
            "city",
            "state",
            "pincode",
            "phone",
            "email",
        )
