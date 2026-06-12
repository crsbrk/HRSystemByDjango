from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from .models import Cutovers

# Create your views here.
def index(request):
    #return HttpResponse('hello django')
    cutovers = Cutovers.objects.all().order_by('-deadline_at')#[:10]
    paginator = Paginator(cutovers, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    listings = paginator.get_page(page)
    context = {
         'title':'割接类',
         'cutovers':listings

    }

    return render(request, 'cutovers/index.html', context)

def details(request, id):
    cutover = get_object_or_404(Cutovers, id=id)

    context = {
        'cutover': cutover
    }

    return render(request, 'cutovers/details.html', context)

def welcom(request):
    return render(request, 'posts/welcom.html')
