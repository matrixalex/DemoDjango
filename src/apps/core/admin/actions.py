from ..models import Log


def delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        if str(type(obj)) == "<class 'src.apps.users.models.user.User'>" and obj.id == request.user.id:
            continue
        obj.is_deleted = True
        obj.save()
        Log.objects.create(user=request.user, text=f'Пользователь {request.user} удалил {obj}')
