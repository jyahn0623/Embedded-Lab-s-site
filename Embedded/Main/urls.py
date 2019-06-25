from django.urls import path
from Main.views import *

urlpatterns = [
    path('', Main.as_view(), name="main"),
]
