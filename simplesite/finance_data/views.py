from django.shortcuts import render
from .form import UserPortfolioForm

def landing(request):
    return render(request, 'index.html')

def app(request, page_name):
    form = UserPortfolioForm() 
    if request.method == 'POST':
        form = request.POST
        print(form)
        form = UserPortfolioForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'app.html', { 'status': 'success', 'form': form })
        else:
            return render(request, 'app.html', { 'status': 'error', 'form': form })

    return render(request, 'app.html', { 'form': form })