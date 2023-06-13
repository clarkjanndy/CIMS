from datetime import datetime
from django.http import HttpResponseForbidden

class DateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define the date from which the 403 response should be returned
        forbidden_date = datetime(year=2023, month=6, day=15)  # Replace with your desired date

        # Check if the current date is after the forbidden date
        if datetime.now() >= forbidden_date:
            return self.forbidden_response()

        return self.get_response(request)

    def forbidden_response(self):
        return HttpResponseForbidden()
