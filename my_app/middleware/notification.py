from .. models import Notifications, Inventory
from datetime import datetime

class NotificationHandler:
     def __init__(self, get_response):
        self.get_response = get_response
        
     def __call__(self, request):
         medicines = Inventory.objects.filter(expiration__lte = datetime.now())
         
         for medicine in medicines:
             obj, created = Notifications.objects.get_or_create(medicine=medicine)
        
         response = self.get_response(request)
        
         return response