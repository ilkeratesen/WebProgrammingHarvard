from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("wiki/<str:entry>", views.entry, name="entry")
]
