from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("account-transactions/", views.account_transactions, name="account_transactions"),
    path("stocks-transactions/", views.stocks_transactions, name="stocks_transactions"),
    path("app_user/<int:id>/", views.app_user, name="app_user"),
    path("app_user/", views.app_user, name="app_user"),
    path("stocks/<int:id>/", views.stocks, name="stocks"),
    path("stocks/", views.stocks, name="stocks"),
    path("user_holdings/<int:id>/", views.user_holdings, name="user_holdings"),
    path("user_holdings/", views.user_holdings, name="user_holdings"),
    path("user_transactions/<int:id>/", views.user_transactions, name="user_transactions"),
    path("user_transactions/", views.user_transactions, name="user_transactions"),
]