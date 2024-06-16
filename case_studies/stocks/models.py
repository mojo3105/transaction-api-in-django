"""
The script contains database models for the applications.
"""

#imports
from django.db import models
from django.utils import timezone
import re
from stocks.constants.common import APIConstants


# Create your models here.
class AppUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_email = models.EmailField(unique=True)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"user-id:{self.id}, email:{self.user_email}, current_balance:{self.current_balance}"
    
    def validate_and_save(self):
        if (not isinstance(self.user_email, str)) or (re.match(APIConstants.EMAIL_PATTERN, self.user_email)):
            return APIConstants.INVALID_TYPE_MESSAGE.format(field_type='string', field_name='user_email')
        if ((not isinstance(self.current_balance, float)) and (not isinstance(self.current_balance, int))) or (self.current_balance is None):
            return APIConstants.INVALID_TYPE_MESSAGE.format(field_type='float/int', field_name='current_balance')
        if self.current_balance < 0:
            return APIConstants.INCORRECT_INTEGER_VALUE.format(field_name='current_balance')
        self.save()


class Stocks(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=50)
    stock_symbol = models.CharField(max_length=10, unique=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"stock-id:{self.id}, company-name:{self.company_name}, stock-symbol:{self.stock_symbol}, current-price:{self.current_price}"
    
    def valiate_and_save(self):
        if (not isinstance(self.company_name, str)) or (self.company_name.strip() == "") or \
            (self.company_name is None):
            return APIConstants.INVALID_TYPE_MESSAGE.format(field_type='string', field_name='company_name')
        if (not isinstance(self.stock_symbol, str)) or (self.stock_symbol.strip() == "") or \
            (self.stock_symbol is None):
            return APIConstants.INVALID_TYPE_MESSAGE.format(field_type='string', field_name='stock_symbol')
        if ((not isinstance(self.current_price, float)) and (not isinstance(self.current_price, int))) or \
            (self.current_price is None):
            return APIConstants.INVALID_TYPE_MESSAGE.format(field_type='int/float', field_name='current_price')
        if (self.current_price <= 0):
            return APIConstants.INCORRECT_INTEGER_VALUE.format(field_name='current_price')
        self.save()


class UserTransactions(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10)
    amount = models.CharField(max_length=10)
    stock_symbol = models.ForeignKey(Stocks, on_delete=models.CASCADE, to_field="stock_symbol", null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"transaction-id:{self.id}, user-id:{self.user}, transaction-type:{self.transaction_type}, amount:{self.amount}"

    def validate_and_save(self):
        if (not isinstance(self.user, AppUser)) or (self.user is None):
            return APIConstants.USER_NOT_EXIST_MESSAGE
        if (not isinstance(self.transaction_type, str)) or (self.transaction_type is None):
            return APIConstants.INVALID_TYPE_MESSAGE.format(field_type='string', field_name='transaction_type')
        if (self.transaction_type not in ['credited', 'debited', 'buy', 'sell']):
            return APIConstants.TRANSACTION_VALUE_ERROR_MESSAGE.format(trans_values='credited/debited/buy/sell')
        if (self.amount is None):
            return APIConstants.INVALID_TYPE_MESSAGE.format(field_type='int/float', field_name='amount')
        self.save()


class UserHoldings(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    stock_symbol = models.ForeignKey(Stocks, on_delete=models.CASCADE, to_field="stock_symbol")
    quantity = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"holding-id:{self.id}, user-id:{self.user}, stock-symbol:{self.stock_symbol}, quantity:{self.quantity}"

    def validate_and_save(self):
        if (not isinstance(self.user, AppUser)) or (self.user is None):
            return APIConstants.USER_NOT_EXIST_MESSAGE
        if (not isinstance(self.stock_symbol, Stocks)) or (self.stock_symbol is None):
            return APIConstants.STOCKS_NOT_EXIST_MESSAGE
        if (not isinstance(self.quantity, int)) or (self.quantity is None):
            return APIConstants.INVALID_TYPE_MESSAGE.format(field_type='integer', field_name='quantity')
        if self.quantity <= 0:
            return APIConstants.INCORRECT_INTEGER_VALUE(field_name='quantity')
        self.save()


class WatchList(models.Model):
    id = models.AutoField(primary_key=True)
    watchlist_name = models.CharField(max_length=50)
    watchlist_type = models.CharField(max_length=20)
    stocks = models.CharField(max_length=1000)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"watchlist-id:{self.id}, name:{self.watchlist_name}, type:{self.watchlist_type}, stocks:{self.stocks},user-id:{self.user}"
