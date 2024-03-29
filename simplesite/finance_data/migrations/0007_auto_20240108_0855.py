# Generated by Django 3.0.3 on 2024-01-08 08:55

from django.db import migrations, models
import finance_data.models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_data', '0006_auto_20240108_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userportfolio',
            name='Remark',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='userportfolio',
            name='TargetPrice',
            field=models.DecimalField(decimal_places=12, default=0, max_digits=38, validators=[finance_data.models.validate_positive]),
        ),
    ]
