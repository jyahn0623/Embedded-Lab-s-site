from django.urls import path
from Main.views import *
from Main import views

app_name = 'main'
urlpatterns = [
    path('', Main.as_view(), name="main"),
    path('members/', views.ViewMembers, name="Viewmembers"),
]
