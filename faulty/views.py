from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from .models import Faulty

# Create your views here.


def index(request):
    #return HttpResponse('hello django')
    faults = Faulty.objects.all().order_by('-created_at')  # [:10]
    paginator = Paginator(faults, 25)  # Show 25 contacts per page

    page = request.GET.get('page')
    listings = paginator.get_page(page)
    context = {
         'title': '故障处理',
         'faults': listings

    }

    return render(request, 'faulty/index.html', context)


def details(request, id):
    fault = get_object_or_404(Faulty, id=id)

    context = {
        'fault': fault
    }

    return render(request, 'faulty/details.html', context)
