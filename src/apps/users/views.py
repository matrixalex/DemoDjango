from django.contrib.auth import logout
from django.views import View
from django.shortcuts import render, redirect
from . import services as user_services


class LoginView(View):
    """
    Аторизация пользователя
    """

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/debts')
        return render(request, 'login.html')

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/debts')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        data = user_services.authenticate(request, email, password)
        if not data.status:
            return render(request, 'login.html', context={'error': data.message})
        if data.user.is_superuser:
            return redirect('/admin')
        return redirect('/debts')


class LogoutView(View):
    """
    Логаут пользователя из системы
    """

    def get(self, request):
        logout(request)
        return redirect('/auth/login')
