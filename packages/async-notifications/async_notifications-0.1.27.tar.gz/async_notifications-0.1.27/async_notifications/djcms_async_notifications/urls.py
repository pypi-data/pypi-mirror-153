from django.urls import re_path

from .views import get_email_modal

urlpatterns = [
    re_path(r'^get_email_modal$',  get_email_modal, name="get_email_modal"),

]
