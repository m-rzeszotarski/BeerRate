from django.urls import path
from . import views

# urls for created views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('beer/new', views.beer_new, name='beer_new'),
    path('beer_list', views.beer_list, name='beer_list'),
    path('beer/<int:pk>/', views.beer_detail, name='beer_detail'),
    path('beer/<int:pk>/edit', views.beer_edit, name='beer_edit'),
    path('beer/<int:pk>/remove', views.beer_remove, name='beer_remove'),
    path('beer/<int:pk>/approve', views.beer_approve, name='beer_approve'),
    path('approve_list', views.approve_list, name='approve_list'),
    path('register', views.register_request, name='register'),
]
