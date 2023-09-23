from django.urls import path
from . import views

urlpatterns = [
    path('add/', view=views.add),
    path('list/', view=views.index),
    path('get/<int:id>/', view=views.get),
    path('update/<int:id>', view=views.set),
    path('delete/<int:id>', view=views.delete),
    path('login/', view=views.login),
    path('logout/', view=views.logout),
    path('current/', view=views.current),
]