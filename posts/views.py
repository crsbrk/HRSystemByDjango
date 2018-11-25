from django.shortcuts import render
from django.http import HttpResponse
from .models import Posts

# Create your views here.
def index(request):
    #return HttpResponse('hello django')
    posts = Posts.objects.all()[:10]

    context = {
         'title':'项目类',
         'posts':posts

    }

    return render(request, 'posts/index.html', context)

def details(request, id):
    post = Posts.objects.get(id=id)

    context = {
        'post': post
    }

    return render(request, 'posts/details.html', context)


def about(request):
    return HttpResponse("努力积分，争取拿A")

def welcom(request):
    return render(request, 'posts/welcom.html')
