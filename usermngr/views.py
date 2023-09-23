from django.http import HttpResponse, JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as log_in, logout as log_out
from django.db.models import Q
from .models import Ticket
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from .serializers import UserSerializer, DetailedUserSerializer
from .utils import isNotAuthenticated, isAuthenticated, Unauthorized401, DataResponse
import traceback

# Create your views here.

@api_view(['GET'])
def index(request):
    if isNotAuthenticated(request):
        return Unauthorized401()
    
    users = User.objects.all()
    data = UserSerializer(users, many=True).data
    return DataResponse(data, "users")


@api_view(['POST'])
def add(request: HttpRequest):
    if isNotAuthenticated(request):
        return Unauthorized401()
    
    if 'username' not in request.POST or 'email' not in request.POST or 'password' not in request.POST:
        return DataResponse("Missing required fields!","error", status=400)
    try:
        users = User.objects.filter(Q(username=request.POST['username']) | Q(email=request.POST['email']))
        if users.count() > 0:
            return DataResponse("Cannot create new user - username or email is in use!","error", status=400)
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        return JsonResponse({"message": f"User {user.username} created"})
    except Exception as e:
        Ticket(
            name=str(e),
            context=__file__,
            info=traceback.format_exc()
        ).save()
        return DataResponse("Failed to create new user!","error", status=400)

@api_view(['GET'])
def get(request, id):
    if isNotAuthenticated(request):
        return Unauthorized401()
    
    user = User.objects.filter(pk=id).first()
    return JsonResponse({"user": DetailedUserSerializer(user).data})

def set(request, id):
    if isNotAuthenticated(request):
        return Unauthorized401()
    
    return HttpResponse("OK")

def delete(request, id):
    if isNotAuthenticated(request):
        return Unauthorized401()
    
    return HttpResponse("OK")


@api_view(['GET','POST'])
def login(request: HttpRequest):
    if request.method == 'GET':
        if isAuthenticated(request):
            return DataResponse(True, "authenticated")
        return DataResponse(False, "authenticated")
    try:
        user = authenticate(username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return DataResponse(False, "authenticated")
        else:
            log_in(request=request, user=user)
            return DataResponse(True, "authenticated")
    except Exception as e:
        Ticket(
            name = str(e),
            context = __file__,
            info = traceback.format_exc()
        ).save()
        return JsonResponse({"error": "Request failed"}, status=400)

@api_view(['GET'])
def current(request):
    if isNotAuthenticated(request):
        return Unauthorized401()
    
    return DataResponse(request.user.username, "user")

@api_view(["POST"])
def logout(request):
    log_out(request)
    return JsonResponse({"message": "Success"}, status=207)