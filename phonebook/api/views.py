from rest_framework import viewsets, filters

from .serializer import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """
    Viewset that allow `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions with Contact model.
    """

    serializer_class = ContactSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name',)

    def get_queryset(self):
        """ Function return all contacts where owner is current user. """
        return self.request.user.contacts.all()
