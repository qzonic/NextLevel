from django.contrib import admin

from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    """ Contact admin model. """

    list_display = (
        'owner',
        'first_name',
        'last_name',
        'phone',
        'email',
    )
    list_editable = (
        'first_name',
        'last_name',
        'phone',
        'email',
    )
    search_fields = (
        'first_name',
        'last_name',
    )


admin.site.register(Contact, ContactAdmin)
