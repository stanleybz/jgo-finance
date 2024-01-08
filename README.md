# Finance Application

This is a finance application built with Django that allows users to record their stock tickers and compare them with the headlines on the day to see the price changes. Users can also add tickers to their portfolio for stock comparison.

## Dataset

- Financial data: [Yahoo Finance Industries Dataset](https://www.kaggle.com/datasets/belayethossainds/yahoo-finance-industries-dataset)
- Headlines by date: [Financial News Headlines](https://www.kaggle.com/datasets/notlucasp/financial-news-headlines)
- Stockcode ticker to company name: [Stock Info CSV](https://github.com/dhhagan/stocks/blob/master/scripts/stock_info.csv)

## Setup

0. Prequest
  ```
  apt-get update
  apt-get install python3-virtualenv
  ```

1. Enter virtual environment:
  ```
  python3 -m venv --system-site-packages venv
  source venv/bin/activate
  ```

2. Install the required dependencies:
  ```
  pip install -r requirements.txt
  ```

3. Enter application repo
  ```
  cd simplesite
  ```

4. Run database migration (delete simplesite/db.sqlite3 before migration)
  ```
  python manage.py makemigrations
  python manage.py migrate
  ```

5. Create superadmin on by django
  ```
  python manage.py createsuperuser
  ```

6. Populate data, before that you need to update populate_date.py sys.path.append to current foloder
  ```
  python simplesite/script/populate_data.py
  ```

7. Run the application:
  ```
  python manage.py runserver
  ```

## Usage

1. Log in to your existing account created by Django admin

2. Check the stock price and compare them with the headlines on the day to see the price changes

3. Add tickers to your portfolio for stock comparison

## Dataset
*Financial data*
https://www.kaggle.com/datasets/belayethossainds/yahoo-finance-industries-dataset
(Only 2019-01-01 to 2019-01-29 due to entries limitation)

*Headlines by date*
https://www.kaggle.com/datasets/notlucasp/financial-news-headlines

*Stockcode ticker to company name*
https://github.com/dhhagan/stocks/blob/master/scripts/stock_info.csv
