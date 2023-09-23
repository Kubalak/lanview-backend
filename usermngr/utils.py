from django.http import HttpRequest, JsonResponse


def isAuthenticated(request:HttpRequest):
    return request.user.is_authenticated

def isNotAuthenticated(request:HttpRequest):
    return not request.user.is_authenticated

def canAddUsers(request:HttpRequest):
    return request.user.has_perms("auth.add_user")


class Unauthorized401(JsonResponse):
    def __init__(self, info=None):
        if info is None:
            info = "Unathorized - please log in first"
        super().__init__({"error": info}, status=401)


class DataResponse(JsonResponse):
    def __init__(self, data, fieldname="data", **kwargs):
        """
        Initializes JsonResponse with data labeled by `fieldname` argument.
        """
        super().__init__({fieldname: data}, **kwargs)
        
        
class ErrorResponse(JsonResponse):
    def __init__(self, data, code=400, **kwargs):
        """
        Initializes JsonResponse with data labeled by `fieldname` argument.
        """
        super().__init__({"error": data}, status=code, **kwargs)

def check_login(func):
    def _check(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return Unauthorized401()
    return _check
