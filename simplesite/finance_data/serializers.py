from rest_framework import serializers
from .models import FinanceData, Company, UserPortfolio, Headlines

# For financial data
class FinanceDataSerializer(serializers.ModelSerializer):
  class Meta:
    model = FinanceData
    fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
  class Meta:
    model = Company
    fields = '__all__'

# For user portfolio
class UserPortfolioSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserPortfolio
    fields = '__all__'

# Headlines
class NewsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Headlines
    fields = '__all__'