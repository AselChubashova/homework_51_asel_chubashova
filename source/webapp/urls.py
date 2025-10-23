from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cat/', views.cat_view, name='cat_view'),
]
