from django.shortcuts import render, redirect
from django.views import View
from . import services


class MyDebtsView(View):
    """
    Контроллер получения, добавления долга
    """

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/auth/login')
        data = {'debts': services.get_user_debts_data(request.user), 'user': request.user}
        print(data)
        return render(request, 'index.html', context=data)
