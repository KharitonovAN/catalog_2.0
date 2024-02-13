from django.contrib import admin
from blogpost.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
