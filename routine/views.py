from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from .models import Routine

# Create your views here.


def index(request):
    routines = Routine.objects.all().order_by('-created_at')  # [:10]
    paginator = Paginator(routines, 25)  # Show 25 contacts per page

    page = request.GET.get('page')
    listings = paginator.get_page(page)
    context = {
         'title': '故障处理',
         'routines': listings

    }

    return render(request, 'routine/index.html', context)


def details(request, id):
    routine = Routine.objects.get(id=id)

    context = {
        'routine': routine
    }

    return render(request, 'routine/details.html', context)
