from django.shortcuts import render

from django.http import HttpResponse
from .models import Cutovers

# Create your views here.
def index(request):
    #return HttpResponse('hello django')
    cutovers = Cutovers.objects.all()[:10]

    context = {
         'title':'割接类',
         'cutovers':cutovers

    }

    return render(request, 'cutovers/index.html', context)

def details(request, id):
    cutover = Cutovers.objects.get(id=id)

    context = {
        'cutover': cutover
    }

    return render(request, 'cutovers/details.html', context)

def welcom(request):
    return render(request, 'posts/welcom.html')
