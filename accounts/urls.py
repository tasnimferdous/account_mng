from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('products/', views.products, name = "products"),
    path('customer/<str:customer_id>/', views.customer, name = "customer"),
    path('create_order/<str:customer_id>/', views.createOrder, name = "create_order"),
    path('update_order/<str:order_id>/', views.updateOrder, name = "update_order"),
    path('delete_order/<str:order_id>/', views.deleteOrder, name = "delete_order"),
    path('registration/', views.registration, name = "register"),
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutPage, name = "logout"),
    path('user/', views.userPage, name = "user_page"),
    path('account/', views.accountSettings, name = "account"),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name = "reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name = "password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name = "password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name = "password_reset_complete"),
]