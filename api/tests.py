import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from api.serializers import UserSerializer, WalletSerializer
from transactions.models import Wallet, Category, Transaction


class LoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'password')

    def test_login_user(self):
        self.user = authenticate(username='john', password='password')
        self.assertTrue(self.user)

    def test_login_wrong_credentials(self):
        self.user = authenticate(username='john', password='badpassword')
        self.assertFalse(self.user)

    def tearDown(self):
        self.user = User.objects.get(username='john')
        self.user.delete()


class GetApiRootTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'password')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_can_get_root(self):
        response = self.client.get(reverse('api:api_root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.user = User.objects.get(username='john')
        self.user.delete()


class CreateUserTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'lennon@thebeatles.com', 'password')
        self.client.force_authenticate(self.superuser)

    def test_get_wallet_list(self):
        url = reverse('api:user_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        self.data = {'username': 'john_snow', 'first_name': 'john', 'last_name': 'snow'}
        self.url = reverse('api:user_list')
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetUpdateAndDeleteUserTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'lennon@thebeatles.com', 'password')
        self.client.force_authenticate(self.superuser)
        self.user = User.objects.create(username='JohnSnow', first_name='John', last_name='Snow')
        self.data = UserSerializer(self.user).data
        self.data.update({'last_name': 'Changed'})
        self.url = reverse('api:user_details', args=(self.user.id,))

    def test_get_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        response = self.client.put(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CreateWalletTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'password')
        self.client.force_authenticate(self.user)

    def test_get_wallet_list(self):
        url = reverse('api:wallet_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_wallet(self):
        url = reverse('api:wallet_list')
        user_id = reverse('api:user_details', args=(self.user.id,))
        data = {'name': 'test_wallet', 'balance': 1000, 'user': user_id, 'description': 'test'}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetUpdateAndDeleteWalletTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'password')
        self.client.force_authenticate(self.user)
        self.user_id = reverse('api:user_details', args=(self.user.id,))
        self.wallet = Wallet.objects.create(name='test_wallet', balance=10,
                                            user=self.user, description='test')
        # self.data = WalletSerializer(self.wallet).data
        # self.data({'name': 'Changed'})
        self.url = reverse('api:wallet_details', args=(self.wallet.id,))

    def test_get_wallet(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wallet(self):
        data = {'name': 'Changed', 'user': self.user_id}
        response = self.client.put(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_wallet(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CreateCategoryTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'password')
        self.client.force_authenticate(self.user)

    def test_get_category_list(self):
        url = reverse('api:category_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        url = reverse('api:category_list')
        user_id = reverse('api:user_details', args=(self.user.id,))
        data = {'name': 'test_category', 'user': user_id}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetUpdateAndDeleteCategoryTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'password')
        self.client.force_authenticate(self.user)
        self.user_id = reverse('api:user_details', args=(self.user.id,))
        self.category = Category.objects.create(name='test_category', user=self.user)
        self.url = reverse('api:category_details', args=(self.category.id,))

    def test_get_category(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category(self):
        data = {'name': 'Changed', 'user': self.user_id}
        response = self.client.put(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CreateTransactionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'password')
        self.client.force_authenticate(self.user)
        self.user_id = reverse('api:user_details', args=(self.user.id,))
        self.date = datetime.datetime.today().strftime('%Y-%m-%d')

    def test_get_transaction_list(self):
        url = reverse('api:transaction_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_transaction(self):
        url = reverse('api:transaction_list')
        data = {'name': 'test_transaction', 'type': 'income', 'user': self.user_id, 'date': self.date, 'amount': 10}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetUpdateAndDeleteTransactionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'password')
        self.client.force_authenticate(self.user)
        self.user_id = reverse('api:user_details', args=(self.user.id,))
        self.date = datetime.datetime.today().strftime('%Y-%m-%d')
        self.transaction = Transaction.objects.create(name='test_transaction',
                                                      type='income',
                                                      user=self.user,
                                                      date=self.date,
                                                      amount=10)
        self.url = reverse('api:transaction_details', args=(self.transaction.id,))

    def test_get_transaction(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_transaction(self):
        data = {'name': 'Changed', 'user': self.user_id,
                'type': 'expense', 'amount': 20}
        response = self.client.put(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_transaction(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

