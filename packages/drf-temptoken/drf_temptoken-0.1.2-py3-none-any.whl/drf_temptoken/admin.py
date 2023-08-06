from django.contrib import admin

from drf_temptoken import models

admin.site.register(models.TempToken)

