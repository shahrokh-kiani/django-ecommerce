from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("aboutus/", views.aboutus, name="aboutus"),
]
