from django.db import models

# Create your models here.
from django.db import models
from django.contrib.humanize.templatetags import humanize
from accounts.models import User
from django.utils.timezone import now
import uuid
from django.utils.text import slugify
from helper import unique_code_generator
from django.utils.crypto import get_random_string


class Post(models.Model):
    slug = models.SlugField(null=True, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        self.slug = slugify(get_random_string(length=32))
        super(Post, self).save(*args, **kwargs)

    def get_date(self):
        return humanize.naturaltime(self.created_at)
    
    
class UserPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    is_post = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def get_all_image(self):
        return PostImage.objects.filter(post=self)
    
    def get_total_like_count(self):
        return Like.objects.filter(post=self).count()

    def get_all_comment(self):
        return Comment.objects.filter(post=self)

    def get_all_like(self):
        return Like.objects.filter(post=self)

    

class Like(models.Model):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    
    def __str__(self):
        return f'{self.post} liked by {self.user}'


class Comment(models.Model):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=now)

    def get_date(self):
        return humanize.naturaltime(self.created_at)
    
class PostImage(models.Model):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name="post_images")
    image = models.ImageField(upload_to='post/images/')

    def __str__(self):
        return self.post.body