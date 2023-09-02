from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from contact.models import Contact

User = get_user_model()


class TestContact(APITestCase):
    """ Test contact api. """

    contact_url = '/api/v1/contacts/'

    @classmethod
    def setUpClass(cls):
        super(TestContact, cls).setUpClass()
        cls.first_user = User.objects.create_user(
            username='first_user',
        )
        cls.second_user = User.objects.create_user(
            username='second_user',
        )
        cls.first_user_contact = Contact.objects.create(
            owner=cls.first_user,
            first_name='Иван',
            last_name='Иванов',
            phone='+79046738754',
            email='ivanov@ivan.ru',
        )
        cls.second_user_contact = Contact.objects.create(
            owner=cls.second_user,
            first_name='Петр',
            last_name='Петров',
            phone='+79104563499',
            email='petrov@petr.ru',
        )

    def setUp(self) -> None:
        self.guest_client = APIClient()

        self.first_authorized_client = APIClient()
        first_token = RefreshToken.for_user(self.first_user)
        self.first_authorized_client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(first_token.access_token)}'
        )

        self.second_authorized_client = APIClient()
        second_token = RefreshToken.for_user(self.second_user)
        self.second_authorized_client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(second_token.access_token)}'
        )

    def test_get_contact_by_guest(self):
        response = self.guest_client.get(self.contact_url)
        expected_error = {'detail': 'Authentication credentials were not provided.'}

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), expected_error)

    def test_get_contact_list_by_owner(self):
        contacts_count = Contact.objects.filter(owner=self.first_user).count()
        response = self.first_authorized_client.get(self.contact_url)
        expected_keys = ['count', 'next', 'previous', 'results']

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response_json.keys()), expected_keys)
        self.assertEqual(response_json['count'], contacts_count)

        for contact in response_json['results']:
            self.assertTrue(Contact.objects.filter(
                owner=self.first_user,
                first_name=contact['first_name'],
                last_name=contact['last_name'],
                phone=contact['phone'],
                email=contact['email'],
            ).exists())

    def test_get_contact_with_id_by_owner(self):
        response = self.first_authorized_client.get(
            self.contact_url + str(self.first_user_contact.id) + '/'
        )

        response_json = response.json()
        contact = Contact.objects.filter(
            id=response_json['id'],
            first_name=response_json['first_name'],
            last_name=response_json['last_name'],
            phone=response_json['phone'],
            email=response_json['email'],
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(contact.exists())
        self.assertEqual(contact.first().owner, self.first_user)

    def test_get_contact_with_id_by_another_user(self):
        response = self.second_authorized_client.get(
            self.contact_url + str(self.first_user_contact.id) + '/'
        )
        expected_error = {'detail': 'Not found.'}

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), expected_error)

    def test_create_contact_by_guest(self):
        data = {
            'first_name': 'Guest',
            'last_name': 'Guestovich',
            'phone': '89003337777',
            'email': 'guest@guestovich.ru',
        }
        response = self.guest_client.post(self.contact_url, data=data)
        expected_error = {'detail': 'Authentication credentials were not provided.'}

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), expected_error)

    def test_create_contact_with_bad_data(self):
        data = {}
        response = self.first_authorized_client.post(self.contact_url, data=data)
        expected_error = ['This field is required.']
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for error in response_json:
            self.assertEqual(
                response_json[error],
                expected_error
            )

    def test_validate_phone(self):
        invalid_phones = [
            '89oo3337777',
            'phone',
            '111',
            '+790364548973134',
            '9036454897'
        ]
        data = {
            'first_name': 'Phone',
            'last_name': 'Phonovich',
            'email': 'phone@phonovich.ru',
        }
        expected_error = {'phone': ['Invalid phone number format.']}
        for phone in invalid_phones:
            data['phone'] = phone
            response = self.first_authorized_client.post(self.contact_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, phone)
            self.assertEqual(response.json(), expected_error)

    def test_create_contact(self):
        contacts_count = Contact.objects.count()
        data = {
            'first_name': 'First',
            'last_name': 'User',
            'phone': '89003337777',
            'email': 'first@user.ru',
        }
        response = self.first_authorized_client.post(self.contact_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), contacts_count + 1)

    def test_put_patch_delete_contact_by_another_user(self):
        url = self.contact_url + str(self.second_user_contact.id) + '/'
        methods = ['put', 'patch', 'delete']
        for method in methods:
            met = getattr(self.first_authorized_client, method)
            response = met(url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_patch_contact_by_owner(self):
        url = self.contact_url + str(self.first_user_contact.id) + '/'
        data = {
            'first_name': 'Another first name',
            'last_name': 'Another last name',
            'phone': '89023567834',
            'email': 'new@new.ru',
        }

        response = self.first_authorized_client.put(url, data=data)
        response_json = response.json()
        contact = Contact.objects.get(id=self.first_user_contact.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            [
                contact.id,
                contact.first_name,
                contact.last_name,
                contact.phone,
                contact.email,
            ],
            [
                response_json['id'],
                response_json['first_name'],
                response_json['last_name'],
                response_json['phone'],
                response_json['email'],
            ]
        )

    def test_patch_contact_by_owner(self):
        url = self.contact_url + str(self.first_user_contact.id) + '/'
        data = {'phone': '89058754387'}

        response = self.first_authorized_client.patch(url, data=data)
        response_json = response.json()
        contact = Contact.objects.get(id=self.first_user_contact.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            contact.phone,
            response_json['phone']
        )

    def test_delete_contact_by_owner(self):
        url = self.contact_url + str(self.first_user_contact.id) + '/'

        response = self.first_authorized_client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
