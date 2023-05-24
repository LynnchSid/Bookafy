from django.urls import path
from .views import *

app_name = "newsfeed"

urlpatterns = [
    path('post/create', PostCreateView.as_view(), name="post-create"),
    path('comment/create/<int:post_id>', create_comment, name="comment-create"),
    path('like_post/', like_post, name="like-post"),
    path('test/', test, name="test"),
    path('test/friend/', friend_request_test, name="friend_test"),
]
