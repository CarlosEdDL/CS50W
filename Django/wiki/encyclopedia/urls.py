from django.urls import path, re_path
from . import views





urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entries, name="entry"),
    path("entry/new", views.new_entry, name="new_entry"),
    path("entry/search", views.search_entry, name="search"),
    path("entry/edit", views.edit, name="edit")
    ]
    
    

