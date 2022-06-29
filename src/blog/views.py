# from django.shortcuts import render

# # Create your views here.

# def home(request):
#     return render(request, 'blog/index.html',{'title': 'Home'})

from django.template import loader
from django.http import HttpResponse
def home(request):
    template=loader.get_template('index.html')
    return HttpResponse(template.render())