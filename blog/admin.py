from django.contrib import admin
from .models import Blog, BlogAuthor, BlogComment

# Register your models here.
admin.site.register(Blog)
admin.site.register(BlogComment)
admin.site.register(BlogAuthor)
