from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("wiki/<str:name>", views.view, name = "view"),
    path("wiki/<str:name>/edit", views.edit, name = "edit"),
    path("search", views.search, name="search"),
    path("random", views.random_page, name="random")
]
