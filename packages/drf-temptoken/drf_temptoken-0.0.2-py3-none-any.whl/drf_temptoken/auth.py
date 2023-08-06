from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

from drf_temptoken import utils
from drf_temptoken.models import TempToken

class TempTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        query = request.GET

        header = request.META.get(f'HTTP_{utils.TMP_TOKEN_AUTH_HEADER}'.upper())

        param = utils.get_query_param()

        if not header and not param:
            return None

        header_prefix = utils.get_header_prefix()

        value = query.get(param) 

        if (header and header_prefix not in header) and not value:
            return None

        if value:
            key = value
        else:
            _, key = header.split(header_prefix)

        try:
            token = TempToken.objects.get(key=key)
        except TempToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such token')

        if token.expired:
            token.delete()

            raise exceptions.AuthenticationFailed('Token has expired')

        user = token.user

        return (user, None)


