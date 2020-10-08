from django.shortcuts import redirect


def index(request):
    """
    Корневой url сайта
    :param request: мета данные
    :return: HttpResponse
    """
    user = request.user
    if not user.is_authenticated:
        return redirect('/auth/login')
    if user.is_superuser:
        return redirect('/admin')
    return redirect('/debts')
