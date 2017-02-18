from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from transactions.forms import WalletCreateForm
from transactions.models import Wallet


class RedirectNotLoggedIn(TestCase):
    def test_get_wallet_list_not_logged_in(self):
        url = reverse('wallet:wallet_list')
        response = self.client.get(url)
        self.assertRedirects(response, '/users/login/?next={}'.format(url))


class ListViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john_snow', password='password')
        self.user.save()
        self.client = Client()
        self.client.login(username='john_snow', password='password')

    def test_logged_in_get_transaction_list(self):
        response = self.client.get(reverse('wallet:transactions_list'))
        self.assertEqual(str(response.context['user']), 'john_snow')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_get_category_list(self):
        response = self.client.get(reverse('wallet:category_list'))
        self.assertEqual(str(response.context['user']), 'john_snow')
        self.assertEqual(response.status_code, 200)


class WalletViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john_snow', password='password')
        self.user.save()
        self.client = Client()
        self.client.login(username='john_snow', password='password')
        self.wallet = Wallet.objects.create(name='TestWallet', balance=1000, user=self.user, description='test')
        self.wallet.save()

    def test_logged_in_get_wallet_list(self):
        response = self.client.get(reverse('wallet:wallet_list'))
        self.assertEqual(str(response.context['user']), 'john_snow')
        self.assertEqual(response.status_code, 200)

    def test_get_wallet_details_view(self):
        response = self.client.get(reverse('wallet:wallet_details', args=(self.wallet.id,)))
        self.assertEqual(str(response.context['user']), 'john_snow')
        self.assertEqual(response.status_code, 200)

    def test_get_wallet_create_view(self):
        response = self.client.get(reverse('wallet:wallet_create'))
        self.assertEqual(str(response.context['user']), 'john_snow')
        self.assertEqual(response.status_code, 200)

    def test_get_wallet_edit_view(self):
        response = self.client.get(reverse('wallet:wallet_create'))
        self.assertEqual(str(response.context['user']), 'john_snow')
        self.assertEqual(response.status_code, 200)

    def test_get_wallet_delete_view(self):
        response = self.client.get(reverse('wallet:wallet_delete', args=(self.wallet.id,)))
        self.assertEqual(str(response.context['user']), 'john_snow')
        self.assertEqual(response.status_code, 200)


class WalletFormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john_snow', password='password')
        self.user.save()
        self.client = Client()
        self.client.login(username='john_snow', password='password')
        self.wallet = Wallet.objects.create(name='TestWallet', balance=1000, user=self.user, description='test')
        self.wallet.save()

    def test_wallet_create_form_blank(self):
        form = WalletCreateForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['This field is required.'],
            'balance': ['This field is required.'],
        })

    def test_wallet_create_form_with_invalid_data(self):
        form_data = {'name': 'TestWallet2', 'balance': 'invalid', 'description': 'test'}
        form = WalletCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_wallet_create_form_with_invalid_data_too_long_name(self):
        form_data = {'name': 'TestWallet2'*12, 'balance': 'invalid', 'description': 'test'}
        form = WalletCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_wallet_create_form_with_valid_data(self):
        form_data = {'name': 'TestWallet2', 'balance': 100, 'description': 'test'}
        form = WalletCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        # test_wallet = form.save()
        # self.assertEqual(test_wallet.name, 'TestWallet2')
        # self.assertEqual(test_wallet.balance, 100)
        # self.assertEqual(test_wallet.description, 'test')

    def test_post_create_form(self):
        url = reverse('wallet:wallet_create')
        form_data = {'name': 'TestWallet2', 'balance': 100, 'description': 'test'}
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 200)


