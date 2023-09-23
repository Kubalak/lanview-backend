from django.urls import path
from . import views

urlpatterns = [
    path('list/', view=views.index),
    path('hosts/<int:id>/', view=views.host),
    path('config/',view=views.config),
    path('config/update/', view=views.update),
    path('online/<int:id>/', view=views.online)
]