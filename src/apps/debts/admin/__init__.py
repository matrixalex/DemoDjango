from ..models import Debt
from .models import DebtAdmin
from django.contrib.admin import site


site.register(Debt, DebtAdmin)
