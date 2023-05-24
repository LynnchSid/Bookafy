import datetime
from .models import Settings
# from home.models import Offer

def get_company_details(request):
    setting = Settings.load()
    if setting:
        return {'settings': {'success': True, 'data': setting}}
    else:
        return {'settings': {'success': False, 'data': None}}
    

