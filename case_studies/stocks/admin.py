from django.contrib import admin
from stocks.models import AppUser, UserTransactions, UserHoldings, WatchList, Stocks

# Register your models here.
admin.site.register(AppUser)
admin.site.register(UserTransactions)
admin.site.register(UserHoldings)
admin.site.register(WatchList)
admin.site.register(Stocks)