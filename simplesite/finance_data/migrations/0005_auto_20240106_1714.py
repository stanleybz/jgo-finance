# Generated by Django 3.0.3 on 2024-01-06 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance_data', '0004_headlines'),
    ]

    operations = [
        migrations.RenameField(
            model_name='headlines',
            old_name='Time',
            new_name='Date',
        ),
        migrations.RemoveField(
            model_name='headlines',
            name='Description',
        ),
        migrations.RemoveField(
            model_name='headlines',
            name='Ticker',
        ),
    ]
