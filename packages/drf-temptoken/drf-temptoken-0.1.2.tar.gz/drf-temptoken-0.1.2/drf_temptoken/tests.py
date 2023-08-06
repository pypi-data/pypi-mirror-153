from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from drf_temptoken import utils, models

User = get_user_model()

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='kapustlo', password='password')

    def test_token_expires(self):
        token = utils.create_token(self.user)

        token = token.expire()

        self.assertTrue(token.expired)

class UtilsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='kapustlo', password='password')

    def test_create_token_generates_token_for_user(self):
        token = utils.create_token(self.user)

        self.assertEquals(token.user.pk, self.user.pk)

    def test_get_user_tokens_returns_quryset_with_3_tokens(self):
        for _ in range(3):
            utils.create_token(self.user)

        tokens = utils.get_user_tokens(self.user)

        self.assertEquals(tokens.count(), 3)

class ReceiversTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='kapustlo', password='password')

        self.token = utils.create_token(self.user)

        self.expired_pks = []

        for _ in range(3):
            token = utils.create_token(self.user, expires_on=timezone.now() - utils.get_time_delta())

            self.expired_pks.append(token.pk)

    def test_expired_tokens_deleted_after_creation_of_another_token(self):
        utils.create_token(self.user)

        tokens = models.TempToken.objects.filter(pk__in=self.expired_pks)

        self.assertEquals(tokens.count(), 0)

    def test_exipration_date_added(self):
        self.assertNotEquals(self.token.expires_on, None)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='kapustlo', password='password')

        self.token = utils.create_token(self.user)

    def test_check_auth_returns_http_204_no_content(self):
        url = reverse('check_auth')

        headers = {
            'HTTP_' + utils.TMP_TOKEN_AUTH_HEADER.upper(): utils.get_header_prefix() + self.token.key
        }

        response = self.client.get(url, **headers)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
