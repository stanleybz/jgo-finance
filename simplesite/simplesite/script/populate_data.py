import os
import sys
import django
import csv

sys.path.append("/Users/apple/Documents/study/cm3035/simplesite")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simplesite.settings')
django.setup()

import csv
from datetime import datetime
from finance_data.models import FinanceData, Company, Headlines

stock_details_csv_path = '/Users/apple/Documents/study/cm3035/dataset/stock_details_5_years.csv'
stock_info_csv_path = '/Users/apple/Documents/study/cm3035/dataset/stock_info.csv'
headlines_csv_path = '/Users/apple/Documents/study/cm3035/dataset/headlines.csv'

FinanceData.objects.all().delete()
Company.objects.all().delete()
Headlines.objects.all().delete()
print("Total rows from FinanceData.objects after deletion:", FinanceData.objects.count())
print("Total rows from Company.objects after deletion:", Company.objects.count())
print("Total rows from Company.objects after deletion:", Headlines.objects.count())

unique_companies = set()

print("Importing stock details")
with open(stock_details_csv_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for index, row in enumerate(csv_reader):
        if index % 1000 == 0:
            print(f"Completed: {index} row")

        date_str = row['Date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S%z')
        data_row = FinanceData(
            Date=date_obj,
            Open=float(row['Open']),
            High=float(row['High']),
            Low=float(row['Low']),
            Close=float(row['Close']),
            Volume=int(row['Volume']),
            Dividends=float(row['Dividends']),
            Stock_Splits=float(row['Stock Splits']),
            Ticker=row['Company']
        )

        # Push the company name to unique_companies set
        unique_companies.add(row['Company'])
        data_row.save()

    print("Total count of FinanceData table after importing:", FinanceData.objects.count())


matched_companies = set()

print("Importing company details")
with open(stock_info_csv_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for index, row in enumerate(csv_reader):  # Fix: Added 'enumerate' to iterate over csv_reader
        if index % 1000 == 0:
            print(f"Completed: {index} row")

        if row['Ticker'] in unique_companies:
            data_row = Company(
                Ticker=row['Ticker'],
                Name=row['Name'],
                Exchange=row['Exchange']
            )
            data_row.save()

print("Total count of Company table after importing:", Company.objects.count())

print("Importing headlines")
with open(headlines_csv_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for index, row in enumerate(csv_reader):
        if index % 1000 == 0:
            print(f"Completed: {index} row")

        date_str = row['Time'].strip()
        #  7:21  PM ET Thu, 31 Jan 2019
        format_string = '%d-%b-%y'

        date_obj = None
        try:
            date_obj = datetime.strptime(date_str, format_string)
        except ValueError as e:
            print("Error parsing time:", e)

        data_row = Headlines(
            Headlines=row['Headlines'],
            Date=date_obj,
        )
        data_row.save()

print("Total count of Headlines table after importing:", Headlines.objects.count())

total_count = FinanceData.objects.count() + Company.objects.count() + Headlines.objects.count()
print(f"All data imported successfully! Total {total_count} entries.")