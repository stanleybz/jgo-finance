# Generated by Django 3.0.3 on 2024-01-08 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_data', '0007_auto_20240108_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userportfolio',
            name='Remark',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
