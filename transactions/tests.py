from django.core.urlresolvers import resolve
from django.test import TestCase
from users.views import user_login


class HomePageTest(TestCase):

    def test_root_url_resolves_to_main_view(self):
        found = resolve('/users/login')
        self.assertEqual(found.func, user_login)
