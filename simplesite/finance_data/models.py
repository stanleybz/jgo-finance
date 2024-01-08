from django.db import models
from django.contrib.auth.models import User

class FinanceData(models.Model):
    Date = models.DateField()
    Open = models.DecimalField(max_digits=38, decimal_places=12)
    High = models.DecimalField(max_digits=38, decimal_places=12)
    Low = models.DecimalField(max_digits=38, decimal_places=12)
    Close = models.DecimalField(max_digits=38, decimal_places=12)
    Volume = models.IntegerField()
    Dividends = models.DecimalField(max_digits=38, decimal_places=12)
    Stock_Splits = models.DecimalField(max_digits=38, decimal_places=12)
    Ticker = models.CharField(max_length=200)

class Company(models.Model):
    Ticker = models.CharField(max_length=10)
    Name = models.CharField(max_length=200)
    Exchange = models.CharField(max_length=50)

class Headlines(models.Model):
    Headlines = models.CharField(max_length=200)
    Date = models.DateField()

class UserPortfolio(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Ticker = models.CharField(max_length=10)
