from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *
from .authentication import CsrfExemptSessionAuthentication
from rest_framework.decorators import authentication_classes
import json
from rest_framework.authtoken.models import Token

class CustomPagination(PageNumberPagination):
    page_size = 30 
    page_size_query_param = 'page_size'
    max_page_size = 100 
    
@api_view(['GET'])
@csrf_exempt
def finance_data_list(request, ticker):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        # filter by ticker
        # ticker = request.GET.get('ticker')
        if ticker is not None:
            financeData = FinanceData.objects.filter(Ticker=ticker)
            if not financeData.exists():
                return HttpResponse("Data not found", status=404)
        else:
            financeData = FinanceData.objects.all()

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(financeData, request)
        serializer = FinanceDataSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    return JsonResponse("Method not allow", status=400)

# an endpoint for getting company from company table
@api_view(['GET'])
@csrf_exempt
def company_list(request):
    if request.method == 'GET':
        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse("Method not allow", status=400)

# get headlilnes
@api_view(['GET'])
@csrf_exempt
def headlilnes_list(request):
    if request.method == 'GET':
        news = Headlines.objects.all()
        serializer = NewsSerializer(news, many=True)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse("Method not allow", status=400)

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@authentication_classes([CsrfExemptSessionAuthentication])
def user_portfolio(request):
    # Check user token from request.header and get user id
    token = request.META.get('HTTP_AUTHORIZATION')
    user = None
    if token is None:
        return HttpResponse("Token is required", status=401)
    try:
        token = token.split(' ')[1]
        user = Token.objects.get(key=token).user
    except Token.DoesNotExist:
        return HttpResponse("Token is invalid", status=401)

    if request.method == 'GET':
        try:
            user_portfolios = UserPortfolio.objects.filter(User=user.id)
            if user_portfolios.exists():
                serializer = UserPortfolioSerializer(user_portfolios, many=True)
                return JsonResponse(serializer.data, safe=False)
            else:
                # return empty array if user portfolio not found
                return JsonResponse([], safe=False)
        except UserPortfolio.DoesNotExist:
            return HttpResponse("User portfolio not found", status=404)

    elif request.method == 'POST':
        data = json.loads(request.body)
        ticker = data.get('ticker')

        if ticker is None:
            return HttpResponse("Ticker is required", status=400)
        
        exist_ticker = UserPortfolio.objects.filter(User=user.id, Ticker=ticker)
        if exist_ticker.exists():
            return HttpResponse("Ticker already exist", status=400)

        user_portfolio = UserPortfolio(User=user, Ticker=ticker)
        user_portfolio.save()
        return HttpResponse("Data saved successfully", status=201)    
    
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        ticker = data.get('ticker')

        if ticker is None:
            return HttpResponse("Ticker is required", status=400)
        
        try:
            user_portfolio = UserPortfolio.objects.filter(Ticker=ticker, User=user.id)
            if not user_portfolio.exists():
                return HttpResponse("Data not found", status=404)
            user_portfolio.delete()
            return HttpResponse("Data deleted successfully", status=200)
        except UserPortfolio.DoesNotExist:
            return HttpResponse("Data not found", status=404)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        id = data.get('id')
        ticker = data.get('ticker')

        if id is None:
            return HttpResponse("Id is required", status=400)
        if ticker is None:
            return HttpResponse("Ticker is required", status=400)
        
        try:
            user_portfolio = UserPortfolio.objects.filter(pk=id, User=user.id).first()
            if not user_portfolio:
                return HttpResponse("Data not found", status=404)

            user_portfolio.Ticker = ticker
            user_portfolio.save()
            return HttpResponse("Data updated successfully", status=200)
        except UserPortfolio.DoesNotExist:
            return HttpResponse("Data not found", status=404)
        