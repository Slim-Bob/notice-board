from django.contrib import admin
from .models import Category, Post, Ad, ResponseAd


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Ad)
admin.site.register(ResponseAd)
