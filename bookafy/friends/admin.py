from django.contrib import admin

# Register your models here.
from .models import CustomNotification, Friend, FriendshipRequest

admin.site.register(CustomNotification)
admin.site.register(Friend)
admin.site.register(FriendshipRequest)