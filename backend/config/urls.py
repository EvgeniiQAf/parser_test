"""URL configuration for backend project."""

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path

urlpatterns = [
    path("", lambda request: redirect("admin/", permanent=False)),
    path("admin/", admin.site.urls),
]
