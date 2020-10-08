from .models import BaseModelAdmin, LogAdmin
from django.contrib.admin import site
from ..models import Log

site.register(Log, LogAdmin)
