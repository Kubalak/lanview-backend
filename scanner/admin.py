from django.contrib import admin
from .models import Host, Exclusion, Config
# Register your models here.

admin.site.register(Host)
admin.site.register(Exclusion)
admin.site.register(Config)
