from django.shortcuts import render, redirect
from django.http import HttpResponse
from news_app.models import News
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required(login_url='signin')
def home(request):
    news = News.objects.all()
    return render(request, 'news_app/home.html', {'news': news})

@login_required(login_url='signin')
def add_news(request):
    if request.method == 'GET':
        return render(request, 'news_app/add-news.html')
    else:
        title = request.POST['title']
        content = request.POST['content']
        News.objects.create(title=title, content=content, user_id=request.user.id)

        return redirect('home')
    
def delete_news(request, id):
    news = News.objects.get(id=id)
    news.delete()

    return redirect('home')

def edit_news(request, id):
    news = News.objects.get(id=id)

    if request.method == 'GET':
        return render(request, 'news_app/edit-news.html', {'news': news})
    else:
        news.title = request.POST['title']
        news.content = request.POST['content']
        news.save()

        return redirect('home')

def register(request):
    if request.method == 'GET':
        return render(request, 'auth/register.html')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(first_name=first_name, last_name=last_name,
                    email=email, username=username, password=password)
        
        send_mail('Account Created',
        f'An account has been created for you with username {username}',
        settings.EMAIL_HOST_USER,
        [email, 'nishaadhikari53@gmail.com', 'shrisab12@gmail.com'],
        fail_silently=False  
        )

        return redirect('signin')
    
def signin(request):
    if request.method == 'GET':
        return render(request, 'auth/signin.html')
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url is None:
                return redirect('home')
            else:
                return redirect(next_url)
        else:
            messages.error(request, 'Username or password is invalid')
            messages.error(request, 'Please try again later.')
            return redirect('signin')

def signout(request):
    logout(request)
    return redirect('signin')

