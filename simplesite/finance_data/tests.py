from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import FinanceData
from datetime import datetime
from django.urls import reverse
from .models import *
from .serializers import *
import json
from rest_framework.authtoken.models import Token

class FinanceDataDetailsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.finance_data = FinanceData.objects.create(
            Date = datetime.strptime("2019-01-02 00:00:00-05:00", '%Y-%m-%d %H:%M:%S%z'),
            Open = "37.1662769799991",
            High = "38.1164913705357",
            Low = "37.0079073046783",
            Close = "37.8933334350586",
            Volume = "148158800",
            Dividends = "0",
            Stock_Splits = "0",
            Ticker = "AAPL",
        )
        self.finance_data_db = FinanceData.objects.get(id=1)

    def test_get_finance_data_details(self):
        url = reverse('finance_data_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # get columns from response data
        id = response.data['results'][0]['id']
        date = response.data['results'][0]['Date']
        open = response.data['results'][0]['Open']
        high = response.data['results'][0]['High']
        low = response.data['results'][0]['Low']
        close = response.data['results'][0]['Close']
        volume = response.data['results'][0]['Volume']
        dividends = response.data['results'][0]['Dividends']
        stock_splits = response.data['results'][0]['Stock_Splits']
        ticker = response.data['results'][0]['Ticker']

        # compare with self.finance_data_db
        id_db = self.finance_data_db.id
        date_db = self.finance_data_db.Date
        open_db = self.finance_data_db.Open
        high_db = self.finance_data_db.High
        low_db = self.finance_data_db.Low
        close_db = self.finance_data_db.Close
        volume_db = self.finance_data_db.Volume
        dividends_db = self.finance_data_db.Dividends
        stock_splits_db = self.finance_data_db.Stock_Splits
        ticker_db = self.finance_data_db.Ticker

        self.assertEqual(id, id_db)
        self.assertEqual(date, date_db.strftime('%Y-%m-%d'))
        self.assertEqual(Decimal(open), open_db) 
        self.assertEqual(Decimal(high), high_db)
        self.assertEqual(Decimal(low), low_db)
        self.assertEqual(Decimal(close), close_db)
        self.assertEqual(Decimal(volume), volume_db)
        self.assertEqual(Decimal(dividends), dividends_db)
        self.assertEqual(Decimal(stock_splits), stock_splits_db)
        self.assertEqual(ticker, ticker_db)

class CompanyListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('company_list')

    def test_company_list_get(self):
        company = Company.objects.create(Ticker="A", Name="Agilent Technologies", Exchange="NYSE")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        expected_data = CompanySerializer(company).data
        self.assertEqual(response.json()[0], expected_data)

class HeadlinesListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('headlines_list')

    def test_get_headlines_list(self):
        headline1 = Headlines.objects.create(
            Date=datetime.strptime("31-Jan-19", '%d-%b-%y'),
            Headlines="Npower to cut 900 jobs as it predicts marked financial losses for 2019"
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserPortfolioTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

    def test_get_user_portfolio(self):
        url = reverse('user_portfolio')
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_create_user_portfolio(self):
        url = reverse('user_portfolio')
        data = {'ticker': 'AAPL'}
        response = self.client.post(url, json.dumps(data), content_type='application/json', **self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(UserPortfolio.objects.filter(User=self.user, Ticker='AAPL').count(), 1)

    def test_create_existing_user_portfolio(self):
        UserPortfolio.objects.create(User=self.user, Ticker='AAPL')
        url = reverse('user_portfolio')
        data = {'ticker': 'AAPL'}
        response = self.client.post(url, json.dumps(data), content_type='application/json', **self.headers)
        self.assertEqual(response.status_code, 400)

    def test_delete_user_portfolio(self):
        user_portfolio = UserPortfolio.objects.create(User=self.user, Ticker='AAPL')
        url = reverse('user_portfolio')
        data = {'ticker': 'AAPL'}
        response = self.client.delete(url, json.dumps(data), content_type='application/json', **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(UserPortfolio.objects.filter(pk=user_portfolio.pk).exists())

    def test_delete_nonexistent_user_portfolio(self):
        url = reverse('user_portfolio')
        data = {'ticker': 'AAPL'}
        response = self.client.delete(url, json.dumps(data), content_type='application/json', **self.headers)
        self.assertEqual(response.status_code, 404)

    def test_update_user_portfolio(self):
        user_portfolio = UserPortfolio.objects.create(User=self.user, Ticker='AAPL')
        url = reverse('user_portfolio')
        data = {'id': user_portfolio.pk, 'ticker': 'GOOG'}
        response = self.client.put(url, json.dumps(data), content_type='application/json', **self.headers)
        self.assertEqual(response.status_code, 200)
        user_portfolio.refresh_from_db()
        self.assertEqual(user_portfolio.Ticker, 'GOOG')

    def test_update_nonexistent_user_portfolio(self):
        url = reverse('user_portfolio')
        data = {'id': 999, 'ticker': 'GOOG'} # mock a non-existent id
        response = self.client.put(url, json.dumps(data), content_type='application/json', **self.headers)
        self.assertEqual(response.status_code, 404)