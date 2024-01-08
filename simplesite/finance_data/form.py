# validate user portfolio form submission

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from .models import UserPortfolio
from django.forms import Select

class UserPortfolioForm(ModelForm):
    class Meta:
        model = UserPortfolio
        fields = ['User', 'Ticker', 'Remark', 'TargetPrice']
        widgets = {
            'Ticker': Select(attrs={'id': 'stock-select'})
        }

    def clean_ticker(self):
        data = self.cleaned_data['Ticker']
        if not data:
            raise ValidationError(_('Invalid ticker - ticker not found in database'))
        return data

    def clean_user(self):
        data = self.cleaned_data['user']
        if data <= 0:
            raise ValidationError(_('Invalid user - must be a positive integer'))
        return data
    
    def clean_targetprice(self):
        data = self.cleaned_data['targetprice']
        if data <= 0:
            raise ValidationError(_('Invalid target price - must be a positive integer'))
        return data
    
    def clean_remark(self):
        data = self.cleaned_data['remark']
        if not data:
            raise ValidationError(_('Invalid remark - remark cannot be empty'))
        return data
    
    def clean(self):
        ticker = self.cleaned_data["Ticker"]
        user = self.cleaned_data["User"]
        exist = UserPortfolio.objects.filter(User=user, Ticker=ticker)
        if exist:
            raise ValidationError(_('Invalid user portfolio - user already has this ticker in portfolio'))