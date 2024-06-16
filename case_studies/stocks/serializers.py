"""
The script will create the class to serialize the django models data
"""

#imports
from rest_framework import serializers
from stocks.models import AppUser, Stocks, UserHoldings, UserTransactions, WatchList

class AppUserSerializers(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields = '__all__'


class StocksSerializers(serializers.ModelSerializer):

    class Meta:
        model = Stocks
        fields = '__all__'


class UserHoldingsSerializers(serializers.ModelSerializer):

    class Meta:
        model = UserHoldings
        fields = "__all__"


class UserTransactionsSerializers(serializers.ModelSerializer):

    class Meta:
        model = UserTransactions
        fields = '__all__'