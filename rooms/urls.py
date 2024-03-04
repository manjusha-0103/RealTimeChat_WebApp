from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', teams, name="temas"),
    path('<slug:slug>/', team, name = "team")
]