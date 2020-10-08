from .base_admin import BaseModelAdmin


class LogAdmin(BaseModelAdmin):
    list_display = ('user', 'text', 'created_at')
