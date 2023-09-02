from django.core.validators import RegexValidator
from rest_framework import serializers

from contact.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """ Serializer for contact model. """

    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    phone = serializers.CharField(
        max_length=16,
        validators=[RegexValidator(
            regex=r'^((8|\+7)[\- ]?)(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$',
            message='Invalid phone number format.'
        )]
    )

    class Meta:
        model = Contact
        fields = (
            'id',
            'owner',
            'first_name',
            'last_name',
            'phone',
            'email',
        )
