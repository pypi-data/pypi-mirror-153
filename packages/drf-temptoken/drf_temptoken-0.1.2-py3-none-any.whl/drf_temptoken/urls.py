from django.urls import path

from drf_temptoken import views

urlpatterns = (
    path('check_auth/', views.check_auth, name='check_auth'),
)
