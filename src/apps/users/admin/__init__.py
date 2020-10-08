from django.contrib.admin import site
from django.contrib.auth.models import Group
from ..models import User
from .models import UserAdmin


site.register(User, UserAdmin)
site.unregister(Group)
