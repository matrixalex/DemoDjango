from django.urls import path, include


urlpatterns = [
    path('', include('src.apps.core.urls')),
    path('auth/', include('src.apps.users.urls')),
    path('debts', include('src.apps.debts.urls')),
]
