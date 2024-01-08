from django.urls import include, path
from . import views
from . import api
from django.urls import re_path

urlpatterns = [
    path('', views.landing, name='landing'),
    path('app/<str:page_name>', views.app, name='app'),
    path('api/finance_data', api.finance_data_list, name = 'finance_data_list'),
    path('api/finance_data/<str:ticker>', api.finance_data_list, name = 'finance_data_list_by_ticker'),
    path('api/user_portfolio', api.user_portfolio, name = 'user_portfolio'),
    path('api/companies', api.company_list, name='company_list'),
    path('api/headlines', api.headlilnes_list, name='headlines_list'),
]
