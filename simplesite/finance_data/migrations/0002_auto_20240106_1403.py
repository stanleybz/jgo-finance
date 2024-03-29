# Generated by Django 3.0.3 on 2024-01-06 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Ticker', models.CharField(max_length=10)),
                ('Name', models.CharField(max_length=200)),
                ('Exchange', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='financedata',
            old_name='Company',
            new_name='Ticker',
        ),
    ]
