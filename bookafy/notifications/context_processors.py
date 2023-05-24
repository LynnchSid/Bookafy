import datetime
from friends.models import CustomNotification
# from home.models import Offer

def get_notification_count(request):
    notification = CustomNotification.objects.filter(is_read=False, recipient=request.user)
    return {'notification': {'success': True, 'data': notification.count}}
    

