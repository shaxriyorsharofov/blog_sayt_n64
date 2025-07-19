from django.contrib import admin
from .models import *
# Register your models here.


class NewsAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'user', 'created_at']
    list_filter = ['category', 'user']
    search_fields = ['title__icontains',]
    

admin.site.register(News, NewsAdmin)

admin.site.register(Catagory)