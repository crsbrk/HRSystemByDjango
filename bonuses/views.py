from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from .models import Bonuses

# Create your views here.
def index(request):
    #return HttpResponse('hello django')
    bonuses = Bonuses.objects.all()#[:10]
    paginator = Paginator(bonuses, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    listings = paginator.get_page(page)
    context = {
         'title':'特殊加分项',
         'bonuses':listings

    }

    return render(request, 'bonuses/index.html', context)

def details(request, id):
    bonus = Bonuses.objects.get(id=id)

    context = {
        'bonus': bonus
    }

    return render(request, 'bonuses/details.html', context)


def welcom(request):
    return render(request, 'posts/welcom.html')
