from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required(login_url='login')
def index(request):
    categories = Catagory.objects.all()
    first_news = []
    for category in categories:
        category_first_post = News.objects.filter(category=category).order_by('-created_at').first()
        print(category_first_post)
        if category_first_post is not None:
            first_news.append(category_first_post)
    if len(first_news) < 4 and len(first_news) > 0:
        news = News.objects.all().order_by('-id')
        first_news.extend(news[len(news)-4:len(news)-len(first_news)])
    
    news = News.objects.all().order_by('-id')
    

    return render(request, 'index.html', {'categories': categories, 'first_news': first_news, 'news':news})


@login_required(login_url='login')
def category(request, pk):
    category = Catagory.objects.get(id=pk)
    news = News.objects.filter(category=category).order_by('-id')
    categories = Catagory.objects.all()

    return render(request, 'category-01.html', {'news': news, 'categories':categories})

def news_detail(request, pk):
    post = News.objects.get(id=pk)
    comments = Comment.objects.filter(news=post).order_by('-id')[:3]
    if request.method == 'POST':
        comment = request.POST['msg']
        Comment.objects.create(
            news=post,
            pos_text = comment,
            user = request.user
        )
        print(comment)
        messages.info(request, 'Comment qoldindingiz')
        
    return render(request, 'blog-detail-01.html', {'post':post, 'comments':comments})


@login_required(login_url='login')
def profile(request):
    
    user = User.objects.get(username=request.user.username)
    return render(request, 'account/profile.html', {'user':user})

    

