from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('accounts.urls')),
    path('accounts/', include('accounts.passwords.urls')),
    
    path('', include('notifications.urls')),
    path('', include('core.urls')),
    path('', include('newsfeeds.urls')),
    path('', include('friends.urls')),
    path('messages/', include('communications.urls')), 
    path('timeline/', include('userprofiles.urls')),


]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)