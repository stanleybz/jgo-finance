# create a custom login api
# Path: finance_data/finance_data/urls.py
# Path: finance_data/finance_data/views.py
from .authentication import CsrfExemptSessionAuthentication
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username and password:
        user = authenticate(username=username, password=password)
        if user:
            # If authentication is successful, generate or retrieve the token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
    
    return Response({'error': 'Invalid credentials'}, status=400)
