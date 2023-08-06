import secrets
from functools import partial

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class TempToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(
        max_length=171, 
        default=partial(secrets.token_urlsafe, 128), 
        blank=True,
        db_index=True
    )
    created = models.DateTimeField(auto_now=True, blank=True)
    expires_on = models.DateTimeField(null=True, default=None, blank=True)

    @property
    def expired(self):
        return self.expires_on <= timezone.now()

    def expire(self):
        self.expires_on = timezone.now()

        self.save(update_fields=('expires_on',))

        return self

    def __str__(self):
        return self.key
