from django.http import HttpResponse


class ELBHealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get("HTTP_USER_AGENT", "Unknown")
        if user_agent.startswith("ELB-"):
            return HttpResponse("It's all good man", status=200)
        return self.get_response(request)
