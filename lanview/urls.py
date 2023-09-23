"""lanview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# import os
# import time
# import subprocess
# import json
# from django.http import JsonResponse
# from rest_framework.decorators import api_view
# from . import __version__, __build__

# @api_view(['GET'])
# def version(request):
#     FILE_DIR = os.path.dirname(os.path.abspath(__file__))
#     git_command = ['git', 'log', '-1', '--pretty={"commit_hash": "%h", "full_commit_hash": "%H", "author_name": "%an", "commit_date": "%aD", "comment": "%s"}']
#     git_identifier = subprocess.check_output(git_command, cwd=FILE_DIR).decode('utf-8').strip()
#     git_identifier = json.loads(git_identifier)
#     last_updated = time.strftime('%a, %-e %b %Y, %I:%M:%S %p (%Z)', time.localtime(os.path.getmtime('.git'))).strip()
#     return JsonResponse({
#         "last_updated": last_updated,
#         "git_commit": git_identifier,
#         'version': __version__,
#         'build': __build__
#     }, status=200)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('usermngr.urls')),
    path('api/scanner/', include('scanner.urls')),
    # path('api/version/', view=version),
]

handler404 = 'errors.views.handle404'
