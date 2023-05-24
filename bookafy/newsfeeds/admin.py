from django.contrib import admin

# Register your models here.
from .models import Post,Like,Comment,PostImage, UserPost

admin.site.register(Post)
admin.site.register(UserPost)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(PostImage)