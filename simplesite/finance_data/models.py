from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

"""
For Finance Data models
Date: The date of this record
Open: The opening price of the stock in the date
High: The highest price of the stock in the date
Low: The lowest price of the stock in the date
Close: The closing price of the stock in the date
Volume: The volume of the stock in the date
Dividends: The dividends of the stock in the date
Stock_Splits: The stock splits of the stock in the date
Ticker: The stock ticker of this entry
"""
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

"""
For Company to pair the company name with stock ticker
Ticker: The stock ticker of this company
Name: The name of this company
Exchange: The exchange of this company on
"""
class Company(models.Model):
    Ticker = models.CharField(max_length=10)
    Name = models.CharField(max_length=200)
    Exchange = models.CharField(max_length=50)

"""
For Headlines to pair the headline with the date
Headlines: The headline of this article
Date: The date of this article
"""
class Headlines(models.Model):
    Headlines = models.CharField(max_length=200)
    Date = models.DateField()

# Custom validator function to validate positive numbers
def validate_positive(value):
    if value <= 0:
        raise ValidationError("Price must be a positive number.")

"""
For UserPortfolio to store the stock ticker
User: The user of this portfolio
Ticker: The stock ticker of this portfolio
"""
class UserPortfolio(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Ticker = models.CharField(max_length=10)
    Remark = models.CharField(max_length=200, default="", null=True)
    TargetPrice = models.DecimalField(max_digits=38, decimal_places=12, default=0, validators=[validate_positive], null=True)
