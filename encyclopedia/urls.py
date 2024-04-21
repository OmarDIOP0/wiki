from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>",views.display_one,name="display_one"),
    path("/search",views.search,name="search"),
    path('/create',views.create_new_page,name="create_new_page"),
    path('edit/<str:entry>',views.edit_entry,name="edit_entry"),
    path('random/',views.random_page,name="random_page")
]
