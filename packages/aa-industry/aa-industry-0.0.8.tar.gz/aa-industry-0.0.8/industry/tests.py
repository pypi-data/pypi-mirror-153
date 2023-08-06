from django.test import TestCase
from django.urls import reverse as r


class ViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('industry:index'))

    def test_index_requires_login(self):
        """
        GET /industry must require login
        """
        self.assertRedirects(self.resp, f'/account/login/?next={r("industry:index")}')

