from unicodedata import name
from django.urls import path
from news_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home),
    path('add-news/', views.add_news, name='add-news'),
    path('delete-news/<int:id>', views.delete_news, name='delete-news'),
    path('edit-news/<int:id>', views.edit_news, name='edit-news'),  
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
]
