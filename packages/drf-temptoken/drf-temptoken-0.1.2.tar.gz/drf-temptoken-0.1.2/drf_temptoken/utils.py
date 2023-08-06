from datetime import timedelta
from functools import partial

from django.utils import timezone
from django.conf import settings

from drf_temptoken import models

TMP_TOKEN_AUTH_HEADER = 'Authorization'

TMP_TOKEN_HEADR_PREFIX = 'TMP'

TMP_TOKEN_TIME_DELTA_KWARGS = {
    'days': 7
}

get_header_prefix = lambda: getattr(settings, 'TMP_TOKEN_HEADR_PREFIX', TMP_TOKEN_HEADR_PREFIX) + ' '

get_query_param = partial(getattr, settings, 'TMP_TOKEN_QUERY_PARAM', None)

get_time_delta = partial(timedelta, **getattr(settings, 'TMP_TOKEN_TIME_DELTA_KWARGS', TMP_TOKEN_TIME_DELTA_KWARGS))

get_user_tokens = lambda user: models.TempToken.objects.filter(user=user)

create_token = lambda user, **kwargs: models.TempToken.objects.create(user=user, **kwargs)

