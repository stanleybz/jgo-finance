from django.shortcuts import render

def landing(request):
    return render(request, 'index.html')

def app(request, page_name):
    return render(request, 'app.html')