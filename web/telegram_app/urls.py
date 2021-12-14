from django.urls import path

from telegram_app import views

app_name = 'telegram_user'

urlpatterns = [
    path('users/', views.CreateUser.as_view()),
    path('users/<int:pk>/', views.RetrieveUpdateUser.as_view()),
    path('payment/', views.PaymentHook.as_view())
]
