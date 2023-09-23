from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.contrib.auth.models import User

class EventType(models.Model):
    class Importance(models.TextChoices):
        INFO = "INFO", _("INFORMATION")
        WARNING = "WARN", _("WARNING")
        ERROR = "ERR", _("ERROR")
        LOG = "LOG", _("LOG")
        
    name = models.CharField(max_length=64,unique=True)
    importance = models.CharField(
        choices=Importance.choices,
        default=Importance.INFO,
        max_length=5
    )

class Event(models.Model):
    etype = models.ForeignKey("EventType", on_delete=models.PROTECT)
    triggered_by = models.ForeignKey(User, on_delete=models.PROTECT)
    description = models.CharField(max_length=128)
    timestamp = models.DateTimeField(default=now)
    
class Ticket(models.Model):
    name = models.CharField(max_length=64)
    context = models.CharField(max_length=64)
    info = models.TextField()
    timestamp = models.DateTimeField(default=now)