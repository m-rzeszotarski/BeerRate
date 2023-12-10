from django.urls import path, include
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
    path('mybeer/new', views.mybeer_new, name='mybeer_new'),
    path('mybeer_list', views.mybeer_list, name='mybeer_list'),
    path('mybeer/<int:pk>/', views.mybeer_detail, name='mybeer_detail'),
    path('mybeer/<int:pk>/edit', views.mybeer_edit, name='mybeer_edit'),
    path('mybeer/<int:pk>/remove', views.mybeer_remove, name='mybeer_remove'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:pk>', views.remove_from_cart, name='remove_from_cart'),
    path('increase_cart_item<int:pk>', views.increase_cart_item, name='increase_cart_item'),
    path('decrease_cart_item<int:pk>', views.decrease_cart_item, name='decrease_cart_item'),
    path('order/new', views.make_order, name='make_order'),
    path('order/<int:pk>/edit', views.order_edit, name='order_edit'),
    path('order_list', views.order_list, name='order_list'),
    path('order/<int:pk>/remove', views.order_remove, name='order_remove'),
    path('order/<int:pk>/<str:status>', views.order_status_change, name='order_status_change'),
    path('order_status', views.order_status, name='order_status'),
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('payment/process', views.payment_process, name='payment_process'),
    path('payment/done', views.payment_done, name='payment_done'),
    path('payment/canceled', views.payment_canceled, name='payment_canceled'),
    path('review_ban/<int:pk>', views.review_ban, name='review_ban'),
    path('review_unban/<int:pk>', views.review_unban, name='review_unban'),
]
