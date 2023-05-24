from django.db import models
from accounts.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from schools.models import School

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to='avatars', default='avatars/guest.png')
    cover_image = models.ImageField(upload_to='avatars', default='avatars/cover.png')
    bio = models.TextField(max_length=500, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')), blank=True, null=True)
    work = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    relationship_status = models.CharField(max_length=20, choices=(('single', 'Single'), ('in_a_relationship', 'In a relationship'), ('married', 'Married'), ('engaged', 'Engaged')), blank=True, null=True)
    interested_in = models.CharField(max_length=20, choices=(('male', 'Male'), ('female', 'Female'), ('both', 'Both')), blank=True, null=True)
    political_views = models.CharField(max_length=100, blank=True, null=True)
    religious_views = models.CharField(max_length=100, blank=True, null=True)
    hometown = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # If the user is being created, set the first name and last name
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
        self.slug = slugify(self.user.phone)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('user_profile_detail', args=[self.slug])
    

# def post_save_user_create_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         profile = UserProfile.objects.create(user=instance)
#         profile.save()

# post_save.connect(post_save_user_create_receiver, sender=User)