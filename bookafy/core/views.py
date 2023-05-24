from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from friends.models import Friend
from newsfeeds.models import Post, UserPost


def home(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))

    friends = Friend.objects.friends(request.user)
    # posts = Post.objects.filter(user__in=friends_list_id)
    posts = UserPost.objects.filter(is_active=True, is_deleted=False)
    return render(request, 'home.html', {'posts': posts, 'friends': friends})
