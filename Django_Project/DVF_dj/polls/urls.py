from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("page1", views.index1, name="index"),
    path("apply_Region", views.index2, name="index"),
    path("page2", views.index3, name="index"),
    path("apply_Region_G2", views.index4, name="index"),

]