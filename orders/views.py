from django.shortcuts import render

from django.http import HttpResponse
from .models import Orders

# Create your views here.
def index(request):
    #return HttpResponse('hello django')
    orders = Orders.objects.all()[:10]

    context = {
         'title':'工单类',
         'orders':orders

    }

    return render(request, 'orders/index.html', context)

def details(request, id):
    order = Orders.objects.get(id=id)

    context = {
        'order': order
    }

    return render(request, 'orders/details.html', context)
    
def welcom(request):
    return render(request, 'posts/welcom.html')
