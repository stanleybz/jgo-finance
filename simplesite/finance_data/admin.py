from django.contrib import admin
from .models import FinanceData, Company

class FinanceDataAdmin(admin.ModelAdmin):
  list_display = ('Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock_Splits', 'Ticker')


class CompanyAdmin(admin.ModelAdmin):
  list_display = ('Ticker', 'Name', 'Exchange')

admin.site.register(FinanceData, FinanceDataAdmin)
admin.site.register(Company, CompanyAdmin)
