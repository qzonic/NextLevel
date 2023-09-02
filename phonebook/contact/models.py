from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Contact(models.Model):
    """ Contact model. """

    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='contacts',
    )
    first_name = models.CharField(
        max_length=128,
    )
    last_name = models.CharField(
        max_length=128,
    )
    phone = models.CharField(
        max_length=16,
    )
    email = models.EmailField()

    class Meta:
        ordering = ['first_name', 'last_name']
