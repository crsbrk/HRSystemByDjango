from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from .models import Orders

# Create your views here.
def index(request):
    #return HttpResponse('hello django')
    #orders = Orders.objects.all()[:10]
    orders = Orders.objects.all().order_by('-deadline_at')
    paginator = Paginator(orders, 15) # Show 25 contacts per page

    page = request.GET.get('page')
    listings = paginator.get_page(page)

    context = {
         'title':'工单类',
         'orders':listings

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
