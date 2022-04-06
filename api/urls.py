from api.views import *
from django.urls import path

urlpatterns = [
    path("getAddressDetails/", GetAddressDetails.as_view())
]