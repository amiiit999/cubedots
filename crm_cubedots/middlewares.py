from django.urls import reverse
from django.shortcuts import redirect


class RestrictUserMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.find("home") > -1:  # restricted admin url for custom admin site
           if not request.user.is_staff:
              return redirect(reverse('login'))
        response = self.get_response(request)
        return response