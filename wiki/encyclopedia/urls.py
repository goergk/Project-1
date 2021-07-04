from django.urls import path
from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/<str:title>/edit", views.editPage, name="editPage"),
    path("search", views.searchPage, name="searchPage"),
    path("random", views.randomPage, name="randomPage"),
    path("new", views.newPage, name="newPage")
]
