from django.db import models
from .utils import SingletonModel

# Create your models here.
class Settings(SingletonModel):
    site_name = models.CharField(max_length=200)
    slogon = models.CharField(max_length=200, null=True, blank=True)
    logo = models.ImageField(upload_to="settings/logo")
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=50, null=True)
    phone_no = models.CharField(max_length=20)
    mobile_no = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    pan = models.CharField(max_length=50, null=True)
    facebook = models.CharField(max_length=100)
    instagram = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=20)
    about_description = models.CharField(max_length=255)
    site_language = models.CharField(max_length=10)