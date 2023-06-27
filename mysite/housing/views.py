from django.shortcuts import render

from housing.models import Housing, News


def home(request):
    return render(request, 'housing/home.html')

def about(request):
    return render(request, 'housing/about.html')

def contact(request):
    return render(request, 'housing/contact.html')

def housing_list(request):
    housing = Housing.objects.all()
    return render(request, 'housing/housing_list.html', {'housing': housing})

def news_list(request):
    news = News.objects.all()
    return render(request, 'housing/news_list.html', {'news': news})