from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Posts
from accounts.models import HomeSlide
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.
def index(request):
    #return HttpResponse('hello django')
    #posts = Posts.objects.all()[:10]
    posts = Posts.objects.all().order_by('-deadline_at')
    paginator = Paginator(posts, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    listings = paginator.get_page(page)
    context = {
         'title':'项目类',
         'posts':listings

    }

    return render(request, 'posts/index.html', context)

def details(request, id):
    post = get_object_or_404(Posts, id=id)

    context = {
        'post': post
    }

    return render(request, 'posts/details.html', context)


def about(request):
    return HttpResponse("努力积分，争取拿A")

def welcom(request):
    default_slides = [
        {
            'title': '大物移云智',
            'subtitle': 'eMBB 高带宽 / uRLLC 低时延 / mMTC 大连接',
            'image_static': 'welcom/pic/slider/main/slide-1.jpg',
            'link': '#',
        },
        {
            'title': '传承、担当、求索',
            'subtitle': '',
            'image_static': 'img/slide-1.jpg',
            'link': '#',
        },
        {
            'title': '',
            'subtitle': '',
            'image_static': 'img/slide-3.jpg',
            'link': '#',
        },
    ]
    slides = HomeSlide.objects.filter(is_active=True)
    return render(request, 'posts/welcom.html', {
        'home_slides': slides,
        'default_slides': default_slides,
    })
