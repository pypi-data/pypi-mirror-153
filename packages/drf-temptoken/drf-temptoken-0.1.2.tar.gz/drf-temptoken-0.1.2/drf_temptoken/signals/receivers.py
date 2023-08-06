from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save

from drf_temptoken import models, utils

@receiver(pre_save, sender=models.TempToken)
def on_token_pre_save(sender, *args, **kwargs):
    models.TempToken.objects.filter(expires_on__lte=timezone.now()).delete()

    instance = kwargs['instance']

    if not instance.expires_on:
        instance.expires_on = timezone.now() + utils.get_time_delta()

