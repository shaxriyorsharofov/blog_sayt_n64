from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('category/<int:pk>', category, name='category'),
    path('detail/<int:pk>', news_detail, name='detail'),
    path('profile/', profile, name='profile')
]


