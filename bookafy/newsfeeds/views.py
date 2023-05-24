import json
from django.shortcuts import HttpResponse , render, get_object_or_404
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.contants.common import COMMENT_VERB, LIKE_VERB
from friends.models import CustomNotification
from friends.serializers import NotificationSerializer
from .forms import PostCreateForm
from .models import *
from django.http import JsonResponse
from settings.utils import is_ajax


class PostCreateView(CreateView):
    model = Post
    http_method_names = ['post']
    form_class = PostCreateForm
    template_name = 'home.html'
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super(PostCreateView, self).form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        print(form.errors)
        return redirect(reverse_lazy('core:home'))

    def post(self, *args, **kwargs):
        form = self.get_form()
        self.object = None
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def like_post(request):
    if request.method == 'POST' and is_ajax(request):
        post_slug = request.POST.get('post_slug')
        try:
            post = UserPost.objects.get(post__slug=post_slug)
            try:
                like = Like.objects.get(post=post, user=request.user)
                like.delete()
                is_liked = False
                success = True
                message = "Unlike"

                
            except:
                like = Like.objects.create(post=post, user=request.user)
                is_liked = True
                success = True
                message = "Like"
                notification = CustomNotification.objects.create(type="comment",recipient=post.user, actor=request.user, verb=LIKE_VERB,
                                                                description="like on your post")
                channel_layer = get_channel_layer()
                channel = "comment_like_notifications_{}".format(post.user.username)
                async_to_sync(channel_layer.group_send)(
                    channel, {
                        "type": "notify",
                        "command": "new_like_comment_notification",
                        "notification": json.dumps(NotificationSerializer(notification).data),
                        'unread_notifications': CustomNotification.objects.user_unread_notification_count(request.user)
                    }
                )

        except:
            is_liked = False
            success = False
            message = "Something went wrong"

        total_likes = Like.objects.filter(post=post).count()
        response_data ={
            'success': success,
            'slug': post.post.slug,
            'is_liked': is_liked,
            'total_likes': total_likes,
        }
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': False})
    


def create_comment(request, post_id=None):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        comment = post.comments.create(user=request.user, content=request.POST.get('content'))
        notification = CustomNotification.objects.create(recipient=post.user, actor=request.user, verb=COMMENT_VERB,
                                                         description="commented on your post")
        channel_layer = get_channel_layer()
        channel = "comment_like_notifications_{}".format(post.user.username)
        async_to_sync(channel_layer.group_send)(
            channel, {
                "type": "notify",
                "command": "new_like_comment_notification",
                "notification": json.dumps(NotificationSerializer(notification).data),
                'unread_notifications': CustomNotification.objects.user_unread_notification_count(request.user)
            }
        )
        return redirect(reverse_lazy('core:home'))
    else:
        return redirect(reverse_lazy('core:home'))

def test(request):
    user = User.objects.get(username="J5QCZ3QKTVJaYa0")
    notification = CustomNotification.objects.create(recipient=user, actor=request.user, verb=COMMENT_VERB,
                                                         description="His hunxa hai")
    channel_layer = get_channel_layer()
    channel = "comment_like_notifications_{}".format(user.username)
    async_to_sync(channel_layer.group_send)(
        channel, {
            "type": "notify",
            "command": "new_like_comment_notification",
            "notification": json.dumps(NotificationSerializer(notification).data),
            'unread_notifications': CustomNotification.objects.user_unread_notification_count(request.user)
        }
    )
    return HttpResponse('Done')

from friends.serializers import NotificationSerializer, FriendshipRequestSerializer
from friends.models import FriendshipRequest, Friend



def friend_request_test(request):
    username = User.objects.get(username="J5QCZ3QKTVJaYa0")
    if username is not None:
        friend_user = User.objects.get(username=username.username)
        try:
            friend_request = Friend.objects.add_friend(request.user, friend_user, message='Hi! I would like to add you')
        except Exception as e:
            data = {
                'status': False,
                'message': str(e),
            }
            return JsonResponse(data)
        channel_layer = get_channel_layer()
        channel = "all_friend_requests_{}".format(friend_user.username)
        async_to_sync(channel_layer.group_send)(
            channel, {
                "type": "notify",  # method name
                "command": "new_friend_request",
                "notification": FriendshipRequestSerializer(friend_request).data
            }
        )
        data = {
            'status': True,
            'message': "Request sent.",
        }
    return HttpResponse('Done')